from django.db import models


class Node(models.Model):
    # 上线的节点列表

    INVALID = '0'
    VALID = '1'
    BAN = '2'

    STATUS_CHOICE = [
        (INVALID, "不可用"),
        (VALID, "可用"),
        (BAN, "禁用")
    ]


    category = models.IntegerField("应用", null=False)
    domain = models.IntegerField("业务", null=False)

    hostname = models.CharField("地址", max_length=128, null=False)
    label = models.CharField("标签", max_length=64, null=False)

    cpu = models.FloatField("CPU", default=0.0)
    disk = models.FloatField("DISK", default=0.0)
    memory = models.FloatField("MEM", default=0.0)

    #enabled = models.IntegerField("状态", null=False, default=0)
    enabled = models.CharField("状态", max_length=2, choices=STATUS_CHOICE, default=INVALID)

    alive_account_count = models.IntegerField("可用账号", default=0)
    pending_task_count = models.IntegerField("待执行任务", default=0)

    accounts = models.TextField("账号统计详情", blank=True, null=True)
    tasks = models.TextField("任务统计详情", blank=True, null=True)

    updated_ts = models.IntegerField("更新时间", default=0)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "online_machine"
        verbose_name = "节点"
        verbose_name_plural = "节点"

    def __str__(self):
        return f"C{self.category} - D{self.domain} - {self.label} - {self.hostname}"