# Generated by Django 3.2.10 on 2022-03-10 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translator', '0002_auto_20220219_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='images/contributors')),
            ],
            options={
                'verbose_name': 'Contributor',
                'verbose_name_plural': 'Contributors',
            },
        ),
        migrations.AlterField(
            model_name='translator',
            name='destination_language',
            field=models.CharField(choices=[('fr', 'French'), ('en', 'English')], max_length=5),
        ),
        migrations.AlterField(
            model_name='translator',
            name='source_language',
            field=models.CharField(choices=[('fr', 'French'), ('en', 'English')], max_length=5),
        ),
    ]
