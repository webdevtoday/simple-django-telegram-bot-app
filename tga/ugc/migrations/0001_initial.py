# Generated by Django 4.1.2 on 2022-10-31 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.PositiveIntegerField(verbose_name='Social user ID')),
                ('name', models.TextField(verbose_name='Username')),
            ],
            options={
                'verbose_name': 'Profile',
            },
        ),
    ]