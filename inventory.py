#!/usr/bin/python

import json
import os
import vagrant
from pprint import pprint

vm = vagrant.Vagrant("./")

def get_vm_info(name):
    d = {}
    d.update({"name": name})
    d.update({"ansible_connection": "ssh"})
    d.update({"ansible_ssh_port": int(vm.port(name))})
    d.update({"ansible_ssh_host": vm.hostname(name)})
    d.update({"ansible_user": vm.user(name)})
    d.update({"ansible_ssh_private_key_file": vm.keyfile(name)})

    return d

hosts = []
for i in vm.status():
    if i[1] == 'running':
        hosts.append(i[0])

result = {
    'all': {
        "children": ['local', 'vagrantvms'],
    },
    'localhost': {
        "hosts": [
            "localhost"
            ],
    },
    'vagrantvms': {
        "hosts": hosts
    },

    '_meta': {
        'hostvars': {
            "localhost" : {
                "ansible_connection": "local"
            }
        }
    },
}

for i in hosts:
    result['_meta']['hostvars'].update({i: get_vm_info(i)})

print json.dumps(result)
