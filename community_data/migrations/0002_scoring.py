# Generated by Django 2.0.5 on 2018-05-25 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scoring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_pulls', models.PositiveSmallIntegerField()),
                ('closed_pulls', models.PositiveSmallIntegerField()),
                ('open_issues', models.PositiveSmallIntegerField()),
                ('closed_issues', models.PositiveSmallIntegerField()),
                ('popularity', models.FloatField()),
                ('popularity_vs_issues', models.FloatField(null=True)),
                ('popularity_vs_contributors', models.FloatField()),
                ('closed_issues_per_day', models.FloatField(null=True)),
                ('popularity_vs_closed_issues_per_day', models.FloatField(null=True)),
                ('days_since_last_pr_merge', models.FloatField(null=True)),
                ('popularity_vs_days_since_last_pr_merge', models.FloatField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community_data.Project')),
            ],
        ),
    ]
