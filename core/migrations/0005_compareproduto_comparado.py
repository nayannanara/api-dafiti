# Generated by Django 3.1.7 on 2021-03-28 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210328_0401'),
    ]

    operations = [
        migrations.AddField(
            model_name='compareproduto',
            name='comparado',
            field=models.BooleanField(default=False, verbose_name='Houve comparação?'),
        ),
    ]