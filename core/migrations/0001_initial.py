# Generated by Django 3.1.7 on 2021-03-25 15:02

import autoslug.fields
from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('descricao', models.CharField(max_length=255, verbose_name='Descrição do produto')),
                ('preco_original', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço do produto')),
                ('preco_promocional', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Preço do produto')),
                ('tp_promocao', models.CharField(max_length=100, verbose_name='Tipo de promoção')),
                ('link_produto', models.CharField(blank=True, max_length=255, null=True, verbose_name='Link do produto')),
                ('link_img_produto', models.CharField(blank=True, max_length=255, null=True, verbose_name='Link da imagem do produto')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='ds_produto', unique=True)),
                ('status', models.BooleanField(default=False, verbose_name='Ativo?')),
                ('marca', models.CharField(max_length=25, verbose_name='Marca')),
                ('loja', models.CharField(max_length=25, verbose_name='Loja')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
    ]