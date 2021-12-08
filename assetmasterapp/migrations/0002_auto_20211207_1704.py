# Generated by Django 3.2.9 on 2021-12-07 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assetmasterapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='asset_type',
            field=models.CharField(choices=[('EQUITY', 'Equity'), ('ETF', 'ETF(Equity Trade Fund)'), ('BOND', 'Bond'), ('REITS', 'Reits'), ('PENSION', 'Pension'), ('CRYPTO', 'Crypto Asset')], max_length=100),
        ),
        migrations.AlterField(
            model_name='asset',
            name='currency',
            field=models.CharField(choices=[('KRW', 'KRW(￦)'), ('USD', 'USD($)')], max_length=10),
        ),
    ]