from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView
from django.utils.html import format_html
from django.contrib.auth.password_validation import password_validators_help_texts
from django.contrib.auth.forms import (
    SetPasswordForm
)
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from website.views.authentication_views.validate_views import validate_password

def _custom_password_validators_help_text_html(password_validators=None):
    """
        Return an HTML string with all help texts of all configured validators
        in an <ul>.
    """
    # help_texts = password_validators_help_texts(password_validators)
    # help_items = [format_html('<li>{}</li>', help_text) for help_text in help_texts]
    #<------------- append your hint here in help_items  ------------->
    help_items = []
    help_items.append(format_html('<li>Your password can’t be too similar to your other personal information.</li>'))
    help_items.append(format_html('<li>Your password must be 8 to 16 characters.</li>'))
    help_items.append(format_html('<li>Your password must contain at least one letter.</li>'))
    help_items.append(format_html('<li>Your password must contain at least one number.</li>'))

    return '<ul>%s</ul>' % ''.join(help_items) if help_items else ''


class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
        'regex_failed': _('Your password must be 8 to 16 characters.'),
    }
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
                'autocomplete': 'new-password',
                'class': 'form-control', 
                'placeholder': 'New Password',
                "id" : "new-password1"
            }),
    )
    new_password2 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control', 
            'placeholder': 'Confirm Password',
            'id':'new-password2'
        }),
        help_text=_custom_password_validators_help_text_html(),
    )
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
            if not validate_password(password=password2):
                raise ValidationError(
                    self.error_messages['regex_failed'],
                    code='regex_failed',
                )
        return password2

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('website:password_reset_complete')
    form_class = CustomSetPasswordForm
    template_name = 'authentication/password_reset_confirm.html'


class UserPasswordResetView(PasswordResetView):
    template_name = 'authentication/password_reset.html'
    success_url = reverse_lazy('website:password_reset_done')
    email_template_name = "authentication/password_reset_email.html"
    subject_template_name = "authentication/password_reset_subject.txt"
    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'authentication/password_reset_done_fail.html')

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'authentication/password_reset_done.html'

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'authentication/password_reset_complete.html'
