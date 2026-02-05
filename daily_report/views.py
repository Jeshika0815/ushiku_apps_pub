from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib import messages
from django.utils.timezone import now, timedelta
from django.db.models import Sum
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponseForbidden
from collections import defaultdict
from work_orders.models import WorkOrder
from .models import WorkLog
from .forms import WorkLogForm, Csv_Settings
import datetime
from django.db.models import Prefetch
from itertools import groupby
from operator import itemgetter
import json


from django.contrib.auth.views import LogoutView
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        """GET リクエストでもログアウトを許可"""
        return self.post(request, *args, **kwargs)

@login_required
def work_logs(request):
    # 従業員情報の取得
    try:
        employee = request.user.employee
    except employee.DoesNotExist:
        return HttpResponseForbidden("このユーザーには対応する従業員情報がありません。管理者に問い合わせてください。")
    
    # 日付範囲の指定
    initial_date = now().date()
    selected_date_str = request.GET.get('selected_date', datetime.datetime.now().strftime('%Y-%m-%d'))
    if selected_date_str:
        try:
            selected_date = datetime.datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = initial_date

    else:
        selected_date = initial_date


    start_date = selected_date
    end_date = start_date + timedelta(days=7)
        
    # 作業日報を日付順に取得
    work_logs = WorkLog.objects.select_related('employee').filter(employee=employee,date__range=(start_date,end_date)).order_by('date','employee__name')
    awork_logs = WorkLog.objects.filter(employee=employee, date__range=(start_date,end_date)).order_by('date')
    
    # 作業時間の自動計算
    total_hours,remining_minutes = calc_p_wlogs(work_logs)

    # 作業日報個数表示
    count_logs = work_logs.count()
    
    # 個人の作業日報の取得
    an_work_log = WorkLog.objects.filter(employee=employee).order_by('-date') 
    
    # テンプレートで返す変数群
    context = {
        'work_logs': awork_logs,
        'work_log':an_work_log,
        'total_hours': total_hours,
        'remining_minutes': remining_minutes,
        'cout_logs': count_logs,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'daily_report/view_wlogs.html', context)

# 作業日報集計
@login_required
def log_totals(request):
    selected_date = request.GET.get('date') or str(datetime.date.today()) 

    try:
        target_date = datetime.date.fromisoformat(selected_date)
    except ValueError:
        target_date = datetime.date.today()

    summary = totaling(target_date)
    context = {
        'selected_date':target_date,
        'count_logss':summary['count_logss'],
        'total_hours': summary['total_hours'],
        'total_minute': summary['total_minute'],
        'order_summary': summary['onum_summary']
    }
    
    return render(request , 'daily_report/view_totals.html', context)

# 作業日報登録
@login_required
def log_work(request):
    work_orders = WorkOrder.objects.all().order_by('-release_date')
    if request.method == "POST":
        form = WorkLogForm(request.POST)
        if form.is_valid():
            work_log = form.save(commit=False)
            work_log.employee = request.user.employee  # ログイン中の従業員を紐付け
            work_log.save()
            return redirect('daily_report:work_logs')
    else:
        form = WorkLogForm()
    return render(request, 'daily_report/log_work.html', {'form': form, 'work_orders':work_orders})

# 作業日報修正
@login_required
def edit_work_log(request, pk):
    work_orders = WorkOrder.objects.all().order_by('-release_date')
    work_log = get_object_or_404(WorkLog, pk=pk, employee=request.user.employee)
    if request.method == "POST":
        form = WorkLogForm(request.POST, instance=work_log)
        if form.is_valid():

            form.save()
            return redirect('daily_report:work_logs')
    else:
        form = WorkLogForm(instance=work_log)
    return render(request, 'daily_report/edit_work_log.html', {'form': form, 'work_orders':work_orders})

# スタッフ権限で作業日報を修正・削除できる
# 編集ビュー
@login_required
@staff_member_required
def staff_edit_log(request, pk):
    work_log = get_object_or_404(WorkLog, pk=pk)
    if request.method == "POST":
        form = WorkLogForm(request.POST, instance=work_log)
        if form.is_valid():
            form.save()
            return redirect('daily_report:all-logs')
    else:
        form = WorkLogForm(instance = work_log)        
            
    reta = {'form':form, 'work_log':work_log}
    return render(request, 'daily_report/edit_wlog_st.html', reta)

# 削除ビュー   
@login_required
@staff_member_required
def delete_work_logs(request, pk):
    work_logs = get_object_or_404(WorkLog, pk=pk)
    if request.method == "POST":
        work_logs.delete()
        return redirect('daily_report:all-logs')
    return render(request, 'daily_report/logs_delete.html', {'work_logs': work_logs})

#全体の作業日報のテーブル出力
@login_required
def all_logs(request):
        
    selected_date_str = request.GET.get('selected_date', datetime.datetime.now().strftime('%Y-%m-%d'))
    if selected_date_str:
        selected_date = datetime.datetime.strptime(selected_date_str, '%Y-%m-%d').date() 
    else:
        selected_date = datetime.date.today()    
    # 全ての作業日報を取得
    filtered_log = WorkLog.objects.select_related('employee').filter(date=selected_date).order_by('date', 'employee__name')
    
    work_log = WorkLog.objects.select_related('employee').order_by('-date', 'employee__name')
    # 存在する日数のカウント
    wl_count = work_log.count()
    wls_count = filtered_log.count()

    #CSV出力関連
    csv_set = ExportCSV()
    cform = Csv_Settings(request.POST)
    if request.method == 'POST':
        cform = Csv_Settings(request.POST)
        if cform.is_valid():
            start_date = cform.cleaned_data['start_date']
            end_date = cform.cleaned_data['end_date']
            log_data = csv_set.get_datas(start_date,end_date)
            request.session['log_data'] = json.dumps(log_data, default=str)
            
            key_arg={
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d') if end_date else 'none'
            }
                
            url = reverse("daily_report:export_work_logs_csv", kwargs=key_arg)
            return redirect(url)
    else:
        cform = Csv_Settings()

    # テンプレートに返す値
    context = {
               'form': cform,
               'work_log':work_log,
               'wl_count':wl_count,
               'selected_date':selected_date,
               'filtered_log':filtered_log,
               'wls_count': wls_count
              }
    return render(request, 'daily_report/all_wlogs.html', context)

