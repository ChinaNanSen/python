from multiprocessing import context
from pydoc import render_doc
from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    return HttpResponse("hello world!!!666")

def test(request):
    context = ['111','222','打法','fff']
    return render(request,"runoob.html", {"context":context})

def cai(request):
  views_name =  {"name":"菜鸟教程","ak":99}
  return  render(request,"runoob.html", {"views_name":views_name})


def ubk(request):
    name = 'dsfsdfsd'
    num = 88
    return render(request,"runoob.html", {'num':num})