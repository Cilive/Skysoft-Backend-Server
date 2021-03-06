# Generated by Django 4.0 on 2022-01-26 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_bankaccountmaster_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashmaster',
            name='credit_balance',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='cashmaster',
            name='debit_balance',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='owner',
            name='email',
            field=models.EmailField(max_length=100),
        ),
        migrations.AlterField(
            model_name='owner',
            name='phone',
            field=models.CharField(max_length=30),
        ),
    ]
