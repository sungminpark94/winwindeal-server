# Generated by Django 4.2.16 on 2024-12-11 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='social_provider',
            field=models.CharField(blank=True, choices=[('KAKAO', 'Kakao')], max_length=20, null=True),
        ),
    ]