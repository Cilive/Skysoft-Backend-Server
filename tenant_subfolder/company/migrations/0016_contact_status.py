# Generated by Django 4.0 on 2022-02-09 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0015_invoice_base_64_encoded'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]