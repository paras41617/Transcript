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

def check_status(request):
    url = f"https://api.symbl.ai/v1/job/{jobid}"
    print("url : " , url)
    print("jobid : " , jobid)
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + token               
    }

    response = requests.get(url, headers=headers)
    print(response.json())
    print(response.text)
    if(response.json()['status'] == "completed"):
        status = True
        url = f"https://api.symbl.ai/v1/conversations/{conversationid}/transcript"
        payload = {"contentType": "text/srt"}
        headers = {
            "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token,            
        }
        response = requests.post(url, json=payload, headers=headers)
        print(response.json())
        print(response.text)
    return render(request, "index.html", {'filename': response.text})    


@ensure_csrf_cookie
def upload_display_video(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
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
            print(response.json()['expiresIn'])
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
            print(response.json())
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
            print(response.json())
            print(response.text)
            return render(request, 'index.html' , {"filename":response.text})
    else:
        form = UploadFileForm()
    return render(request, 'index.html' , {"filename":None})