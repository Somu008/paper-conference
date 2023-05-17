from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return (
        user.pk + timestamp 
        # text_type(user.profile.signup_confirmation)
        )

generate_token = TokenGenerator()