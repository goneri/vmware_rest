from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type stats_counters\nextends_documentation_fragment: []\nmodule: stats_counters_info\nnotes:\n- Tested on vSphere 7.0\noptions:\n  cid:\n    description:\n    - 'Counter ID.\n\n      The parameter must be an identifier for the resource type: vstats.model.Counter.'\n    type: str\n  metric:\n    description:\n    - 'Metric for which counters will be listed. Warning: This attribute is available\n      as Technology Preview. These are early access APIs provided to test, automate\n      and provide feedback on the feature. Since this can change based on feedback,\n      VMware does not guarantee backwards compatibility and recommends against using\n      them in production environments. Some Technology Preview APIs might only be\n      applicable to specific environments.\n\n      If unset metric filter will not be applied.\n\n      When clients pass a value of this structure as a parameter, the field must be\n      an identifier for the resource type: vstats.model.Metric. When operations return\n      a value of this structure as a result, the field will be an identifier for the\n      resource type: vstats.model.Metric.'\n    type: str\n  types:\n    description:\n    - 'Resource type filter. Warning: This attribute is available as Technology Preview.\n      These are early access APIs provided to test, automate and provide feedback\n      on the feature. Since this can change based on feedback, VMware does not guarantee\n      backwards compatibility and recommends against using them in production environments.\n      Some Technology Preview APIs might only be applicable to specific environments.\n\n      If unset resource type filter will not be applied.\n\n      When clients pass a value of this structure as a parameter, the field must contain\n      identifiers for the resource type: vstats.model.RsrcType. When operations return\n      a value of this structure as a result, the field will contain identifiers for\n      the resource type: vstats.model.RsrcType.'\n    type: list\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type stats_counters\nversion_added: 1.0.0\n"
IN_QUERY_PARAMETER = ["types", "metric"]
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
    argument_spec["types"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["metric"] = {"type": "str", "operationIds": ["list"]}
    argument_spec["cid"] = {"type": "str", "operationIds": ["get", "list"]}
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
    if params["cid"]:
        return "https://{vcenter_hostname}/rest/api/stats/counters/{cid}".format(
            **params
        ) + gen_args(params, IN_QUERY_PARAMETER)
    else:
        return "https://{vcenter_hostname}/rest/api/stats/counters".format(
            **params
        ) + gen_args(params, IN_QUERY_PARAMETER)


async def entry_point(module, session):
    async with session.get(url(module.params)) as resp:
        _json = await resp.json()
        return await update_changed_flag(_json, resp.status, "get")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
