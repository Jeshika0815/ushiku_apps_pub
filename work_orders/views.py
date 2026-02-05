# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import transaction
from collections import defaultdict
import csv
import datetime
from .forms import WorkOrderForm, WorkOrderProgressFormSet
from .models import WorkOrder, WorkOrderProgress
from daily_report.models import WorkLog
from django.db.models import Sum


# view the 作業注文票一覧
@login_required
def work_order_list(request):
    work_ordersx = WorkOrder.objects.all().order_by('-release_date')
    w_psum = wprogress_all()
    for order in work_ordersx:
        order.progress_rate = w_psum.get(order.id,0)

    wo_count = work_ordersx.count()
    if not work_ordersx.exists():
        return render(request, 'work_orders/work_order_list.html', {'woerror': '作業注文票のデータが存在しません。登録してください。'})
    return render(request, 'work_orders/work_order_list.html', {'work_orders': work_ordersx, 'wo_count':wo_count, 'work_progress':w_psum})


# 削除機能のビュー
@login_required
def delete_work_order(request, pk):
    work_order = get_object_or_404(WorkOrder, pk=pk)
    if request.method == "POST":
        work_order.delete()
        return redirect('work_orders:work_order_list')
    return render(request, 'work_orders/delete_work_order.html', {'work_order': work_order})

# view the 作業指示票登録
@login_required
def register_work_order(request):
    if request.method == 'POST':
        form = WorkOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('work_orders:work_order_list')
    else:
        form = WorkOrderForm()
    return render(request, 'work_orders/register_work_order.html', {'form': form})

# view the 作業指示票修正
@login_required
def edit_work_order(request, pk):
    # 修正する作業指示票を取得
    work_order = get_object_or_404(WorkOrder, pk=pk)
    
    if request.method == 'POST':
        form = WorkOrderForm(request.POST, instance=work_order)
        formset = WorkOrderProgressFormSet(request.POST, instance=work_order)
        if form.is_valid() and formset.is_valid():
            form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                # 必要なフィールドが適切に入力されているか確認
                if instance.daily_result is not None and instance.work_date :
                    instance.save()
            # 削除が選択されたインスタンスを削除
            for instance in formset.deleted_objects:
                instance.delete()
            calc_prate(work_order.id) #作業進捗率を自動で保存
            return redirect('work_orders:work_order_list')
    else:
        form = WorkOrderForm(instance=work_order)
        formset = WorkOrderProgressFormSet(instance=work_order)
    
    return render(request, 'work_orders/edit_work_order.html', {'form': form, 'formset': formset, 'work_order': work_order})

# view the 作業注文票詳細
@login_required
def work_order_detail(request, pk):
    # 指定された作業注文票とその進捗データを取得
    work_order = get_object_or_404(WorkOrder, pk=pk)
    work_orders= WorkOrderProgress.objects.filter(work_order=work_order)  # 関連する進捗データを取得
    w_psum = wprogress_all()
    
    work_order.progress_rate = w_psum.get(work_order.id,0)# 各注文における進捗率合計

    return render(request, 'work_orders/work_order_detail.html', {
        'work_order': work_order,
        'work_orders': work_orders,
        'work_progress': w_psum,
    })

#CSV and PDF download support

@login_required
def export_work_orders_csv(request):
    from urllib.parse import quote
    # CSVレスポンス設定
    filename = f"作業注文票 - {datetime.datetime.now().strftime('%Y%m%d')}.csv"
    encoded_fname = quote(filename) # URL encode
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f"attachment; filename*=UTF-8\'\'{encoded_fname}"

    # Shift-JIS エンコーディング
    response.write(u'\ufeff'.encode('utf-8-sig'))  # BOM追加（Excel対応）
    writer = csv.writer(response)
    # ヘッダー行
    writer.writerow([
        '作業注文票番号', '工番', '件名', '製造管理担当者',
        '作業工数時間', '次工程', '作業開始日', '終了予定日'
    ])

    # 作業注文票データを取得してCSVに書き込む
    work_orders_list = WorkOrder.objects.all()
    for orders in work_orders_list:
        writer.writerow([
            orders.id,
            orders.work_number,
            orders.subject,
            orders.manager,
            orders.work_hours,
            orders.next_process,
            orders.start_date,
            orders.end_date,
        ])

    return response


@login_required
def export_workorderprogress_csv(request):
    from urllib.parse import quote
    # CSVレスポンス設定
    filename = f"全体の作業進捗 - {datetime.datetime.now().strftime('%Y%m%d')}.csv"
    encoded_fname = quote(filename)
    response = HttpResponse(content_type='text/csv; charset=shift_jis')
    response['Content-Disposition'] = f"attachment; filename*=UTF-8\'\'{encoded_fname}"

    writer = csv.writer(response, quoting=csv.QUOTE_MINIMAL)

    # ヘッダー行
    writer.writerow([
        '進捗ID', '作業注文票番号', '作業日', '進捗（％）', '当日実績'
    ])

    # データ行
    progress_list = WorkOrderProgress.objects.select_related('work_order').all()
    for progress in progress_list:
        writer.writerow([
            progress.id,
            progress.work_order.work_order_number if progress.work_order else 'なし',
            progress.work_date.strftime('%Y-%m-%d'),
            progress.achievement,
            progress.daily_result,
        ])

    return response

# 作業進捗率の計算
def calc_prate(work_order_id):
    progress_data = WorkOrderProgress.objects.filter(work_order_id=work_order_id)
    with transaction.atomic():
        for progress in progress_data:
            # 作業注文票の計画値を取得
            work_order = progress.work_order
            if work_order:
                planed_value = work_order.planed_value
                # 作業進捗率を計算
                if planed_value > 0:
                    progress_rate = (progress.daily_result / planed_value) * 100
                    rounded_rate = round(progress_rate, 2)
                    if progress.achievement != rounded_rate:
                        progress.achievement = rounded_rate
                        progress.save()
                else:
                    if progress.achievement != 0:
                        # 計画値が0の場合、進捗率を0にリセット
                        progress.achievement = 0
                        progress.save()

# 作業進捗の合計の計算
def wprogress_all():
    progress_totals = defaultdict(float)
    progress_all = WorkOrderProgress.objects.values('work_order_id').annotate(total_pall=Sum('achievement'))
    
    
    for progress in progress_all:
        worder_id = progress['work_order_id']
        total_pall = float(progress['total_pall'] or 0)
        progress_totals[worder_id] += round(total_pall, 2)
    
    return dict(progress_totals)


