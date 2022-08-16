from django.shortcuts import render, redirect
from .forms import ItemForm, TimeSheetForm
from .models import TimeSheet, CheckItem

# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator


def home(request):
    item = CheckItem.objects.all()
    page_num = 6
    p = Paginator(item,page_num)
    page = request.GET.get('page')

    item_list = p.get_page(page)


    context = { 'item_list': item_list }

    return render(request, 'home.html', context)


def detail(request, pk):
    item = CheckItem.objects.get(id=pk)
    detail = TimeSheet.objects.filter(item=pk)
    page_num =6
    p = Paginator(detail, page_num)
    page = request.GET.get('page')
    detail_list = p.get_page(page)

    content = {'item': item, 'details': detail_list}



    return render(request, 'detail.html', content)


def createItem(request):
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')

    context = {'form': form}
    return render(request, 'checkItem_form.html', context)


def updateItem(request, pk):
    item = CheckItem.objects.get(id=pk)
    form = ItemForm(instance=item)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'checkItem_form.html', context)


def deleteItem(request, pk):
    item = CheckItem.objects.get(id=pk)
    if request.method =='POST':
        item.delete()
        return redirect('home')

    return render(request, 'delete.html')


def createTimeSheet(request):
    form = TimeSheetForm()

    if request.method == 'POST':
        form = TimeSheetForm(request.POST)
        item_num = request.GET.get('item_num')
        print(item_num)
        if form.is_valid():
            form.save()
            url = '/detail/{}/'.format(item_num)
            return redirect(url)


    context = {'form': form}
    return render(request, 'TimeSheet_form.html', context)

def updateTimeSheet(request, pk):
    item = TimeSheet.objects.get(id=pk)
    form = TimeSheetForm(instance=item)

    if request.method == 'POST':
        form = TimeSheetForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            url = '/detail/{}/'.format(item.item.id)
            return redirect(url)

    context = {'form': form}
    return render(request, 'TimeSheet_form.html', context)


def deleteTimeSheet(request, pk):
    item = TimeSheet.objects.get(id=pk)
    if request.method =='POST':
        item.delete()
        url = '/detail/{}/'.format(item.item.id)
        return redirect(url)

    return render(request, 'delete.html')


def base(request):

    return render(request,'base.html')



def detailView(request, pk):
    item = CheckItem.objects.get(id=pk)
    detail = TimeSheet.objects.filter(item=pk)
    page_num =10
    p = Paginator(detail, page_num)
    page = request.GET.get('page')
    detail_list = p.get_page(page)



    content = {'item': item, 'details': detail }



    return render(request, 'view_sheet.html', content)