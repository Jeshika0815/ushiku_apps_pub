from django import forms
from .models import WorkLog
from work_orders.models import WorkOrder

class WorkLogForm(forms.ModelForm):
    work_number = forms.ChoiceField(
        label='工番',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    subject = forms.ChoiceField(
        required=False,
        label='件名',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['work_number'].choices = [('', '---------')] + [
            (wn, wn) for wn in WorkOrder.objects
            .filter(work_number__isnull=False)
            .values_list('work_number', flat=True)
            .distinct()
            .order_by('-release_date','work_number')
        ]
        self.fields['work_trenum'].choices = [('', '---------')] + [
            (work_trenum, work_trenum) for work_trenum in WorkOrder.objects
            .filter(work_trenum__isnull=False, work_number__isnull=False)
            .values_list('work_trenum', flat=True)
            .distinct()
            .order_by('-release_date')
        ]
        self.fields['subject'].choices = [('', '---------')] + [
            (sbj,sbj) for sbj in WorkOrder.objects
            .filter(subject__isnull=False)
            .values_list('subject', flat=True)
            .distinct()
            .order_by('subject')
        ]

    class Meta:
        model = WorkLog
        fields = ['date', 'work_number', 'subject','work_content' , 'work_hours', 'work_minute']
        labels = {
            'date': '作業日',
            'work_number': '工番',
            'subject': '件名',
            'work_content': '作業内容',
            'work_hours': '時間',
            'work_minute': '分',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # HTML5の日付入力ウィジェット
            'work_hours': forms.NumberInput(attrs={'min':'0','max':'23'}),
            'work_minute': forms.NumberInput(attrs={'step': '10', 'min':'0', 'max':'50'}),
        }

class Csv_Settings(forms.Form):
    start_date = forms.DateField(label='開始日* ',required=True, widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(label='終了日',required=False, widget=forms.DateInput(attrs={'type':'date'}))



        