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
module: vcenter_vm_hardware_adapter_scsi_info
short_description: Returns information about a virtual SCSI adapter.
description: Returns information about a virtual SCSI adapter.
options:
  adapter:
    description:
    - Virtual SCSI adapter identifier. Required with I(state=['get'])
    type: str
  label:
    description:
    - The name of the item
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
  vm:
    description:
    - Virtual machine identifier. This parameter is mandatory.
    required: true
    type: str
author:
- Ansible Cloud Team (@ansible-collections)
version_added: 1.0.0
requirements:
- python >= 3.6
- aiohttp
"""

EXAMPLES = r"""
- name: Look up the VM called test_vm1 in the inventory
  register: search_result
  vmware.vmware_rest.vcenter_vm_info:
    filter_names:
    - test_vm1

- name: Collect information about a specific VM
  vmware.vmware_rest.vcenter_vm_info:
    vm: '{{ search_result.value[0].vm }}'
  register: test_vm1_info

- name: List the SCSI adapter of a given VM
  vmware.vmware_rest.vcenter_vm_hardware_adapter_scsi_info:
    vm: '{{ test_vm1_info.id }}'
"""

RETURN = r"""
# content generated by the update_return_section callback# task: List the SCSI adapter of a given VM
value:
  description: List the SCSI adapter of a given VM
  returned: On success
  sample:
  - label: SCSI controller 0
    scsi:
      bus: 0
      unit: 7
    sharing: NONE
    type: PVSCSI
  type: list
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "get": {"query": {}, "body": {}, "path": {"adapter": "adapter", "vm": "vm"}},
    "list": {"query": {}, "body": {}, "path": {"vm": "vm"}},
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

    argument_spec["adapter"] = {"type": "str"}
    argument_spec["label"] = {"type": "str"}
    argument_spec["vm"] = {"required": True, "type": "str"}

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


# template: info_list_and_get_module.j2
def build_url(params):
    if params.get("adapter"):
        _in_query_parameters = PAYLOAD_FORMAT["get"]["query"].keys()
        return (
            (
                "https://{vcenter_hostname}"
                "/api/vcenter/vm/{vm}/hardware/adapter/scsi/"
            ).format(**params)
            + params["adapter"]
            + gen_args(params, _in_query_parameters)
        )
    _in_query_parameters = PAYLOAD_FORMAT["list"]["query"].keys()
    return (
        "https://{vcenter_hostname}" "/api/vcenter/vm/{vm}/hardware/adapter/scsi"
    ).format(**params) + gen_args(params, _in_query_parameters)


async def entry_point(module, session):
    url = build_url(module.params)
    async with session.get(url) as resp:
        _json = await resp.json()

        if "value" not in _json:  # 7.0.2+
            _json = {"value": _json}

        if module.params.get("adapter"):
            _json["id"] = module.params.get("adapter")
        elif module.params.get("label"):  # TODO extend the list of filter
            _json = await exists(module.params, session, url)
        else:  # list context, retrieve the details of each entry
            try:
                if (
                    isinstance(_json["value"][0]["adapter"], str)
                    and len(list(_json["value"][0].values())) == 1
                ):
                    # this is a list of id, we fetch the details
                    full_device_list = await build_full_device_list(session, url, _json)
                    _json = {"value": [i["value"] for i in full_device_list]}
            except (TypeError, KeyError, IndexError):
                pass

        return await update_changed_flag(_json, resp.status, "get")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
