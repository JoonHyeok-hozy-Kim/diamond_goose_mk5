# Generated by Django 3.2.9 on 2021-12-16 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assetmasterapp', '0003_asset_current_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='asset_type',
            field=models.CharField(choices=[('EQUITY', 'Equity'), ('GUARDIAN', 'Guardian'), ('REITS', 'Reits'), ('PENSION', 'Pension'), ('CRYPTO', 'Crypto Asset')], max_length=100),
        ),
    ]
