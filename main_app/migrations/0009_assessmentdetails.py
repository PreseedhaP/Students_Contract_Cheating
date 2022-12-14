# Generated by Django 3.1.1 on 2022-09-10 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_academicengagement'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AD1', models.CharField(choices=[('HIGH', 'HIGH'), ('MEDIUM', 'MEDIUM'), ('LOW', 'LOW'), ('NA', 'NA')], default='NA', max_length=10, verbose_name='Has the lecturer participated in any training/learning sessions on contract cheating hosted by the higher education institute?')),
                ('AD2', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Does the assessment design ensure relatively higher possibility of detecting contract cheating?')),
                ('AD3', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Is there a similarity reported on a block of references in thebibliography?')),
                ('AD4', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Are there any references mentioned in the documents that have been submitted by the student?')),
                ('AD5', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Has the student used sources that are specific to the assessment topic rather than generic or outdated ones in the references?')),
                ('AD6', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Do the citations from the references appear in the text as well?')),
                ('AD7', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Is there a reasonable range of reference access dates in bibliography?')),
                ('AD8', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Has the student used the correct referencing style as mentioned in the assessment brief?')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.subject')),
            ],
        ),
    ]
