# Generated by Django 3.1.1 on 2022-08-27 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_student_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evidence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=60)),
                ('priority', models.CharField(max_length=60)),
                ('category', models.CharField(max_length=60)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.student')),
            ],
        ),
    ]
