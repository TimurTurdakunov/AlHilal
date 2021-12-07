# Generated by Django 3.2.5 on 2021-08-09 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CardType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('alpha2', models.CharField(max_length=2)),
                ('alpha3', models.CharField(max_length=3)),
                ('name_official_eng', models.CharField(max_length=255)),
                ('name_official_rus', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='KatoRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OldCif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cif', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TariffPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='KatoDistrict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.IntegerField()),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directories.katoregion')),
            ],
        ),
        migrations.CreateModel(
            name='KatoCommunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.IntegerField()),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directories.katodistrict')),
            ],
        ),
    ]
