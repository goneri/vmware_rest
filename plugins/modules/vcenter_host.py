#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated by vmware_rest_code_generator.
# See: https://github.com/ansible-collections/vmware_rest_code_generator
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: vcenter_host
short_description: Add a new standalone host in the vCenter inventory
description: Add a new standalone host in the vCenter inventory. The newly connected
  host will be in connected state. The vCenter Server will verify the SSL certificate
  before adding the host to its inventory. In the case where the SSL certificate cannot
  be verified because the Certificate Authority is not recognized or the certificate
  is self signed, the vCenter Server will fall back to thumbprint verification mode
  as defined by {@link CreateSpec.ThumbprintVerification}.
options:
  folder:
    description:
    - Host and cluster folder in which the new standalone host should be created.
    type: str
  force_add:
    description:
    - Whether host should be added to the vCenter Server even if it is being managed
      by another vCenter Server. The original vCenterServer loses connection to the
      host.
    type: bool
  host:
    description:
    - Identifier of the host to be disconnected. Required with I(state=['absent',
      'connect', 'disconnect'])
    type: str
  hostname:
    description:
    - The IP address or DNS resolvable name of the host. Required with I(state=['present'])
    type: str
  password:
    description:
    - The password for the administrator account on the host. Required with I(state=['present'])
    type: str
  port:
    description:
    - The port of the host.
    type: int
  state:
    choices:
    - absent
    - connect
    - disconnect
    - present
    default: present
    description: []
    type: str
  thumbprint:
    description:
    - 'The thumbprint of the SSL certificate, which the host is expected to have.
      The thumbprint is always computed using the SHA1 hash and is the string representation
      of that hash in the format: xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx
      where, ''x'' represents a hexadecimal digit.'
    type: str
  thumbprint_verification:
    choices:
    - NONE
    - THUMBPRINT
    description:
    - The {@name ThumbprintVerification} defines the thumbprint verification schemes
      for a host's SSL certificate. Required with I(state=['present'])
    type: str
  user_name:
    description:
    - The administrator account on the host. Required with I(state=['present'])
    type: str
  vcenter_hostname:
    description:
    - The hostname or IP address of the vSphere vCenter
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_HOST) will be used instead.
    required: true
    type: str
  vcenter_password:
    description:
    - The vSphere vCenter username
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_PASSWORD) will be used instead.
    required: true
    type: str
  vcenter_rest_log_file:
    description:
    - 'You can use this optional parameter to set the location of a log file. '
    - 'This file will be used to record the HTTP REST interaction. '
    - 'The file will be stored on the host that run the module. '
    - 'If the value is not specified in the task, the value of '
    - environment variable C(VMWARE_REST_LOG_FILE) will be used instead.
    type: str
  vcenter_username:
    description:
    - The vSphere vCenter username
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_USER) will be used instead.
    required: true
    type: str
  vcenter_validate_certs:
    default: true
    description:
    - Allows connection when SSL certificates are not valid. Set to C(false) when
      certificates are not trusted.
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_VALIDATE_CERTS) will be used instead.
    type: bool
author:
- Ansible Cloud Team (@ansible-collections)
version_added: 1.0.0
requirements:
- python >= 3.6
- aiohttp
"""

EXAMPLES = r"""
- name: Build a list of all the folders
  vmware.vmware_rest.vcenter_folder_info:
  register: my_folders

- name: Look up the different folders
  set_fact:
    my_host_folder: '{{ my_folders.value|selectattr("type", "equalto", "HOST")|first
      }}'

- name: Connect the host(s)
  vmware.vmware_rest.vcenter_host:
    hostname: "{{ lookup('env', 'ESXI1_HOSTNAME') }}"
    user_name: "{{ lookup('env', 'ESXI1_USERNAME') }}"
    password: "{{ lookup('env', 'ESXI1_PASSWORD') }}"
    thumbprint_verification: NONE
    folder: '{{ my_host_folder.folder }}'
"""

RETURN = r"""
# content generated by the update_return_section callback# task: Connect the host(s)
value:
  description: Connect the host(s)
  returned: On success
  sample: host-1404
  type: str
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "disconnect": {"query": {}, "body": {}, "path": {"host": "host"}},
    "delete": {"query": {}, "body": {}, "path": {"host": "host"}},
    "create": {
        "query": {},
        "body": {
            "folder": "folder",
            "force_add": "force_add",
            "hostname": "hostname",
            "password": "password",
            "port": "port",
            "thumbprint": "thumbprint",
            "thumbprint_verification": "thumbprint_verification",
            "user_name": "user_name",
        },
        "path": {},
    },
    "connect": {"query": {}, "body": {}, "path": {"host": "host"}},
}  # pylint: disable=line-too-long

import json
import socket
from ansible.module_utils.basic import env_fallback

try:
    from ansible_collections.cloud.common.plugins.module_utils.turbo.exceptions import (
        EmbeddedModuleFailure,
    )
    from ansible_collections.cloud.common.plugins.module_utils.turbo.module import (
        AnsibleTurboModule as AnsibleModule,
    )

    AnsibleModule.collection_name = "vmware.vmware_rest"
except ImportError:
    from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    build_full_device_list,
    exists,
    gen_args,
    get_device_info,
    get_subdevice_type,
    list_devices,
    open_session,
    prepare_payload,
    update_changed_flag,
)


