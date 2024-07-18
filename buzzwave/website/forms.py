from django import forms
from website.models import Blog
from django_summernote.widgets import SummernoteWidget

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'image', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'id' : 'title',
                'class': "form-control",
                'placeholder': "제목을 입력해주세요"
            }),
            'image': forms.FileInput(attrs={
                'id' : 'image',
                'class': "form-control"
            }),
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '700'}}),
        }