#for CSV download
import csv
from django.http import HttpResponse
from .models import WorkLog
from urllib.parse import quote

@login_required
def export_work_logs_csv(request,start_date,end_date):
    try:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = None if end_date == 'none' else datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    except (ValueError,TypeError):
        return HttpResponse("開始日が不正です。", status=400)
    # CSVレスポンス設定
    filename = f"{start_date}_{end_date or '以降'}の作業日報 - {datetime.datetime.now().strftime('%Y%m%d')}.csv"
    encoded_fname = quote(filename.encode('utf-8'))
    response = HttpResponse(content_type='text/csv; charset=shift_jis')
    response['Content-Disposition'] = f"attachment; filename*=UTF-8\'\'{encoded_fname}"

    # Shift-JIS でエンコードされた CSV データを生成
    writer = csv.writer(response, quoting=csv.QUOTE_MINIMAL)

    # ヘッダー行（日本語）
    header = ['従業員名', '工番', '件名', '作業コード', '作業時間(時間)', '作業時間(分)', '作業日']
    response.write(",".join(header).encode('shift_jis') + b"\r\n")

    log_datas = request.session.get('log_data')
    if not log_datas:
        return HttpResponse("セッションにデータがありません。", status=400)
    # データ行
    work_logs = json.loads(log_datas)
    for log in work_logs:
        writer.writerow ([
            
            log['employee__name'],
            log['work_number'],
            log['work_trenum'],
            log['subject'],
            log['work_code'],
            log['work_hours'],
            log['work_minute'],
            log['date']
            
        ])

    return response

# その他関数

# 個人の作業時間計算周り
def calc_p_wlogs(work_logs):
    # work_hours and work_minutes
    total_work_hours = work_logs.aggregate(total_hours=Sum('work_hours'),total_minute=Sum('work_minute'))

    # calucration of total work hours
    total_hours = total_work_hours['total_hours'] or 0
    total_minute = total_work_hours['total_minute'] or 0
    total_hours += total_minute // 60
    remining_minutes = total_minute % 60

    return total_hours, remining_minutes

# 作業日報集計・工番とその中に枝番ごとにグループ化
def totaling(target_date):
    logs = WorkLog.objects.filter(date=target_date) #作業伝票を取得
    # 作業日報個数表示
    count_logss = logs.count()

    #合計時間計算
    total_minutes = sum(log.work_hours * 60 + log.work_minute for log in logs)
    total_hours = total_minutes // 60 
    total_minute = total_minutes % 60 
    
    # 工番ごとの集計データを保持する辞書
    onum_summary = defaultdict(lambda: {'total_hours':0, 'total_minute':0, 'trenum_details':[], 'trenum_group':set(), 'subject':set()}) #工番ごとの_合計

    # 工番ごとの集計
    for log in logs:
        onum = log.work_number
        trenum_details = {
            'employee': log.employee,
            'work_hours': log.work_hours,
            'work_minute': log.work_minute
        }
        onum_summary[onum]['total_hours'] += log.work_hours
        onum_summary[onum]['total_minute'] += log.work_minute
        onum_summary[onum]['trenum_details'].append(trenum_details)
        onum_summary[onum]['trenum_group'].add(log.work_trenum)
        onum_summary[onum]['subject'].add(log.subject)

    # 必要に応じてセットをリストに変換
    for onum, summary in onum_summary.items():
        summary['trenum_group'] = list(summary['trenum_group'])
        summary['subject'] = ', '.join(summary['subject'])

        
    return {
        'count_logss': count_logss,
        'total_hours':total_hours,
        'total_minute':total_minute,
        'onum_summary':dict(onum_summary)
    }
    
# CSV出力の関数
class ExportCSV:
    def __init__(self):
        self.start_date = None
        self.end_date = None
        
    def get_datas(self,start_date,end_date=None):
        if start_date and end_date:
            logs = self.o_range_ldata(start_date,end_date)
        else:
            logs = self.o_all_ldata(start_date)
        log_data = list(logs.values(
            'employee__name',
            'work_number',
            'work_trenum',
            'subject',
            'work_code',
            'work_hours',
            'work_minute',
            'date'
        ))
        return log_data

    #最初の日付のみ入っていた場合、全体の伝票を出力する
    def o_all_ldata(self, start_date):
        return WorkLog.objects.select_related('employee').filter(date__gte=start_date)
        
    
    #開始日、終了日が入っている場合は、その範囲内のデータを取得する
    def o_range_ldata(self, start_date, end_date):
        return WorkLog.objects.select_related('employee').filter(date__range=[start_date,end_date])

    
    def check_date(self, dates):
        try:
            return datetime.datetime.strptime(dates,'%Y-%m-%d').date()
        except (ValueError,TypeError):
            return None
    