#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'N-A'
}

DOCUMENTATION = '''
---
module: tinc_retrieve_public_getkey

short_description: Get key 

version_added: "2.4"

description:
    - "Get tinc"

options:
    network:
        description:
            - This is name of the network        
        required: true
    node_name:
        description:
            - Control to demo if the result of this module is changed or not
        required: false
    file:
        description: 
            - Name of the file to check
    required:
        description: 
            - If the key is not present, fail.                 

author:
    - VerosK (@verosk)
'''

from ansible.module_utils.basic import AnsibleModule


def read_key(module, file_name):
    try:
        f = open(file_name, 'rb')
    except FileNotFoundError:
        module.fail_json(
            "Unable to open file `{}`".format(file_name))

    key, in_key = [], False
    for ln in f.readlines():
        if ln.strip() == '-----BEGIN RSA PUBLIC KEY-----':
            assert len(key) == 0, key
            key.append(ln.strip())
            in_key = True
            continue
        if ln.strip() == '-----END RSA PUBLIC KEY-----':
            key.append(ln.strip())
            in_key = False
            continue
        if in_key:
            key.append(ln.strip())
    return '\n'.join(key)


def run_module():
    module_args = dict(
        network=dict(type='str', required=False),
        node_name=dict(type='str', required=False),
        file=dict(type='str', required=False),
        required=dict(type='bool', default=False),
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    params_valid = False
    if module.params['network'] and module.params['node_name']:
        params_valid = True
        file_name = '/etc/tinc/{}/hosts/{}'.format(
            module.params['network'], module.params['node_name'])

    elif module.params['file']:
        params_valid = True
        file_name = module.params['file']

    if not params_valid:
        module.fail_json(
            "Insufficient parameters. Either `file` or bot `network` "
            "and `nodename` should be provided")

    result['file'] = file_name

    key = read_key(module=module, file_name=file_name)

    if not key and module.params['required']:
        result['message'] = 'No key has been found'
        result['failed'] = True

    if key:
        result['ansible_facts'] = dict(tinc_node_public_key=key)
        result['key'] = key
        result['message'] = 'Key has been received'
    else:
        result['message'] = 'No key has been found'
    result['changed'] = False
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
