# Generated by Django 2.2.2 on 2020-10-09 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0002_auto_20201009_0509'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendinduser',
            name='linkedin_user_url',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]