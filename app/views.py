from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from django.views.decorators.csrf import ensure_csrf_cookie
import requests
import time

appId = "4b42316e4675476f433157593942644d43634646527663506670317977376237"
appSecret = "7544376f5179574a766a33464546327366655571747977336c644a50655543714a6f41436d436151596d614f5f4146326635584b62526339474b5a4f4a346d4f"
token = ''
jobid = ''
conversationid = ''
status = False
srt = ''
text = ''

def result_srt(request):
    url = f"https://api.symbl.ai/v1/conversations/{conversationid}/transcript"
    payload = {"contentType": "text/srt"}
    headers = {
            "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token,            
    }
    response = requests.post(url, json=payload, headers=headers)
    global srt
    srt = response.text
    filename = "my_file.txt"
    content = srt
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

def result_text(request):
    url = f"https://api.symbl.ai/v1/conversations/{conversationid}/messages?verbose=true&sentiment=true"

    headers = {
            "Accept": "application/json",
                    "Authorization": "Bearer " + token,            
    }

    response = requests.get(url, headers=headers)
    global text
    text = response.text
    filename = "my_file.txt"
    content = text
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


def check_status(request):
    url = f"https://api.symbl.ai/v1/job/{jobid}"
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + token               
    }

    response = requests.get(url, headers=headers)
    response = HttpResponse(response.text)
    return response

@ensure_csrf_cookie
def upload_display_video(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            file = request.FILES['file']
            url = "https://api.symbl.ai/oauth2/token:generate"

            headers = {
            "Content-Type": "application/json"
            }

            request_body = {
            "type": "application",
            "appId": appId,
            "appSecret": appSecret
            }

            response = requests.post(url, headers=headers, json=request_body)
            symblai_params = {
            "name": "Sample"
            }
            global token
            token = response.json()['accessToken']
            headers = {
            "Authorization": "Bearer " + response.json()['accessToken'],
            "Content-Type": "video/mp4"
            }

            request_body = file.read()

            response = requests.request(
            method="POST", 
            url="https://api.symbl.ai/v1/process/video",
            params=symblai_params,
            headers=headers,
            data=request_body
            )
            global conversationid
            global jobid
            conversationid = response.json()['conversationId']
            jobid = response.json()['jobId']
            url = f"https://api.symbl.ai/v1/job/{response.json()['jobId']}"

            headers = {
                "Accept": "application/json",
                "Authorization": "Bearer " + token,                 
                }

            response = requests.get(url, headers=headers)
            return render(request, 'build/index.html' , {"filename":response.text})
    else:
        form = UploadFileForm()
    return render(request, 'build/index.html' , {"filename":None})

def render_home(request):
    return render(request, 'build/index.html')
