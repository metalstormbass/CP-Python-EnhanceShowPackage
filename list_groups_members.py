#!/bin/python

import requests
import json
import sys
import csv
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
            #print (response_json)
            return response_json
        except:
            print ("Error Occured")
            sys.exit()

#Gather Information            
ip = input("Management Server IP Address: ")
user = input("Username: ")
pw = getpass.getpass('Password:')

#Login
sid = login(ip,user,pw)
#print sid

print ("")
print ("")

#Gather Network Groups -------------------------------------------------------------
print ("Network Groups")
command = "show-groups"
json_data = {
  "limit" : 500,
  "offset" : 0,
  "details-level" : "standard"
}

response_json = post(command, json_data, sid, ip)

#Parse JSON

total_group = response_json['total']
group_list = []

for x in range(0, total_group):
    group_name = response_json['objects'][x]['name']
    #print (group_name)
    group_list.append(group_name)
     
for name in group_list: 
    print (name + ":")
    print ("")
    command = "show-group"
    json_data = {"name" : name}
    #print json_data
    response_json = post(command, json_data, sid, ip)
    #print response_json["members"]
    for y in response_json['members']:
        print (y['name'])
    print ("")
    print ("")
    
#Service Groups ---------------------------------------------------------------------
    
print ("Service Groups")
command = "show-service-groups"
json_data = {
  "limit" : 500,
  "offset" : 0,
  "details-level" : "standard"
}

response_json = post(command, json_data, sid, ip)
#Parse JSON

service_total_group = response_json['total']
print (service_total_group)
service_group_list = []



for x in range(0, service_total_group):
    service_group_name = response_json['objects'][x]['name']
    print (service_group_name)
    service_group_list.append(service_group_name)
     
for name in service_group_list: 
    print (name + ":")
    command = "show-service-group"
    json_data = {"name" : name}
    json_data
    response_json = post(command, json_data, sid, ip)
    #print response_json["members"]
    for y in response_json['members']:
        print (y['name'])
    print ("")
    
    
#List Users within groups--------------------------------------------------------------

print ("User Groups:")
print ("")

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
    print (user_group_name + ":")
    
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
        print (user_name['name'])
    print ("")


