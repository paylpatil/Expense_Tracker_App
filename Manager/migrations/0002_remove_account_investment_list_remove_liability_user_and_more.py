# Generated by Django 5.1.4 on 2024-12-24 21:54

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='investment_list',
        ),
        migrations.RemoveField(
            model_name='liability',
            name='user',
        ),
        migrations.RemoveField(
            model_name='account',
            name='liability_list',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='user',
        ),
        migrations.RemoveField(
            model_name='account',
            name='subscription_list',
        ),
        migrations.RemoveField(
            model_name='account',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='account',
            name='income',
        ),
        migrations.RemoveField(
            model_name='account',
            name='saving_goal',
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.FloatField(default=0)),
                ('date', models.DateField(default=datetime.date(2024, 12, 25))),
                ('long_term', models.BooleanField(default=False)),
                ('interest_rate', models.FloatField(blank=True, default=0, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('monthly_expenses', models.FloatField(blank=True, default=0, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='expense_list',
            field=models.ManyToManyField(blank=True, to='Manager.expense'),
        ),
        migrations.DeleteModel(
            name='Investments',
        ),
        migrations.DeleteModel(
            name='Liability',
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
