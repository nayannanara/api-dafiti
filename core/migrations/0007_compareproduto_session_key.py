# Generated by Django 3.1.7 on 2021-03-28 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210328_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='compareproduto',
            name='session_key',
            field=models.CharField(db_index=True, max_length=40, null=True, verbose_name='Chave da sessão'),
        ),
    ]
