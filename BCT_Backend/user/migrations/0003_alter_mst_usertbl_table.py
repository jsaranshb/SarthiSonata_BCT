# Generated by Django 5.0.9 on 2024-09-14 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_mst_usertbl_options'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='mst_usertbl',
            table='accounts_Mst_UserTbl',
        ),
    ]
