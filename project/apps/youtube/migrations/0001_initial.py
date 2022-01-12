# Generated by Django 3.2.8 on 2022-01-12 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyYoutube',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('absolute_path', models.CharField(blank=True, max_length=255, null=True)),
                ('slug_title', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_info', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Youtube object',
                'verbose_name_plural': 'Youtube objects',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_info', models.CharField(blank=True, max_length=255)),
                ('visit_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Visitor',
                'verbose_name_plural': 'Visitors',
                'ordering': ('-visit_time',),
            },
        ),
    ]