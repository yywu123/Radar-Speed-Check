from datetime import datetime

from django.shortcuts import render, redirect
from .forms import ItemForm, TimeSheetForm
from .models import TimeSheet, CheckItem

# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator


import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa





def render_pdf_view(request, pk):
    item = CheckItem.objects.get(id=pk)
    detail = TimeSheet.objects.filter(item=pk)

    content = {'item': item, 'details': detail}

    template_path = 'print_PDF.html'

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(content)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def render_pdf(request, pk):
    path =  'print_PDF.html'
    item = CheckItem.objects.get(id=pk)
    detail = TimeSheet.objects.filter(item=pk)

    content = {'item': item, 'details': detail}


    html = render_to_string(path, content)
    io_bytes = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)

    if not pdf.err:
        return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error while rendering PDF", status=400)


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


    item_num = request.GET.get('item_num')
    initial_data = {
        'item' : CheckItem.objects.get(id=item_num),
        'time' : datetime.now()
    }

    if request.method == 'POST':
        form = TimeSheetForm(request.POST)
        item_num = request.GET.get('item_num')
        print(item_num)
        if form.is_valid():
            form.save()
            url = '/detail/{}/'.format(item_num)
            return redirect(url)

    form = TimeSheetForm(initial=initial_data)
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


def printPDF(request, pk ):
    item = CheckItem.objects.get(id=pk)
    detail = TimeSheet.objects.filter(item=pk)
    content = {'item': item, 'details': detail }




    return render(request,'print_PDF.html', content)
