''' Database entry models for 'users' application. '''

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import UsernameMeValidator


class User(AbstractUser):
    ''' Stores a single user entry. '''
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]
    username = models.CharField(
        _('Username'),
        max_length=150,
        unique=True,
        validators=[UsernameMeValidator()],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
        help_text=_('Enter the username.'),
    )
    email = models.EmailField(
        _('Email address'),
        max_length=254,
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
        help_text=_('Enter the email.'),
    )
    first_name = models.CharField(
        _('First name'),
        max_length=150,
        help_text=_('Enter the first name.'),
    )
    last_name = models.CharField(
        _('Last name'),
        max_length=150,
        help_text=_('Enter the last name.'),
    )
    password = models.CharField(
        _('Password'),
        max_length=150,
        help_text=_('Enter the password.'),
    )
    subscriptions = models.ManyToManyField(
        'self',
        through='UserSubscription',
        through_fields=('subscriber', 'subscribed'),
        symmetrical=False,
        verbose_name=_('Subscriptions')
    )
    objects = UserManager()

    class Meta(AbstractUser.Meta):
        ordering = ('id',)

    def __str__(self):
        ''' Return string in format 'first_name last_name'. '''
        return self.get_full_name()


class UserProxyForSubscription(User):

    class Meta:
        proxy = True
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')


class UserSubscription(models.Model):
    '''
    Stores the relation between :model:'users.User'
    user as subscriber and :model:'users.User' other users as subscribed.
    '''
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=_('Subscriber'),
        help_text=_('Subscriber'),
    )

    subscribed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=_('Subscribed'),
        help_text=_('Subscribed'),
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('subscribed')),
                name='subscribed_to_yourself',
            ),
            models.UniqueConstraint(
                fields=['subscriber', 'subscribed'],
                name='subscription_exists'
            ),
        ]
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')

    def __str__(self):
        ''' Return string in format 'subscriber - subscribed'. '''
        return f'{self.subscriber} - {self.subscribed}'
