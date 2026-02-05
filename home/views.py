from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from django.http import HttpResponseForbidden
from daily_report.models import WorkLog
from work_orders.models import WorkOrder, WorkOrderProgress
from daily_report.forms import WorkLogForm
from django.db.models import Sum
from work_orders.views import wprogress_all

import os

from django.contrib.auth.views import LogoutView
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        """GET リクエストでもログアウトを許可"""
        return self.post(request, *args, **kwargs)

#　ダッシュボードを表示する関数    
@login_required
def home(request):
    try:
        employee = request.user.employee
    except employee.DoesNotExist:
        return HttpResponseForbidden('このユーザーには対応する従業員情報がありません。管理者に問い合わせてください。')
    
    work_orders = WorkOrder.objects.all()

    w_psum = wprogress_all()
    for order in work_orders:
        order.progress_rate = w_psum.get(order.id,0)

    work_order_count = work_orders.count()
    return render(request, 'home/dashboard.html', {'work_orders': work_orders, 'work_order_count':work_order_count,'work_progress': w_psum})

# ユーザプロフィールを表示
@login_required
def user_profile(request):
    try:
        employee = request.user.employee
    except employee.DoesNotExist:
        return HttpResponseForbidden('このユーザーには対応する従業員情報がありません。管理者に問い合わせてください。')
    wlog = WorkLog.objects.filter(employee=employee).order_by('-date')
    return render(request, 'home/users.html',{'work_log':wlog})

# ユーザのデータCSV出力
import csv
from django.http import HttpResponse
@login_required
def export_user_data_csv(request):
    from urllib.parse import quote
    import datetime
    # CSVレスポンス設定
    filename = f"Ushiku 社員IDリスト - {datetime.datetime.now().strftime('%Y%m%d')}.csv"
    encoded_fname = quote(filename)
    response = HttpResponse(content_type='text/csv; charset=shift_jis')
    response['Content-Disposition'] = f"attachment; filename*=UTF-8\'\'{encoded_fname}"

    # Shift-JIS でエンコードされた CSV データを生成
    writer = csv.writer(response, quoting=csv.QUOTE_MINIMAL)

    # ヘッダー行（日本語）
    header = ['データベースID', '社員氏名', '社員ID', '部類', 'メールアドレス', '登録日', '最終ログイン']
    response.write(",".join(header).encode('shift_jis') + b"\r\n")

    # データ行
    user_data = User.objects.all()
    for usr in user_data:
        row = [
            str(items)

            for items in [
            usr.id,
            usr.first_name+usr.last_name,
            usr.username,
            e_csv_judge_umode(request),
            usr.email,
            usr.date_joined.strftime('%Y-%m-%d'),
            usr.last_login.strftime('%Y-%m-%d') if usr.last_login else 'ログイン履歴なし'
            ]
        ]
        response.write(",".join(row).encode('shift_jis') + b"\r\n")

    return response

def e_csv_judge_umode(request):
    if request.user.is_superuser:
        return "管理者"
    else:
        return "社員・パート"