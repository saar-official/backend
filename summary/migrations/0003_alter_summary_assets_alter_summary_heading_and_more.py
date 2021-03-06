# Generated by Django 4.0.3 on 2022-03-29 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0002_summary_assets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='assets',
            field=models.CharField(max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='summary',
            name='heading',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='summary',
            name='highlights',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='summary',
            name='link',
            field=models.CharField(blank=True, max_length=10000),
        ),
        migrations.AlterField(
            model_name='summary',
            name='ministry',
            field=models.CharField(choices=[('CENTRAL MINISTRY', 'Ministry 1'), ('STATE MINISTRY', 'Ministry 2')], max_length=10000),
        ),
        migrations.AlterField(
            model_name='summary',
            name='summary',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='summary',
            name='text',
            field=models.CharField(blank=True, max_length=10000),
        ),
    ]
