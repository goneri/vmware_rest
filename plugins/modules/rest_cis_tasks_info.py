from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type rest_cis_tasks\nextends_documentation_fragment: []\nmodule: rest_cis_tasks_info\nnotes:\n- Tested on vSphere 7.0\noptions:\n  filter_spec.operations:\n    description:\n    - \"Identifiers of operations. Tasks created by these operations match the filter\\\n      \\ (see CommonInfo.operation). \\n Note that an operation identifier by itself\\\n      \\ is not globally unique. To filter on an operation, the identifier of the service\\\n      \\ interface containing the operation should also be specified in Tasks.FilterSpec.services.\\n\\\n      \\nIf unset or empty, tasks associated with any operation will match the filter.\\n\\\n      When clients pass a value of this structure as a parameter, the field must contain\\\n      \\ identifiers for the resource type: vapi.operation. When operations return\\\n      \\ a value of this structure as a result, the field will contain identifiers\\\n      \\ for the resource type: vapi.operation.\"\n    type: list\n  filter_spec.services:\n    description:\n    - 'Identifiers of services. Tasks created by operations in these services match\n      the filter (see CommonInfo.service).\n\n      This field may be unset if Tasks.FilterSpec.tasks is specified. Currently all\n      services must be from the same provider. If this field is unset or empty, tasks\n      for any service will match the filter.\n\n      When clients pass a value of this structure as a parameter, the field must contain\n      identifiers for the resource type: vapi.service. When operations return a value\n      of this structure as a result, the field will contain identifiers for the resource\n      type: vapi.service.'\n    type: list\n  filter_spec.status:\n    description:\n    - 'Status that a task must have to match the filter (see CommonInfo.status).\n\n      If unset or empty, tasks with any status match the filter.'\n    type: list\n  filter_spec.targets:\n    description:\n    - 'Identifiers of the targets the operation for the associated task created or\n      was performed on (see CommonInfo.target).\n\n      If unset or empty, tasks associated with operations on any target match the\n      filter.'\n    type: list\n  filter_spec.tasks:\n    description:\n    - 'Identifiers of tasks that can match the filter.\n\n      This field may be unset if Tasks.FilterSpec.services is specified. Currently\n      all tasks must be from the same provider. If unset or empty, tasks with any\n      identifier will match the filter.\n\n      When clients pass a value of this structure as a parameter, the field must contain\n      identifiers for the resource type: cis.task. When operations return a value\n      of this structure as a result, the field will contain identifiers for the resource\n      type: cis.task.'\n    type: list\n  filter_spec.users:\n    description:\n    - 'Users who must have initiated the operation for the associated task to match\n      the filter (see CommonInfo.user).\n\n      If unset or empty, tasks associated with operations initiated by any user match\n      the filter.'\n    type: list\n  result_spec.exclude_result:\n    description:\n    - 'If true, the result will not be included in the task information, otherwise\n      it will be included.\n\n      If unset, the result of the operation will be included in the task information.'\n    type: bool\n  result_spec.return_all:\n    description:\n    - 'If true, all data, including operation-specific data, will be returned, otherwise\n      only the data described in Info will be returned.\n\n      If unset, only the data described in Info will be returned.'\n    type: bool\n  spec.exclude_result:\n    description:\n    - 'If true, the result will not be included in the task information, otherwise\n      it will be included.\n\n      If unset, the result of the operation will be included in the task information.'\n    type: bool\n  spec.return_all:\n    description:\n    - 'If true, all data, including operation-specific data, will be returned, otherwise\n      only the data described in Info will be returned.\n\n      If unset, only the data described in Info will be returned.'\n    type: bool\n  task:\n    description:\n    - 'Task identifier.\n\n      The parameter must be an identifier for the resource type: cis.task. Required\n      with I(state=[''get''])'\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type rest_cis_tasks\nversion_added: 1.0.0\n"
IN_QUERY_PARAMETER = [
    "spec.return_all",
    "spec.exclude_result",
    "filter_spec.tasks",
    "filter_spec.services",
    "filter_spec.operations",
    "filter_spec.status",
    "filter_spec.targets",
    "filter_spec.users",
    "result_spec.return_all",
    "result_spec.exclude_result",
]
from ansible.module_utils.basic import env_fallback

try:
    from ansible_module.turbo.module import AnsibleTurboModule as AnsibleModule
except ImportError:
    from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    gen_args,
    open_session,
    update_changed_flag,
)


def prepare_argument_spec():
    argument_spec = {
        "vcenter_hostname": dict(
            type="str", required=False, fallback=(env_fallback, ["VMWARE_HOST"])
        ),
        "vcenter_username": dict(
            type="str", required=False, fallback=(env_fallback, ["VMWARE_USER"])
        ),
        "vcenter_password": dict(
            type="str",
            required=False,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_PASSWORD"]),
        ),
        "vcenter_certs": dict(
            type="bool",
            required=False,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_VALIDATE_CERTS"]),
        ),
    }
    argument_spec["task"] = {"type": "str", "operationIds": ["get"]}
    argument_spec["spec.return_all"] = {"type": "bool", "operationIds": ["get"]}
    argument_spec["spec.exclude_result"] = {"type": "bool", "operationIds": ["get"]}
    argument_spec["result_spec.return_all"] = {"type": "bool", "operationIds": ["list"]}
    argument_spec["result_spec.exclude_result"] = {
        "type": "bool",
        "operationIds": ["list"],
    }
    argument_spec["filter_spec.users"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter_spec.tasks"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter_spec.targets"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter_spec.status"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter_spec.services"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["filter_spec.operations"] = {"type": "list", "operationIds": ["list"]}
    return argument_spec


async def get_device_info(params, session, _url, _key):
    async with session.get(((_url + "/") + _key)) as resp:
        _json = await resp.json()
        entry = _json["value"]
        entry["_key"] = _key
        return entry


async def list_devices(params, session):
    existing_entries = []
    _url = url(params)
    async with session.get(_url) as resp:
        _json = await resp.json()
        devices = _json["value"]
    for device in devices:
        _id = list(device.values())[0]
        existing_entries.append((await get_device_info(params, session, _url, _id)))
    return existing_entries


async def exists(params, session):
    unicity_keys = ["bus", "pci_slot_number"]
    devices = await list_devices(params, session)
    for device in devices:
        for k in unicity_keys:
            if (params.get(k) is not None) and (device.get(k) != params.get(k)):
                break
        else:
            return device


async def main():
    module_args = prepare_argument_spec()
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    session = await open_session(
        vcenter_hostname=module.params["vcenter_hostname"],
        vcenter_username=module.params["vcenter_username"],
        vcenter_password=module.params["vcenter_password"],
    )
    result = await entry_point(module, session)
    module.exit_json(**result)


def url(params):
    if params["task"]:
        return "https://{vcenter_hostname}/rest/cis/tasks/{task}".format(
            **params
        ) + gen_args(params, IN_QUERY_PARAMETER)
    else:
        return "https://{vcenter_hostname}/rest/cis/tasks".format(**params) + gen_args(
            params, IN_QUERY_PARAMETER
        )


async def entry_point(module, session):
    async with session.get(url(module.params)) as resp:
        _json = await resp.json()
        return await update_changed_flag(_json, resp.status, "get")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
