import requests
import json
import pdb

url = "https://10.254.64.182:8443/univmax/restapi/replication/devicegroup/"

payload = ""
headers = {
    'Authorization': "Basic c21jOnNtYw==",
    'cache-control': "no-cache",
    'Postman-Token': "5ea09b37-cdc5-4f0d-aeea-51f9f2e2902e"
    }

response = requests.request("GET", url, data=payload,verify=False, headers=headers)

# print(response.text)
json_data = json.loads(response.text)


test=[]
test=json_data['name']

name=[]
rdfgs=[]
symid = []
new_dict = {}
new_dict1 = {}
st="3154"
for t in test:

    url = "https://10.254.64.182:8443/univmax/restapi/replication/devicegroup/"+t

    response = requests.request("GET", url, data=payload,verify=False, headers=headers)

    json_data = json.loads(response.text)

    if st in json_data['deviceGroup']['symmetrixId']:
        name.append(json_data['deviceGroup']['name'])
        symid.append(json_data['deviceGroup']['symmetrixId'])
        rdfgs.append(json_data['deviceGroup']['standardRdfgs'])
new_dict=dict(zip(name,rdfgs))
new_dict1=dict(zip(name,symid))
v_names=[]
'''for (k,v), (k2,v2) in zip(new_dict.items(), new_dict1.items()):
    print(v)
    print(v2)
    str1 = ''.join(str(e) for e in v)'''
for rest in rdfgs:
    for r1 in rest:
        #pdb.set_trace()
        rstr = str(r1)
        url1 = "https://10.254.64.182:8443/univmax/restapi/83/replication/symmetrix/000192603154/rdf_group/"+rstr+"/volume"

        response = requests.request("GET", url1, data=payload,verify=False, headers=headers)

        json_data = json.loads(response.text)
        json_names = json_data['name']
        #pdb.set_trace()
        for json_name in json_names:
            v_names.append(json_name)

print(v_names)
vol_id=[]
type=[]
cap_gb=[]
wwn=[]
storageGroupId=[]
for v_name in v_names:
    url = "https://10.254.64.182:8443/univmax/restapi/provisioning/symmetrix/000192603154/volume/"+v_name

    response = requests.request("GET", url, data=payload, verify=False ,headers=headers)
    json_data = json.loads(response.text)
    print(json_data)
    vol_id.append(json_data['volume']['volumeId'])
    pdb.set_trace()
    type.append(json_data['volume']['type'])
    cap_gb.append(json_data['volume']['cap_gb'])
    wwn.append(json_data['volume']['wwn'])
    storageGroupId.append(json_data['volume']['storageGroupId'])

print(vol_id)
print(type)
print(cap_gb)
print(wwn)
print(storageGroupId)
