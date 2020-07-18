# Generated by Django 3.0.8 on 2020-07-18 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libi_sharing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharingoption',
            name='minimum_price',
        ),
        migrations.AlterField(
            model_name='sharingoption',
            name='description',
            field=models.CharField(help_text='상품 판매 단위', max_length=16),
        ),
        migrations.AlterField(
            model_name='sharingoption',
            name='price',
            field=models.IntegerField(help_text='상품 판매 단위당 가격'),
        ),
        migrations.AlterField(
            model_name='sharingoption',
            name='sharing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='options', to='libi_sharing.Sharing'),
        ),
        migrations.AlterField(
            model_name='sharingphoto',
            name='sharing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='photos', to='libi_sharing.Sharing'),
        ),
    ]
