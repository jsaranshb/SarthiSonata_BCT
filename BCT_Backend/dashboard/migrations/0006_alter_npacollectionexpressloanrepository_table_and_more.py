# Generated by Django 5.0.9 on 2024-09-17 05:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_businesscallingdata_table_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='npacollectionexpressloanrepository',
            table='npa_collection_repository',
        ),
        migrations.AlterModelTable(
            name='pending_proposal_data',
            table='Pending_Proposal_Data',
        ),
        migrations.AlterModelTable(
            name='pendingpromisedata',
            table='PendingPromiseData',
        ),
    ]
