#!/usr/bin/env python
import sys
H = {'1':'白石桥','2':'东直门','3':'复兴路'}
K = {'1':'灵石路','2':'宝山路','3':'康乐路'}
P = {'1':'和平路','2':'辽宁路','3':'新华路'}
J = {'1':'大井湾','2':'王家湾','3':'茅溪村'}
B = {'1':'海淀区','2':'朝阳区','3':'东城区','4':'西城区'}
S = {'1':'黄浦区','2':'虹口区','3':'长宁区','4':'徐汇区'}
T = {'1':'和平区','2':'河东区','3':'河北区','4':'河西区'}
C = {'1':'江北区','2':'长寿区','3':'荣昌区','4':'巴南区'}

City = {
    '1':'北京市',
    '2':'上海市',
    '3':'天津市',
    '4':'重庆市',
}
for k,v in City.items():
    print (k,v)
while True:
    print ('Q:退出')
    A = input('Please select：')
    if A == '1':
        for k,v in B.items():
          print (k,v)
        print ('Q:退出')
        G = input ('Please continue to choose:')
        if G == '1':
            for k,v in H.items():
                print (k,v)
        if G == 'Q':
            print ('Welcome to come again next time.')
            sys.exit()
    if A == '2':
       for k,v in S.items():
         print (k,v)
         print ('Q:退出')
       G = input ('Please continue to choose:')
       if G == '1':
            for k,v in K.items():
                print (k,v)
       if G == 'Q':
            print ('Welcome to come again next time.')
            sys.exit()
    if A == '3':
       for k,v in T.items():
         print (k,v)
       print ('Q:退出')
       G = input ('Please continue to choose:')
       if G == '1':
            for k,v in P.items():
                print (k,v)
       if G == 'Q':
            print ('Welcome to come again next time.')
            sys.exit()
    if A == '4':
       for k,v in C.items():
         print (k,v)
         print ('Q:退出')
       G = input ('Please continue to choose:')
       if G == '1':
            for k,v in J.items():
                print (k,v)
       if G == 'Q':
            print ('Welcome to come again next time.')
            sys.exit()
    if A == 'Q':
        print ('Welcome to come again next time.')
        sys.exit()