def prepare_argument_spec():
    argument_spec = {
        "vcenter_hostname": dict(
            type="str", required=True, fallback=(env_fallback, ["VMWARE_HOST"]),
        ),
        "vcenter_username": dict(
            type="str", required=True, fallback=(env_fallback, ["VMWARE_USER"]),
        ),
        "vcenter_password": dict(
            type="str",
            required=True,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_PASSWORD"]),
        ),
        "vcenter_validate_certs": dict(
            type="bool",
            required=False,
            default=True,
            fallback=(env_fallback, ["VMWARE_VALIDATE_CERTS"]),
        ),
        "vcenter_rest_log_file": dict(
            type="str",
            required=False,
            fallback=(env_fallback, ["VMWARE_REST_LOG_FILE"]),
        ),
    }

    argument_spec["folder"] = {"type": "str"}
    argument_spec["force_add"] = {"type": "bool"}
    argument_spec["host"] = {"type": "str"}
    argument_spec["hostname"] = {"type": "str"}
    argument_spec["password"] = {"no_log": True, "type": "str"}
    argument_spec["port"] = {"type": "int"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["absent", "connect", "disconnect", "present"],
        "default": "present",
    }
    argument_spec["thumbprint"] = {"type": "str"}
    argument_spec["thumbprint_verification"] = {
        "type": "str",
        "choices": ["NONE", "THUMBPRINT"],
    }
    argument_spec["user_name"] = {"no_log": True, "type": "str"}

    return argument_spec


async def main():
    required_if = list([])

    module_args = prepare_argument_spec()
    module = AnsibleModule(
        argument_spec=module_args, required_if=required_if, supports_check_mode=True
    )
    if not module.params["vcenter_hostname"]:
        module.fail_json("vcenter_hostname cannot be empty")
    if not module.params["vcenter_username"]:
        module.fail_json("vcenter_username cannot be empty")
    if not module.params["vcenter_password"]:
        module.fail_json("vcenter_password cannot be empty")
    try:
        session = await open_session(
            vcenter_hostname=module.params["vcenter_hostname"],
            vcenter_username=module.params["vcenter_username"],
            vcenter_password=module.params["vcenter_password"],
            validate_certs=module.params["vcenter_validate_certs"],
            log_file=module.params["vcenter_rest_log_file"],
        )
    except EmbeddedModuleFailure as err:
        module.fail_json(err.get_message())
    result = await entry_point(module, session)
    module.exit_json(**result)


# template: default_module.j2
def build_url(params):
    return ("https://{vcenter_hostname}" "/api/vcenter/host").format(**params)


async def entry_point(module, session):

    if module.params["state"] == "present":
        if "_create" in globals():
            operation = "create"
        else:
            operation = "update"
    elif module.params["state"] == "absent":
        operation = "delete"
    else:
        operation = module.params["state"]

    func = globals()["_" + operation]

    return await func(module.params, session)


async def _connect(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["connect"]["query"].keys()
    payload = prepare_payload(params, PAYLOAD_FORMAT["connect"])
    subdevice_type = get_subdevice_type("/api/vcenter/host/{host}?action=connect")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}"
        # aa
        "/api/vcenter/host/{host}?action=connect"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if "value" not in _json:  # 7.0.2
            _json = {"value": _json}
        return await update_changed_flag(_json, resp.status, "connect")


async def _create(params, session):

    if params["host"]:
        _json = await get_device_info(session, build_url(params), params["host"])
    else:
        _json = await exists(params, session, build_url(params), ["host"])
    if _json:
        if "value" not in _json:  # 7.0.2+
            _json = {"value": _json}
        if "_update" in globals():
            params["host"] = _json["id"]
            return await globals()["_update"](params, session)
        return await update_changed_flag(_json, 200, "get")

    payload = prepare_payload(params, PAYLOAD_FORMAT["create"])
    _url = ("https://{vcenter_hostname}" "/api/vcenter/host").format(**params)
    async with session.post(_url, json=payload) as resp:
        if resp.status == 500:
            text = await resp.text()
            raise EmbeddedModuleFailure(
                f"Request has failed: status={resp.status}, {text}"
            )
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}

        if resp.status in [200, 201]:
            if isinstance(_json, str):  # 7.0.2 and greater
                _id = _json  # TODO: fetch the object
            elif isinstance(_json, dict) and "value" not in _json:
                _id = list(_json["value"].values())[0]
            elif isinstance(_json, dict) and "value" in _json:
                _id = _json["value"]
            _json_device_info = await get_device_info(session, _url, _id)
            if _json_device_info:
                _json = _json_device_info

        return await update_changed_flag(_json, resp.status, "create")


async def _delete(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["delete"]["query"].keys()
    payload = prepare_payload(params, PAYLOAD_FORMAT["delete"])
    subdevice_type = get_subdevice_type("/api/vcenter/host/{host}")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = ("https://{vcenter_hostname}" "/api/vcenter/host/{host}").format(
        **params
    ) + gen_args(params, _in_query_parameters)
    async with session.delete(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


async def _disconnect(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["disconnect"]["query"].keys()
    payload = prepare_payload(params, PAYLOAD_FORMAT["disconnect"])
    subdevice_type = get_subdevice_type("/api/vcenter/host/{host}?action=disconnect")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}"
        # aa
        "/api/vcenter/host/{host}?action=disconnect"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if "value" not in _json:  # 7.0.2
            _json = {"value": _json}
        return await update_changed_flag(_json, resp.status, "disconnect")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
