#!/usr/bin/python

import json
import os
import vagrant
from ansible.module_utils.basic import AnsibleModule


def run_module():

    module_args = dict(
        path=dict(type='str', required=True),
        state=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        return result

    if not os.path.isfile(module.params['path'] + '/Vagrantfile'):
        module.fail_json(msg='Vagrantfile doesn\'t exist', **result)

    try:
        vm = vagrant.Vagrant(module.params['path'])
        vm.status()
    except:
        module.fail_json(msg='Vagrantfile syntax error', **result)

    if module.params['state'] not in ['started', 'stopped', 'destroyed']:
        module.fail_json(msg='Illegal state, please use started|stopped|destroyed', **result)

    def get_vm_info():
        result['state'] = vm.status()[0][1]
        if result['state'] == 'running':
            result['ip_address'] = vm.hostname()
            result['port'] = int(vm.port())
            result['ssh_key_file_path'] = vm.keyfile()
            result['user'] = vm.user()
            result['os_name'] = vm.ssh(None, 'cat /etc/os-release').split('"')[1].split(' ')[0]
            result['ram_size'] = vm.ssh(None, 'cat /proc/meminfo').split('\n')[0].split(' ')[-2]

    if module.params['state'] == 'started':
        result['state'] = vm.status()[0][1]
        if result['state'] != 'running':
            vm.up()
            result['changed'] = True
        get_vm_info()
    elif module.params['state'] == 'stopped':
        result['state'] = vm.status()[0][1]
        if result['state'] != 'poweroff' or result['state'] != 'not_created':
            vm.halt()
            result['changed'] = True
        get_vm_info()
    elif module.params['state'] == 'destroyed':
        result['state'] = vm.status()[0][1]
        if result['state'] != 'not_created':
            vm.destroy()
            result['changed'] = True
        get_vm_info()

    module.exit_json(**result)

def main():
    run_module()


if __name__ == '__main__':
    main()

