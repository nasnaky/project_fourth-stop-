# Generated by Django 4.0.5 on 2022-08-06 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('img1', models.ImageField(upload_to='Auction/')),
                ('img2', models.ImageField(blank=True, null=True, upload_to='Auction/')),
                ('img3', models.ImageField(blank=True, null=True, upload_to='Auction/')),
                ('img4', models.ImageField(blank=True, null=True, upload_to='Auction/')),
                ('img5', models.ImageField(blank=True, null=True, upload_to='Auction/')),
                ('content', models.TextField()),
                ('start_money', models.IntegerField()),
                ('today_money', models.IntegerField()),
                ('auction_date', models.DateTimeField()),
                ('ship', models.TextField()),
                ('ship_money', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=128)),
                ('address', models.TextField()),
                ('name', models.TextField()),
                ('bank', models.IntegerField(default=0)),
                ('trust', models.IntegerField(default=75)),
                ('token', models.TextField(blank=True, null=True)),
                ('token_max_date', models.DateTimeField(blank=True, null=True)),
                ('admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User_img',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to='user/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auction.user')),
            ],
        ),
        migrations.CreateModel(
            name='Inform_cope',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deletes', models.BooleanField(blank=True, null=True)),
                ('minus', models.IntegerField(default=0)),
                ('passed', models.BooleanField(blank=True, null=True)),
                ('content', models.TextField()),
                ('by_inform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auction.alarm')),
            ],
        ),
        migrations.CreateModel(
            name='Inform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_inform', models.TextField()),
                ('auction_inform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auction.auction')),
                ('user_by_inform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_by_inform', to='Auction.user')),
                ('user_inform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_inform', to='Auction.user')),
            ],
        ),
        migrations.CreateModel(
            name='Auction_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('auction_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auction.auction')),
                ('user_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auction.user')),
            ],
        ),
        migrations.CreateModel(
            name='Auction_Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('result', models.BooleanField(blank=True, null=True)),
                ('auction_Receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auction.auction')),
                ('user_Receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auction.user')),
            ],
        ),
        migrations.AddField(
            model_name='auction',
            name='make_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Auction.user'),
        ),
        migrations.AddField(
            model_name='alarm',
            name='user_alarm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auction.user'),
        ),
    ]
