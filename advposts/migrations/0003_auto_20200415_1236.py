# Generated by Django 3.0.4 on 2020-04-15 07:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('org', '0007_auto_20200415_0044'),
        ('advposts', '0002_auto_20200415_0102'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advdetails',
            options={'verbose_name_plural': 'Advertisement Details'},
        ),
        migrations.CreateModel(
            name='BidDetails',
            fields=[
                ('bidID', models.AutoField(primary_key=True, serialize=False)),
                ('bidPartID', models.CharField(max_length=70)),
                ('bidFilePath', models.FileField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bidderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('orgID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.Org')),
                ('tenderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advposts.AdvDetails')),
            ],
            options={
                'verbose_name_plural': 'Bidding Details',
            },
        ),
    ]