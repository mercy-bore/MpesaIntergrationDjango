# Generated by Django 4.0.4 on 2022-07-12 19:57

from django.db import migrations, models
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='B2CTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_no', models.CharField(default=uuid.uuid4, max_length=50, unique=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('checkout_request_id', models.CharField(max_length=200)),
                ('reference', models.CharField(blank=True, max_length=40)),
                ('description', models.TextField(blank=True, null=True)),
                ('amount', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[(1, 'Pending'), (0, 'Complete')], default=1, max_length=15)),
                ('receipt_no', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ip', models.CharField(blank=True, max_length=200, null=True)),
                ('ReceiverPartyPublicName', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
