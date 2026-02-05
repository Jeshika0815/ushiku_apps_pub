from django.db import models

class WorkOrder(models.Model):
    # TypeA・TypeB選択
    work_sp_choices = [
        ('TypeA','TypeA'),
        ('TypeB','TypeB'),
    ]
    # 製作グループ選択
    work_groups = [
        ('東京工場','東京工場'),
        ('横浜工場','横浜工場'),
        ('その他','その他'),
    ]


    work_order_number = models.PositiveIntegerField("作業注文票番号", unique=True)  # 7桁の整数
    release_date = models.DateField("発行日", auto_now_add=True)
    work_number = models.CharField("工番", max_length=4)  # 英数字4文字
    subject = models.CharField("件名", max_length=20)  # 漢字20文字
    manager = models.CharField("製造管理担当者", max_length=16)  # 漢字16文字
    work_group = models.CharField('製作グループ', max_length=10, choices=work_groups, default="東京工場") # 漢字10文字
    work_hours = models.DecimalField("作業工数時間", max_digits=5, decimal_places=1)  # 小数点以下5桁(25.11.23更新)
    next_process = models.CharField("次工程", max_length=20)  # 漢字20文字
    start_date = models.DateField("作業開始日", default="2021/01/01")
    end_date = models.DateField("終了予定日", default="2021/01/10")
    work_type = models.CharField('', max_length=2, choices=work_sp_choices, default="TypeA")
    work_range = models.CharField('作業範囲', max_length=200, default="")
    planed_value = models.DecimalField('計画数', max_digits=3, decimal_places=0, default="")
    syounin_check = models.CharField('承認', max_length=30, default="", blank=True)
    publish_check = models.CharField('作成', max_length=30, default="", blank=True)
    workset_check = models.CharField('工数設定', max_length=30, default="", blank=True)
    buy_check = models.CharField('購買確認', max_length=30, default="", blank=True)
    recive_check = models.CharField('受理', max_length=30, default="", blank=True)
    

    def __str__(self):
        return f"{self.work_order_number} - {self.subject}"

    class Meta:
        verbose_name = "作業注文票"
        verbose_name_plural = "作業注文票"

class WorkOrderProgress(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name="progresses")
    work_date = models.DateField("作業日", blank=True)
    achievement = models.DecimalField("進捗（％）", max_digits=3, decimal_places=0, default=0, blank=True)
    daily_result = models.DecimalField("当日実績", max_digits=2, decimal_places=0, blank=True)

    def __str__(self):
        return f"{self.work_order} - {self.work_date}"
        

    class Meta:
        verbose_name = "作業進捗"
        verbose_name_plural = "作業進捗"

