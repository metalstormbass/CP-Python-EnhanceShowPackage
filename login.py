#!/bin/python
import requests
import json
import sys

#remove https warning
requests.packages.urllib3.disable_warnings()

#Login function
def login(ip,user,pw):
    payload_list={}
    payload_list['user']=user
    payload_list['password']=pw
    headers = {
            'content-type': "application/json",
            'Accept': "*/*",
        }
    try:
        response = requests.post("https://"+ip+"/web_api/login", json=payload_list, headers=headers, verify=False)
        #print response
        response_json = json.loads(response.content)
        #print response_json
        sid = response_json['sid']
        return sid    

    except:
        print "Unable to login. Ensure the API is enabled and check credentials"
        sys.exit()

#Logout function 
def logout(sid,ip):
        payload_list={}
        headers = {
                'content-type': "application/json",
                'Accept': "*/*",
                'x-chkp-sid': sid,
            }
        response = requests.post("https://"+ip+"/web_api/login", json=payload_list, headers=headers, verify=False)
        return response
