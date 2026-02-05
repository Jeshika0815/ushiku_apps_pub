from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Employee(models.Model):
    employee_number = models.CharField("従業員番号", max_length=10, unique=True)
    name = models.CharField("氏名", max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")

    def __str__(self):
        return self.name

class WorkLog(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="work_logs")
    work_number = models.CharField("工番", max_length=4)
    subject = models.CharField("件名", max_length=20)
    work_content = models.CharField("作業内容", max_length=100)
    work_hours = models.DecimalField("時間", max_digits=4, decimal_places=0, default="", validators=[MinValueValidator(0), MaxValueValidator(23)])
    work_minute = models.DecimalField("分", max_digits=2, decimal_places=0, default="", validators=[MinValueValidator(0), MaxValueValidator(59)])
    date = models.DateField("作業日", auto_now_add=False)

    def __str__(self):
        return f"{self.employee.name} - {self.work_number} ({self.date})"

