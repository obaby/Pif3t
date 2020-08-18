# Generated by Django 3.1 on 2020-08-18 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifdata', '0003_ifthis_response_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ifthis',
            name='response_text',
        ),
        migrations.AddField(
            model_name='ifthis',
            name='no_action_response_text',
            field=models.TextField(blank=True, help_text='未绑定动作反馈文本 随机文本反馈使用 | 分割', null=True),
        ),
        migrations.AddField(
            model_name='thataction',
            name='response_text',
            field=models.TextField(blank=True, help_text='动作执行反馈文本 随机文本反馈使用 | 分割', null=True),
        ),
    ]