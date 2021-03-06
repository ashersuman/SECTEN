# Generated by Django 3.0.4 on 2020-06-13 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advposts', '0008_auto_20200510_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploaded_files/')),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='biddetails',
            name='bidFilePath',
            field=models.FileField(upload_to='bids'),
        ),
    ]
