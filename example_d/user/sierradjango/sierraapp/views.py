import urllib
import requests
import json
import base64
import subprocess
import os
import time
import sys
sys.path.append('/home/damian/.local/lib/python3.8/site-packages/')
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from sierraapp.functions.hola_module import hola
from sierraapp.forms_upload import UPloadGIDREPORTForm
from sierraapp.forms_choose_me import ChooseMaskingEngineForm

def index(request):
  template = loader.get_template('myfirst.html')
  return HttpResponse(template.render())

def create_mj_view(request):
    if request.method == 'POST':
        qdict = request.GET
        localfilename = qdict['localfilename']
        fqengine = qdict['fqengine']
        sealid = qdict['sealid']
        uploaded_date_epoch = qdict['uploaded_date_epoch']
        response_dict = {'hola':'hola'}
        #response_dict = backend() 
        return HttpResponse(response_dict)
   

def upload_view(request):
    if request.method == 'POST':
        #this is django object, not a string
        file_to_upload_object = request.FILES['file']
        uploaded_date_epoch = str(time.time()).replace(".", "ms")
        kk = True 
        if kk == True:
            d = dict(upload="nada") 
            return JsonResponse(d, status=200)
        else:
            context = {'sealid': 'algo', 'uploaded_date_epoch': uploaded_date_epoch}
            another_url = "/choose_masking_engine/"
            return redirect(another_url + "?" + urllib.parse.urlencode(context))
    else:
        UPloadGIDREPORTForm_instance = UPloadGIDREPORTForm()
        return render(request, "upload_new_app.html", {'form':UPloadGIDREPORTForm_instance, 'uploaded_ok':False})

def choose_masking_engine_view(request):
    if request.method == 'GET':
        print(request.GET)
        qdict = request.GET
        context = {}
        for q in qdict.items():
            q_key = str(q[0])
            q_value = q[1]
            print("key: " + q_key + ", value: " + str(q_value))
            context[q_key] = q_value
        print("context now is: " + str(context))
        ChooseMaskingEngineForm_instance = ChooseMaskingEngineForm()
        return render(request, "choose_masking_engine.html", context)
    elif request.method == 'POST':
        ChooseMaskingEngineForm_instance = ChooseMaskingEngineForm(request.POST)

        if ChooseMaskingEngineForm_instance.is_valid():
            name_choices = ChooseMaskingEngineForm_instance.cleaned_data.get('name_choices')
            name_specific = ChooseMaskingEngineForm_instance.cleaned_data.get('name_specific')
            if name_specific != "NONE":
                fqengine = name_choices
            elif name_choices != "dynamically_assigned":
                fqengine = name_choices
            else:
                fqengine = name_choices
                fqengine = "vsie"

            qcict = request.GET
            localfilename = qdict['localfilename']
            sealid = qdict['sealid']
            uploaded_date_epoch = qdict['uploaded_date_epoch']
            context = {}
            context['localfilename'] = localfilename
            context['fqengine'] = fqengine
            context['sealid'] = sealid
            context['uploaded_date_epoch'] = uploaded_date_epoch
            another_url = "/create_mj"
            return redirect(another_url + "?" + urllib.parse.urlencode(context)) 

        else:
            qdict = request.GET
            context = {}
            for q in qdict.items():
                q_key = str(q[0])
                q_value = str(q[1])
                context[q_key] = q_value
            context['form'] = ChooseMaskingEngineForm_instance
            return render(request, "choose_masking_engine.html", context)

