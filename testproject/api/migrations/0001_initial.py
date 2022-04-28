# Generated by Django 4.0.4 on 2022-04-28 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.country')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.sector')),
            ],
        ),
        migrations.CreateModel(
            name='Loans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=255)),
                ('date', models.CharField(max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.projects')),
            ],
        ),
    ]
