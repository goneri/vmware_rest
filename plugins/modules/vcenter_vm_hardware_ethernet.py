#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: vcenter_vm_hardware_ethernet
short_description: Adds a virtual Ethernet adapter to the virtual machine.
description: Adds a virtual Ethernet adapter to the virtual machine.
options:
  allow_guest_control:
    description:
    - Flag indicating whether the guest can connect and disconnect the device.
    type: bool
  backing:
    description:
    - Physical resource backing for the virtual Ethernet adapter. Required with I(state=['present'])
    - 'Valid attributes are:'
    - ' - C(type) (str): The {@name BackingType} defines the valid backing types for
      a virtual Ethernet adapter.'
    - '   - Accepted values:'
    - '     - STANDARD_PORTGROUP'
    - '     - HOST_DEVICE'
    - '     - DISTRIBUTED_PORTGROUP'
    - '     - OPAQUE_NETWORK'
    - ' - C(network) (str): Identifier of the network that backs the virtual Ethernet
      adapter.'
    - ' - C(distributed_port) (str): Key of the distributed virtual port that backs
      the virtual Ethernet adapter.  Depending on the type of the Portgroup, the port
      may be specified using this field. If the portgroup type is early-binding (also
      known as static), a port is assigned when the Ethernet adapter is configured
      to use the port. The port may be either automatically or specifically assigned
      based on the value of this field. If the portgroup type is ephemeral, the port
      is created and assigned to a virtual machine when it is powered on and the Ethernet
      adapter is connected.  This field cannot be specified as no free ports exist
      before use.'
    type: dict
  label:
    description:
    - The name of the item
    type: str
  mac_address:
    description:
    - MAC address. This field may be modified at any time, and changes will be applied
      the next time the virtual machine is powered on.
    type: str
  mac_type:
    choices:
    - ASSIGNED
    - GENERATED
    - MANUAL
    description:
    - The {@name MacAddressType} defines the valid MAC address origins for a virtual
      Ethernet adapter.
    type: str
  nic:
    description:
    - Virtual Ethernet adapter identifier. Required with I(state=['absent', 'connect',
      'disconnect', 'present'])
    type: str
  pci_slot_number:
    description:
    - Address of the virtual Ethernet adapter on the PCI bus.  If the PCI address
      is invalid, the server will change when it the VM is started or as the device
      is hot added.
    type: int
  start_connected:
    description:
    - Flag indicating whether the virtual device should be connected whenever the
      virtual machine is powered on.
    type: bool
  state:
    choices:
    - absent
    - connect
    - disconnect
    - present
    default: present
    description: []
    type: str
  type:
    choices:
    - E1000
    - E1000E
    - PCNET32
    - VMXNET
    - VMXNET2
    - VMXNET3
    description:
    - The {@name EmulationType} defines the valid emulation types for a virtual Ethernet
      adapter.
    type: str
  upt_compatibility_enabled:
    description:
    - Flag indicating whether Universal Pass-Through (UPT) compatibility should be
      enabled on this virtual Ethernet adapter. This field may be modified at any
      time, and changes will be applied the next time the virtual machine is powered
      on.
    type: bool
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
  wake_on_lan_enabled:
    description:
    - Flag indicating whether wake-on-LAN shoud be enabled on this virtual Ethernet
      adapter. This field may be modified at any time, and changes will be applied
      the next time the virtual machine is powered on.
    type: bool
author:
- Ansible Cloud Team (@ansible-collections)
version_added: 1.0.0
requirements:
- python >= 3.6
- aiohttp
"""

EXAMPLES = r"""
- name: Collect information about a specific VM
  vmware.vmware_rest.vcenter_vm_info:
    vm: '{{ search_result.value[0].vm }}'
  register: test_vm1_info
- name: Attach a VM to a dvswitch
  vmware.vmware_rest.vcenter_vm_hardware_ethernet:
    vm: '{{ test_vm1_info.id }}'
    pci_slot_number: 4
    backing:
      type: DISTRIBUTED_PORTGROUP
      network: '{{ my_portgroup_info.dvs_portgroup_info.dvswitch1[0].key }}'
    start_connected: false
  register: vm_hardware_ethernet_1
- name: Turn the NIC's start_connected flag on
  vmware.vmware_rest.vcenter_vm_hardware_ethernet:
    nic: '{{ vm_hardware_ethernet_1.id }}'
    start_connected: true
    vm: '{{ test_vm1_info.id }}'
"""

RETURN = r"""
# content generated by the update_return_section callback# task: Attach a VM to a dvswitch
id:
  description: moid of the resource
  returned: On success
  sample: '4000'
  type: str
