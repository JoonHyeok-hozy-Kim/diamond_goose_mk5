# Generated by Django 3.2.9 on 2021-12-16 06:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portfolioapp', '0002_auto_20211206_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pension_type', models.CharField(choices=[('퇴직연금', '퇴직연금'), ('연금저축', '연금저축'), ('IRP', 'IRP')], max_length=30)),
                ('total_paid_amount', models.FloatField(default=0)),
                ('total_current_value', models.FloatField(default=0)),
                ('total_profit_amount', models.FloatField(default=0)),
                ('risk_ratio_force_flag', models.BooleanField(default=False)),
                ('risk_ratio', models.FloatField(default=0.7, null=True)),
                ('current_risk_asset_ratio', models.FloatField(default=0, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pension', to=settings.AUTH_USER_MODEL)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pension', to='portfolioapp.portfolio')),
            ],
        ),
    ]
