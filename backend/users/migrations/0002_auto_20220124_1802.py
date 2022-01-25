# Generated by Django 2.2.26 on 2022-01-24 15:02

import django.contrib.auth.models
import django.db.models.deletion
import django.db.models.expressions
import users.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProxyForSubscription',
            fields=[
            ],
            options={
                'verbose_name': 'Subscription',
                'verbose_name_plural': 'Subscriptions',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',), 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='user',
            name='confirmation_code',
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, help_text='Enter the email.', max_length=254, unique=True, verbose_name='Email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(help_text='Enter the first name.', max_length=150, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(help_text='Enter the last name.', max_length=150, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(help_text='Enter the password.', max_length=150, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Enter the username.', max_length=150, unique=True, validators=[users.validators.UsernameMeValidator()], verbose_name='Username'),
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribed', models.ForeignKey(help_text='Subscribed', on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Subscribed')),
                ('subscriber', models.ForeignKey(help_text='Subscriber', on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Subscriber')),
            ],
            options={
                'verbose_name': 'Subscription',
                'verbose_name_plural': 'Subscriptions',
            },
        ),
        migrations.AddConstraint(
            model_name='usersubscription',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, subscriber=django.db.models.expressions.F('subscribed')), name='subscribed_to_yourself'),
        ),
        migrations.AddConstraint(
            model_name='usersubscription',
            constraint=models.UniqueConstraint(fields=('subscriber', 'subscribed'), name='subscription_exists'),
        ),
    ]