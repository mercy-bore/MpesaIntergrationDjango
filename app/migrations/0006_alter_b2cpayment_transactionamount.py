# Generated by Django 4.0.4 on 2022-07-03 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_b2cpayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='b2cpayment',
            name='TransactionAmount',
            field=models.IntegerField(),
        ),
    ]