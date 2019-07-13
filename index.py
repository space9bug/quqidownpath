# -*- coding:utf-8 -*-

import re
import json
import requests

def handler(event, context):
    pathlist = re.split(r'/', str(event['path']))
    quqi_id = str(pathlist[len(pathlist)-2])
    share_code = str(pathlist[len(pathlist)-1])

    # 第一阶段

    url = "https://quqi.com/api/share/public/initdata"

    querystring = {"quqi_id": quqi_id}

    payload = "share_code=" + share_code
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
    }

    response = requests.request(
        "POST", url, data=payload, headers=headers, params=querystring)
    
    # print(response.text)
    responsedata = json.loads(response.text)['data']
    tree_id = str(responsedata['tree_id'])
    node_id = str(responsedata['node_id'])

    # 第二阶段

    url = "https://quqi.com/api/share/public/doc/getDoc"

    querystring = {"quqi_id": quqi_id}

    payload = "tree_id=" + tree_id + "&node_id=" + \
        node_id + "&share_code=" + share_code
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
    }

    response = requests.request(
        "POST", url, data=payload, headers=headers, params=querystring)

    # print(response.text)
    downloadlink = json.loads(response.text)['data']['path']

    jsonResponse = {
        'statusCode': 200,
        'isBase64Encoded': False,
        'headers': {
            "Content-type": "application/json"
        },
        'body': downloadlink,
    }
    return json.dumps(jsonResponse)
