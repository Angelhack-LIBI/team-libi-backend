# Generated by Django 3.0.8 on 2020-07-18 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('libi_sharing', '0002_auto_20200718_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharingapply',
            name='apply_amount',
            field=models.IntegerField(help_text='구매 수량'),
        ),
        migrations.AlterField(
            model_name='sharingapply',
            name='apply_price',
            field=models.IntegerField(help_text='구매 합산 총액'),
        ),
        migrations.AlterField(
            model_name='sharingapply',
            name='sharing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='applies', to='libi_sharing.Sharing'),
        ),
    ]
