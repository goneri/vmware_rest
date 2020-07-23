from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_systemconfig_deploymenttype\nextends_documentation_fragment: []\nmodule: vcenter_systemconfig_deploymenttype\nnotes:\n- Tested on vSphere 7.0\noptions:\n  remote_psc:\n    description:\n    - External PSC to register with when reconfiguring a VCSA_EMBEDDED appliance to\n      a VCSA_EXTERNAL appliance.\n    - 'Validate attributes are:'\n    - ' - C(https_port) (int): The HTTPS port of the external PSC appliance.'\n    - ' - C(psc_hostname) (str): The IP address or DNS resolvable name of the remote\n      PSC to which this configuring vCenter Server will be registered to.'\n    - ' - C(ssl_thumbprint) (str): SHA1 thumbprint of the server SSL certificate will\n      be used for verification when ssl_verify field is set to true.'\n    - ' - C(ssl_verify) (bool): SSL verification should be enabled or disabled. If\n      {@name #sslVerify} is true and and {@name #sslThumbprint} is {@term unset},\n      the CA certificate will be used for verification. If {@name #sslVerify} is true\n      and {@name #sslThumbprint} is set then the thumbprint will be used for verification.\n      No verification will be performed if {@name #sslVerify} value is set to false.'\n    - ' - C(sso_admin_password) (str): The SSO administrator account password.'\n    type: dict\n  state:\n    choices:\n    - reconfigure\n    description: []\n    type: str\n  type:\n    choices:\n    - VCSA_EMBEDDED\n    - VCSA_EXTERNAL\n    - PSC_EXTERNAL\n    description:\n    - The {@name ApplianceType} defines the vCenter appliance types.\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_systemconfig_deploymenttype\nversion_added: 1.0.0\n"
IN_QUERY_PARAMETER = []
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
    argument_spec["type"] = {
        "type": "str",
        "choices": ["PSC_EXTERNAL", "VCSA_EMBEDDED", "VCSA_EXTERNAL"],
        "operationIds": ["reconfigure"],
    }
    argument_spec["state"] = {"type": "str", "choices": ["reconfigure"]}
    argument_spec["remote_psc"] = {"type": "dict", "operationIds": ["reconfigure"]}
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
    return "https://{vcenter_hostname}/rest/vcenter/system-config/deployment-type".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _reconfigure(params, session):
    accepted_fields = ["remote_psc", "type"]
    if "reconfigure" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/system-config/deployment-type".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("reconfigure" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "reconfigure")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
