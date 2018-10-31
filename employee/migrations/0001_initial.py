# Generated by Django 2.1.2 on 2018-10-31 20:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_id', models.IntegerField()),
                ('u_id', models.TextField()),
                ('r_id', models.TextField()),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete='PROTECT', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
