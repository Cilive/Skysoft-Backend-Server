# Generated by Django 4.0 on 2022-01-22 20:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_alter_accountledger_branches_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='bank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.bankaccountmaster', verbose_name='bank'),
        ),
    ]
