# Generated by Django 4.2 on 2023-05-29 14:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cctvs', '0003_alter_violationfile_options_alter_violationfile_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='violationfile',
            name='file',
            field=models.FileField(help_text='zip을 업로드하세요. zip파일 구조는 다음과 같아야 합니다. <br/>        - filename.zip<br/>          &nbsp&nbsp&nbsp&nbsp- violations<br/>          &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp- 1.txt<br/>          &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp- 2.txt<br/>          &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp:<br/>          &nbsp&nbsp&nbsp&nbsp- images<br/>          &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp- 1.png<br/>          &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp- 2.png<br/>          &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp:', upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['zip'])]),
        ),
    ]
