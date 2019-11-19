#!/bin/python

import requests
import json
import sys
import csv
import datetime
from login import login
from login import logout
import getpass

json_data = {}


def post (command, json_data, sid, ip):
        headers = {
            'content-type': "application/json",
            'Accept': "*/*","X-chkp-sid" : sid
        }
        
        try:
            response = requests.post("https://"+ip+"/web_api/"+command, json=json_data, headers=headers, verify=False)
            response_json = json.loads(response.content)
            #print response_json
            return response_json
        except:
            print "Error Occured"
            sys.exit()

#Gather Information            
ip = raw_input("Management Server IP Address: ")
user = raw_input("Username: ")
pw = getpass.getpass('Password:')

#Login
sid = login(ip,user,pw)
#print sid


#Open Text File
rname = "users_in_groups_" + datetime.datetime.now().strftime("%Y_%m_%d") + ".txt"

f = open(rname, "w+")

#List Users within groups--------------------------------------------------------------

f.write("User Groups\n\n")

#Group-------------------------------------------------------

command = "show-generic-objects"
json_data = {
  "class-name" : 'com.checkpoint.objects.classes.dummy.CpmiUserGroup',
    "details-level" : "full"
}

response_json_user = post(command, json_data, sid, ip)

total_groups = response_json_user['total']

#Loop through groups
for y in range(0, total_groups):
    user_group_name = response_json_user['objects'][y]['name']
    f.write(user_group_name + ": \n")
     
    #Users-------------------------------------------------------
    command = "show-generic-objects"
    json_data = {
      "name" : user_group_name,
        "details-level" : "full"
    }

    response_json = post(command, json_data, sid, ip)
    
    #Parse JSON

    user_total_group = response_json['objects'][0]['emptyFieldName']
    user_total_group_length = len(user_total_group)

    #Get usernames from uid
    for x in range(0, user_total_group_length):
        uid = user_total_group[x]
        command = "show-generic-object"
        json_data = {
        "uid" : uid,
        "details-level" : "full"
        }
        response_json = post(command, json_data, sid, ip)
        user_name = response_json
        f.write(user_name['name'] + "\n")
    f.write("\n")
    
logout(sid,ip)

