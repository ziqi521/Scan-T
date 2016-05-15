#!/usr/bin/python
#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
import datetime
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from nmaptoolbackground.control import usercontrol,jobcontrol,ipcontrol,portcontrol,taskcontrol
from django.views import generic
from spidertool import webtool


import json


                
def indexpage(request):
    username = request.COOKIES.get('username','')
    return render_to_response('fontsearchview/search.html', {'data':'','username':username})
def mainpage(request):
    content=request.GET.get('searchcontent','')
    page=request.GET.get('page','0')
    username = request.COOKIES.get('username','')
    return render_to_response('fontsearchview/searchdetail.html', {'data':content,'page':page,'username':username})
def detailpage(request):
    content=request.POST.get('content','')
    page=request.POST.get('page','0')
    username = request.COOKIES.get('username','')
    response_data = {}  
    response_data['result'] = '0'
    if  content!='':
        extra='   left join ip_maindata on snifferdata.ip=ip_maindata.ip  where     match(snifferdata.ip,portnumber,version,snifferdata.state,name,product,timesearch,head,detail,script) against(\''+content+'\' in Boolean mode)  '
       
#         extra='    or   script  like \'%'+content+'%\' or detail  like \'%'+content+'%\'  or timesearch like ' +'\'%'+content+'%\' or head like \'%' +content+'%\') and  snifferdata.ip=ip_maindata.ip '
#         ports,portcount,portpagecount=portcontrol.portabstractshow(ip=content,port=content,timesearch=content,state=content,name=content,product=content,version=content,page=page,extra=extra,command='or')
        ports,portcount,portpagecount=portcontrol.portabstractshow(page=page,extra=extra,command='or')

        response_data['result'] = '1' 
    
    
        response_data['ports']=ports
        response_data['portslength']=portcount
        response_data['portspagecount']=portpagecount
        response_data['portspage']=page
        response_data['username']=username
    return HttpResponse(json.dumps(response_data,skipkeys=True,default=webtool.object2dict), content_type="application/json")  
    
    
    

  