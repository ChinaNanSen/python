from django.http import HttpResponse
 
from TestModel.models import Test
 
# 数据库操作
def testdb(request):
    test1 = Test(name='zzn')
    test1.save()
    test2 = Test(age=20)
    test2.save()
    test3 = Test(sex="男")
    test3.save()
    test4 = Test(bank="IT")
    test4.save()
    return HttpResponse("<p>数据添加成功！</p>")