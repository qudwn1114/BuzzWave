from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    '''
    토큰 생성 함수
    '''
    def _make_hash_value(self, user, timestamp):
        return (str(user.pk) + str(timestamp)) +  str(user.is_active)

account_activation_token = AccountActivationTokenGenerator()