# Generated by Django 3.0.6 on 2020-08-08 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200808_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clothes_category',
            name='bottom',
        ),
        migrations.RemoveField(
            model_name='clothes_category',
            name='outer',
        ),
        migrations.RemoveField(
            model_name='clothes_category',
            name='top',
        ),
        migrations.AddField(
            model_name='clothes_category',
            name='category',
            field=models.CharField(default='none', max_length=10),
        ),
        migrations.AddField(
            model_name='clothes_category',
            name='pattern',
            field=models.CharField(default='none', max_length=20),
        ),
        migrations.AlterField(
            model_name='clothes_category',
            name='color',
            field=models.CharField(default='none', max_length=15),
        ),
    ]
