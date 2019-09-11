# Generated by Django 2.2 on 2019-05-11 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20190504_0211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instagram_association',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(default='DEFAULT VALUE', max_length=200)),
                ('year', models.CharField(max_length=10)),
                ('association', models.CharField(max_length=200)),
                ('frequency', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Musinsa_association',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(default='DEFAULT VALUE', max_length=200)),
                ('year', models.CharField(max_length=10)),
                ('association', models.CharField(max_length=200)),
                ('frequency', models.BigIntegerField()),
            ],
        ),
    ]
