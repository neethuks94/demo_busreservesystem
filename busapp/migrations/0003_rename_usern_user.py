# Generated by Django 5.0.2 on 2024-03-14 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('busapp', '0002_rename_user_usern_alter_book_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Usern',
            new_name='User',
        ),
    ]
