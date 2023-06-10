# Generated by Django 4.1.8 on 2023-06-06 01:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('auto_increment_id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('specialty', models.CharField(max_length=50)),
                ('registered', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-registered'],
                'unique_together': {('firstname', 'lastname')},
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('auto_increment_id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('join_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('appoint_time', models.DateTimeField()),
                ('patient_no', models.IntegerField(unique=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waitlist_patients', to='waitlist.doctor')),
            ],
            options={
                'ordering': ['join_time'],
                'unique_together': {('firstname', 'lastname')},
            },
        ),
    ]
