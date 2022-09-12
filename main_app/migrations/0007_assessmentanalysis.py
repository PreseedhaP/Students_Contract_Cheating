# Generated by Django 3.1.1 on 2022-09-08 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20220904_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentAnalysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DS1', models.CharField(choices=[('HIGH', 'HIGH'), ('MEDIUM', 'MEDIUM'), ('LOW', 'LOW'), ('NA', 'NA')], default='NA', max_length=10, verbose_name='Similarity score reported on Turnitln')),
                ('DS2', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Is the work submitted by the student very similar to that of another student?')),
                ('DS3', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Is there a similarity reported on a block of references in thebibliography?')),
                ('DR1', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Are there any references mentioned in the documents that have been submitted by the student?')),
                ('DR2', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Has the student used sources that are specific to the assessment topic rather than generic or outdated ones in the references?')),
                ('DR3', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Do the citations from the references appear in the text as well?')),
                ('DR4', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Is there a reasonable range of reference access dates in bibliography?')),
                ('DR5', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Has the student used the correct referencing style as mentioned in the assessment brief?')),
                ('DC1', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Do you think that the quality of the student assessment submissions is reasonable considering the students participation and module&#39;s level?')),
                ('DC2', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Is the writing style used in the supplied documents overly sophisticated, with minimal evidence of the depth of the study?')),
                ('DC3', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Is the level of the English writing in the submitted documents significantly better than the quality of the English used by the student in emails, in-class discussions, and other forms of communication?')),
                ('DC4', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Is the students submission generic in nature, failing to address the assignments key focus points?')),
                ('DC5', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Are there inappropriate replacements of vocabulary in the work that suggests an attempt to make it plagiarism free?')),
                ('DC6', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NA', 'NA')], default='NA', max_length=5, verbose_name='Are there any indications on the students documents that show the involvement of a third?')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.subject')),
            ],
        ),
    ]