# Generated by Django 3.0.14 on 2022-01-02 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, help_text='48px * 48px 크기의 파일을 업로드해주세요.', upload_to='accounts/profile/%Y/%m/%d'),
        ),
    ]
