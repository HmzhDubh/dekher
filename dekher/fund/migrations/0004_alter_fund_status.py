# Generated by Django 5.1.2 on 2025-03-07 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0003_fund_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fund',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Finished', 'Finished'), ('In Progress', 'In Progress'), ('Preparing', 'Preparing'), ('Canceled', 'Canceled')], default='New', max_length=11),
        ),
    ]
