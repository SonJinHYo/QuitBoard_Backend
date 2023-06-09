# Generated by Django 4.2 on 2023-05-05 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cctvs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Violation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('law', models.TextField()),
            ],
            options={
                'verbose_name_plural': '위반규정 관리',
            },
        ),
        migrations.CreateModel(
            name='ViolationInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.URLField(max_length=300, verbose_name='이미지 URL')),
                ('detected_time', models.DateTimeField()),
                ('cctv', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='v_info', to='cctvs.cctv')),
                ('violations', models.ManyToManyField(related_name='v_info', to='violations.violation')),
            ],
            options={
                'verbose_name_plural': '규정 위반 데이터 관리',
            },
        ),
    ]
