# Generated by Django 4.2.7 on 2023-12-14 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_user_mobile_user_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phone_number',
            new_name='mobile',
        ),
    ]
