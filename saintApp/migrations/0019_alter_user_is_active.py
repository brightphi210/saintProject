# Generated by Django 5.1.1 on 2024-10-28 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saintApp', '0018_alter_user_id_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]