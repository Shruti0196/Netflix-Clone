# Generated by Django 3.2.6 on 2022-07-26 18:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('NetflixApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='paidMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('type', models.CharField(choices=[('seasonal', 'Seasonal'), ('single', 'Single')], max_length=10)),
                ('flyer', models.ImageField(upload_to='flyers')),
                ('age_limit', models.CharField(choices=[('All', 'All'), ('KIDS', 'KIDS')], max_length=10)),
                ('amount', models.IntegerField(default=0, max_length=5)),
                ('videos', models.ManyToManyField(to='NetflixApp.Video')),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='purchased_movie',
            field=models.ManyToManyField(blank=True, to='NetflixApp.paidMovie'),
        ),
    ]
