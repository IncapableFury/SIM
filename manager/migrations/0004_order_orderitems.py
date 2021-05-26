# Generated by Django 3.2.3 on 2021-05-26 02:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_alter_item_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PD', 'Pending'), ('SP', 'Shipping'), ('FN', 'Finished')], default='PD', max_length=2)),
                ('created_time', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=500, null=True)),
                ('shipping_address', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='manager.item')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orderitems', to='manager.order')),
            ],
        ),
    ]