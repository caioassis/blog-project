# Generated by Django 2.2.8 on 2019-12-23 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20191223_1120'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reply',
            options={'ordering': ['-created_at', '-approved'], 'verbose_name': 'Reply', 'verbose_name_plural': 'Replies'},
        ),
    ]
