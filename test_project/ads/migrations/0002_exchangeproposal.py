# Generated by Django 5.2.4 on 2025-07-13 01:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeProposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Ожидает'), ('accepted', 'Принят'), ('declined', 'Отклонён')], default='pending')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ad_reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recieved_proposals', to='ads.category')),
                ('ad_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_proposals', to='ads.category')),
            ],
        ),
    ]