value:
  description: Attach a VM to a dvswitch
  returned: On success
  sample:
    allow_guest_control: 0
    backing:
      connection_cookie: 1107666745
      distributed_port: '2'
      distributed_switch_uuid: 50 26 fa 60 df 9b f8 27-8c 63 8b cc 31 1f ca 53
      network: dvportgroup-1247
      type: DISTRIBUTED_PORTGROUP
    label: Network adapter 1
    mac_address: 00:50:56:a6:eb:d7
    mac_type: ASSIGNED
    pci_slot_number: 4
    start_connected: 0
    state: NOT_CONNECTED
    type: VMXNET3
    upt_compatibility_enabled: 0
    wake_on_lan_enabled: 0
  type: dict
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "create": {
        "query": {},
        "body": {
            "allow_guest_control": "allow_guest_control",
            "backing": "backing",
            "mac_address": "mac_address",
            "mac_type": "mac_type",
            "pci_slot_number": "pci_slot_number",
            "start_connected": "start_connected",
            "type": "type",
            "upt_compatibility_enabled": "upt_compatibility_enabled",
            "wake_on_lan_enabled": "wake_on_lan_enabled",
        },
        "path": {"vm": "vm"},
    },
    "list": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "get": {"query": {}, "body": {}, "path": {"nic": "nic", "vm": "vm"}},
    "update": {
        "query": {},
        "body": {
            "allow_guest_control": "allow_guest_control",
            "backing": "backing",
            "mac_address": "mac_address",
            "mac_type": "mac_type",
            "start_connected": "start_connected",
            "upt_compatibility_enabled": "upt_compatibility_enabled",
            "wake_on_lan_enabled": "wake_on_lan_enabled",
        },
        "path": {"nic": "nic", "vm": "vm"},
    },
    "delete": {"query": {}, "body": {}, "path": {"nic": "nic", "vm": "vm"}},
    "connect": {"query": {}, "body": {}, "path": {"nic": "nic", "vm": "vm"}},
    "disconnect": {"query": {}, "body": {}, "path": {"nic": "nic", "vm": "vm"}},
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

    argument_spec["allow_guest_control"] = {"type": "bool"}
    argument_spec["backing"] = {"type": "dict"}
    argument_spec["label"] = {"type": "str"}
    argument_spec["mac_address"] = {"type": "str"}
    argument_spec["mac_type"] = {
        "type": "str",
        "choices": ["ASSIGNED", "GENERATED", "MANUAL"],
    }
    argument_spec["nic"] = {"type": "str"}
    argument_spec["pci_slot_number"] = {"type": "int"}
    argument_spec["start_connected"] = {"type": "bool"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["absent", "connect", "disconnect", "present"],
        "default": "present",
    }
    argument_spec["type"] = {
        "type": "str",
        "choices": ["E1000", "E1000E", "PCNET32", "VMXNET", "VMXNET2", "VMXNET3"],
    }
    argument_spec["upt_compatibility_enabled"] = {"type": "bool"}
    argument_spec["vm"] = {"required": True, "type": "str"}
    argument_spec["wake_on_lan_enabled"] = {"type": "bool"}

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
    return (
        "https://{vcenter_hostname}" "/api/vcenter/vm/{vm}/hardware/ethernet"
    ).format(**params)


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
    subdevice_type = get_subdevice_type(
        "/api/vcenter/vm/{vm}/hardware/ethernet/{nic}?action=connect"
    )
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}"
        # aa
        "/api/vcenter/vm/{vm}/hardware/ethernet/{nic}?action=connect"
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

    if params["nic"]:
        _json = await get_device_info(session, build_url(params), params["nic"])
    else:
        _json = await exists(params, session, build_url(params), ["nic"])
    if _json:
        if "value" not in _json:  # 7.0.2+
            _json = {"value": _json}
        if "_update" in globals():
            params["nic"] = _json["id"]
            return await globals()["_update"](params, session)
        return await update_changed_flag(_json, 200, "get")

    payload = prepare_payload(params, PAYLOAD_FORMAT["create"])
    _url = (
        "https://{vcenter_hostname}" "/api/vcenter/vm/{vm}/hardware/ethernet"
    ).format(**params)
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
    subdevice_type = get_subdevice_type("/api/vcenter/vm/{vm}/hardware/ethernet/{nic}")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}" "/api/vcenter/vm/{vm}/hardware/ethernet/{nic}"
    ).format(**params) + gen_args(params, _in_query_parameters)
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
    subdevice_type = get_subdevice_type(
        "/api/vcenter/vm/{vm}/hardware/ethernet/{nic}?action=disconnect"
    )
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}"
        # aa
        "/api/vcenter/vm/{vm}/hardware/ethernet/{nic}?action=disconnect"
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


async def _update(params, session):
    payload = prepare_payload(params, PAYLOAD_FORMAT["update"])
    _url = (
        "https://{vcenter_hostname}" "/api/vcenter/vm/{vm}/hardware/ethernet/{nic}"
    ).format(**params)
    async with session.get(_url) as resp:
        _json = await resp.json()
        if "value" in _json:
            value = _json["value"]
        else:  # 7.0.2 and greater
            value = _json
        for k, v in value.items():
            if k in payload and payload[k] == v:
                del payload[k]
            elif "spec" in payload:
                if k in payload["spec"] and payload["spec"][k] == v:
                    del payload["spec"][k]

        if payload == {} or payload == {"spec": {}}:
            # Nothing has changed
            if "value" not in _json:  # 7.0.2
                _json = {"value": _json}
            _json["id"] = params.get("nic")
            return await update_changed_flag(_json, resp.status, "get")
    async with session.patch(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if "value" not in _json:  # 7.0.2
            _json = {"value": _json}
        _json["id"] = params.get("nic")
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
