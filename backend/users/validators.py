''' Validators for models in 'users' application. '''

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameMeValidator(UnicodeUsernameValidator):
    ''' Check the username value to 'me'. '''
    message_me = _(
        '''Enter a valid username. The value 'me' is forbidden as username.'''
    )

    def __call__(self, value):
        if str(value).lower() == 'me':
            raise ValidationError(self.message_me, code=self.code)
        return super().__call__(value)
