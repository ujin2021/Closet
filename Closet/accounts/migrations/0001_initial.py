# Generated by Django 3.0.6 on 2020-07-23 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(blank=True, max_length=200, null=True)),
                ('username', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'account',
            },
        ),
        migrations.CreateModel(
            name='Clothes_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default=False, max_length=255, upload_to='%Y/%m/%d')),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('top', models.CharField(blank=True, max_length=50, null=True)),
                ('bottom', models.CharField(blank=True, max_length=50, null=True)),
                ('outer', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'clothes_category',
            },
        ),
        migrations.CreateModel(
            name='Social_Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(max_length=50)),
                ('uid', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'social_login',
            },
        ),
        migrations.CreateModel(
            name='User_Closet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clothes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Clothes_category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Account')),
            ],
            options={
                'db_table': 'user_closet',
            },
        ),
        migrations.AddField(
            model_name='account',
            name='social',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Social_Login'),
        ),
    ]
