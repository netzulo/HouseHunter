# Generated by Django 2.1.3 on 2018-11-26 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='UNNAMED', help_text='Just a name for your control configuration', max_length=20, unique=True)),
                ('selector', models.TextField(help_text='Just a selector to use for obtain some web element', max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ControlInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='ControlBase', help_text='Name type for this control', max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='UNNAMED', help_text='Just a name for your page configuration', max_length=20, unique=True)),
                ('url', models.TextField(default='about:blank', help_text="Url for your page configuration, by default='about:blank'", max_length=1024)),
                ('locator', models.TextField(default='css selector', help_text='Selenium selectors strategy', max_length=25)),
                ('go_url', models.BooleanField(default=False, help_text='Allows to go to page url before load elements')),
                ('wait_url', models.IntegerField(default=0, help_text='Wait for and url before starting to search elements')),
                ('maximize', models.BooleanField(default=False, help_text='Allows to maximize browser window')),
            ],
        ),
        migrations.DeleteModel(
            name='Name',
        ),
        migrations.AddField(
            model_name='control',
            name='instance_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.ControlInstance'),
        ),
    ]
