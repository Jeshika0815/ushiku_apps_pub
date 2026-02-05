from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from work_orders.models import WorkOrder
from .models import Employee

@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance, employee_number=instance.username, name=instance.username)

@receiver(post_save, sender=WorkOrder)
def update_work_order(sender, instance, created, **kwargs):
    if hasattr(instance, '_already_updated'):
        return

    instance.work_number = instance.work_number or 'NAN'
    instance.work_trenum = instance.work_trenum or '000'
    instance.subject = instance.subject or '不明な件名'
    instance._already_updated = True # Avoid infinite recursion
    instance.save()