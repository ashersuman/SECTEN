# Generated by Django 3.0.4 on 2020-04-22 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_accountuser_org_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountuser',
            name='username',
        ),
    ]