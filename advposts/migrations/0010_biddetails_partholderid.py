# Generated by Django 3.0.4 on 2020-08-27 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0010_auto_20200423_0051'),
        ('advposts', '0009_auto_20200613_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='biddetails',
            name='partHolderID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='org.OrgUser'),
            preserve_default=False,
        ),
    ]