# Generated by Django 4.2.16 on 2024-12-04 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('car_type', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=10)),
                ('year', models.IntegerField(default=0)),
                ('is_manual_input', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('number', 'year')},
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('sell_average', models.IntegerField(default=0)),
                ('buy_average', models.IntegerField(default=0)),
                ('sell_count', models.IntegerField(default=0)),
                ('buy_count', models.IntegerField(default=0)),
                ('manual_price', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='car.car')),
            ],
        ),
    ]
