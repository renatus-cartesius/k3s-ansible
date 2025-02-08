#!/usr/bin/python3

import requests as r
import json as j
import os

api_url = "https://compute.api.cloud.yandex.net/compute/v1/instances"
api_token = os.environ['YC_TOKEN']
group_label = "ansible.group"
folder_id = os.environ['YC_FOLDER_ID']


def get_hosts(data_json):
    host_groups = dict()

    host_groups['k3s_cluster'] = {}
    host_groups['k3s_cluster']['children'] = {}

    if data_json == {}:
        return {}

    for instance in data_json['instances']:
        group = instance['labels'][group_label]
        address = instance['networkInterfaces'][0]['primaryV4Address']['oneToOneNat']['address']

        if group not in host_groups['k3s_cluster']['children']:
            host_groups['k3s_cluster']['children'][group] = {'hosts': [], 'vars': {}, 'children': []}
        host_groups['k3s_cluster']['children'][group]['hosts'].append(address)
    return j.dumps(host_groups, indent=2)


def main():
    payload = {"folderId": f"{folder_id}"}
    headers = {"Authorization": f"Bearer {api_token}"}

    res = r.get(api_url, params=payload, headers=headers)
    hosts_formatted = get_hosts(j.loads(res.text))

    print(hosts_formatted)


if __name__ == '__main__':
    main()
