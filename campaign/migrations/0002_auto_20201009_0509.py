# Generated by Django 2.2.2 on 2020-10-09 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='compaign_name',
            new_name='campaign_name',
        ),
        migrations.AddField(
            model_name='campaign',
            name='user_id',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
