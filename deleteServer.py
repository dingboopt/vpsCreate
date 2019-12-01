import json
import requests
import time
import subprocess
import sys

print "arg count is "
print len(sys.argv)

if (sys.argv[1] == '-h'):
    print "usage: username password"

username = sys.argv[1]
password = sys.argv[2]


url = 'https://iam.ap-southeast-1.myhwclouds.com/v3/auth/tokens'
headers = {'Content-type': 'application/json'}
data = {u'auth': {u'scope': {u'project': {u'name': u'ap-southeast-1'}},u'identity': {u'password': {u'user': {u'domain': {u'name': username}, u'password': password, u'name': username}}, u'methods': [u'password']}}}

resp = requests.post(url=url, data=json.dumps(data), headers=headers )
print resp.headers
headers = resp.headers
token = headers['x-subject-token']
print token

#get servers
url = 'https://ecs.ap-southeast-1.myhuaweicloud.com/v1/d915e1d6c7c845e88f3d4d099e671bee/cloudservers/detail'
headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
resp = requests.get(url=url, headers=headers )

print resp.text
serversInfo = json.loads(resp.text)
serverNum = serversInfo['count']

serversInfoDetail = json.loads(resp.text)['servers']
servers = []
for i in range(0,serverNum):
    servers.append({'id':serversInfoDetail[i]['id']})

#delete servers
url = 'https://ecs.ap-southeast-1.myhuaweicloud.com/v1/d915e1d6c7c845e88f3d4d099e671bee/cloudservers/delete'
data = {u'delete_volume': True, u'delete_publicip': True, u'servers': servers}
headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
resp = requests.post(url=url, data=json.dumps(data), headers=headers )
print resp

retcode = subprocess.call(["ssh-keygen", "-f", "/root/.ssh/known_hosts", "-R" ,publicIp])

print retcode

retcode = subprocess.call(["rm", "/data/data/com.termux/files/home/.ssh/known_hosts"])

