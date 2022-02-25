# Generated by Django 4.0 on 2022-01-21 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_alter_invoice_emp_alter_meterreading_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountledger',
            name='total_expense',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='accountledger',
            name='total_purchase',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='accountledger',
            name='total_sales',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='accountledger',
            name='total_transactions',
            field=models.FloatField(null=True),
        ),
    ]