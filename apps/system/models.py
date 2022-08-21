import datetime
import hashlib
import os

from django.db import models

# Create your models here.



class Cat(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    name = models.CharField(max_length=64, verbose_name="猫咪名称", help_text="猫咪名称")
    birthday = models.DateField(null=True, help_text="出生日期", verbose_name="出生日期")
    avatar = models.CharField(max_length=255, null=True, help_text="头像", verbose_name="头像")
    GENDER_CHOICES = ((0, "公"), (1, '母'))
    gender = models.IntegerField(choices=GENDER_CHOICES, help_text="性别", verbose_name="性别")

    class Meta:
        db_table = "cat"
        verbose_name = "猫咪信息"
        verbose_name_plural = verbose_name
        ordering = ['id']


class Weight(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    date = models.DateField(null=True, blank=True, help_text="记录体重时间", verbose_name="记录体重时间")
    weight = models.FloatField(help_text="体重", verbose_name="体重")
    cat = models.ForeignKey(to=Cat, related_name="wg", on_delete=models.DO_NOTHING, help_text="体重关联的猫咪", verbose_name="体重关联的猫咪")

    class Meta:
        db_table = "weight"
        verbose_name = "猫咪体重"
        verbose_name_plural = verbose_name
        ordering = ['date']

class Daily(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    PRIORITY_CHOICES = ((0, "日常"), (1, '重要'))
    priority = models.IntegerField(choices=PRIORITY_CHOICES, help_text="优先级", verbose_name="优先级")
    title = models.TextField(verbose_name="标题", help_text="标题")
    remark = models.TextField(verbose_name="备注", help_text="备注", null=True, blank=True)
    cat = models.ForeignKey(to=Cat, related_name="daily_wg", on_delete=models.DO_NOTHING, help_text="关联的猫咪", verbose_name="关联的猫咪")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间", verbose_name="创建时间")

    class Meta:
        db_table = "daily"
        verbose_name = "猫咪日常"
        verbose_name_plural = verbose_name
        ordering = ['id']

def media_file_name(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join("files", h[0:1], h[1:2], h + ext.lower())

class FileList(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间", verbose_name="创建时间")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="名称", help_text="名称")
    url = models.FileField(upload_to=media_file_name)
    md5sum = models.CharField(max_length=36, blank=True, verbose_name="文件md5", help_text="文件md5")

    def save(self, *args, **kwargs):
        if not self.md5sum:
            md5 = hashlib.md5()
            for chunk in self.url.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "file_list"
        verbose_name = "文件管理"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)
