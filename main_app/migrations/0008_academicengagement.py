# Generated by Django 3.1.1 on 2022-09-08 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_assessmentanalysis'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicEngagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AG1', models.CharField(choices=[('HIGH', 'HIGH'), ('MEDIUM', 'MEDIUM'), ('LOW', 'LOW'), ('NA', 'NA')], default='NA', max_length=10, verbose_name='What is the level of engagement of the student in the module?')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.subject')),
            ],
        ),
    ]
