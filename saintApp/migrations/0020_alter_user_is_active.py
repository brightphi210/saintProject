# Generated by Django 5.1.1 on 2024-10-28 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saintApp', '0019_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
