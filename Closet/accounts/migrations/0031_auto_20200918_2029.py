# Generated by Django 3.0.6 on 2020-09-18 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_auto_20200918_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frequency_fashion',
            name='bottom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fre_bottom', to='accounts.Clothes_category'),
        ),
        migrations.AlterField(
            model_name='frequency_fashion',
            name='dress',
            field=models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fre_dress', to='accounts.Clothes_category'),
        ),
        migrations.AlterField(
            model_name='frequency_fashion',
            name='outer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fre_outer', to='accounts.Clothes_category'),
        ),
        migrations.AlterField(
            model_name='frequency_fashion',
            name='top',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fre_top', to='accounts.Clothes_category'),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='bottom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rec_bottom', to='accounts.Clothes_category'),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='dress',
            field=models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rec_dress', to='accounts.Clothes_category'),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='outer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rec_outer', to='accounts.Clothes_category'),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='top',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rec_top', to='accounts.Clothes_category'),
        ),
    ]
