# Generated by Django 5.1.1 on 2024-10-28 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saintApp', '0014_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
