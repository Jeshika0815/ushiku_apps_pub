from django import forms
from django.forms.models import inlineformset_factory
from .models import WorkOrder, WorkOrderProgress

class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = [
            'work_order_number', 'work_number', 'subject', 
            'manager', 'work_group', 'work_hours', 
            'next_process', 'start_date', 'end_date', 'work_type', 'work_range', 'planed_value',
            'syounin_check', 'publish_check', 'workset_check', 'buy_check', 'recive_check',
        ]
        labels = {
            'work_order_number': '作業指示票番号(必)',
            'work_number': '工番(必)',
            'subject': '件名(必)',
            'manager': '製造管理担当者(必)',
            'work_group': '製作グループ(必)',
            'work_hours': '作業工数時間(必)',
            'next_process': '次工程(必)',
            'start_date': '作業開始日(必)',
            'end_date': '終了予定日(必)',
            'work_range': '作業範囲(必)',
            'planed_value': '計画数(必)',
            'syounin_check': '承認',
            'publish_check': '作成',
            'workset_check': '工数設定',
            'buy_check': '購買確認',
            'recive_check': '受け取り確認',
        }
        widgets = {
            'work_type': forms.RadioSelect(),
            'start_date': forms.TextInput(attrs={'type': 'date'}),
            'end_date': forms.TextInput(attrs={'type': 'date'}),
            'work_range': forms.Textarea(attrs={'resize':'none'}),
            'work_order_number' : forms.TextInput(attrs={'class': 'sel'}),
            'work_hours' : forms.TextInput(attrs={'class':'sel'}),
        }




# 作業進捗用のフォームデータセット
WorkOrderProgressFormSet = inlineformset_factory(
    WorkOrder, WorkOrderProgress,
    fields=('work_date', 'achievement', 'daily_result', ),
    widgets={
        'work_date': forms.TextInput(attrs={'type': 'date','class':'wop_width'}),
    },
    extra=12,  # 12個分のフォームを表示
    max_num=12,
    can_delete=False
)
