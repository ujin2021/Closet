# Generated by Django 3.0.6 on 2020-08-07 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_account_raspberry'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothes_category',
            name='pattern',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
