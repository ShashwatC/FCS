# Generated by Django 2.1.2 on 2018-10-31 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_trans_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trans',
            name='r_id',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='trans',
            name='u_id',
            field=models.TextField(),
        ),
    ]
