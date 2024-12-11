# Generated by Django 5.1.4 on 2024-12-11 14:44

import django.contrib.auth.password_validation
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='saeed', help_text='Required. At least 5 characters long.', max_length=150, unique=True, validators=[django.core.validators.MinLengthValidator(5, message='Username must be at least 5 characters long')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(help_text='Required. A valid email address.', max_length=255, unique=True, validators=[django.core.validators.EmailValidator(message='Enter a valid email address')]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(help_text='Password must be at least 8 characters long, contain an uppercase letter, a number, and a special character.', max_length=128, validators=[django.contrib.auth.password_validation.validate_password]),
        ),
    ]