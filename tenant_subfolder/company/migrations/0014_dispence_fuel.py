# Generated by Django 4.0 on 2022-02-07 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0013_alter_meterreading_fuel_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispence',
            name='fuel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.fuelmaster', verbose_name='fuel'),
        ),
    ]