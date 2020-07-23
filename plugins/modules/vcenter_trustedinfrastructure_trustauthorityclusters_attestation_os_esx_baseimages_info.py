from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_trustedinfrastructure_trustauthorityclusters_attestation_os_esx_baseimages\nextends_documentation_fragment: []\nmodule: vcenter_trustedinfrastructure_trustauthorityclusters_attestation_os_esx_baseimages_info\nnotes:\n- Tested on vSphere 7.0\noptions:\n  cluster:\n    description:\n    - 'The id of the cluster on which the operation will be executed.\n\n      The parameter must be an identifier for the resource type: ClusterComputeResource.'\n    type: str\n  display_name:\n    description:\n    - 'Search criteria by ESX base image version version numbers.\n\n      displayName if {@term.unset} return all ESX display version numbers.'\n    type: list\n  health:\n    description:\n    - 'Search criteria by health indicator.\n\n      health if {@term.unset} return all health indicators.'\n    type: list\n  version:\n    description:\n    - 'The ESX base image version.\n\n      The parameter must be an identifier for the resource type: vcenter.trusted_infrastructure.trust_authority_clusters.attestation.os.esx.BaseImage.'\n    type: str\n  vmw-task:\n    choices:\n    - 'true'\n    description:\n    - vmw-task=true\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_trustedinfrastructure_trustauthorityclusters_attestation_os_esx_baseimages\nversion_added: 1.0.0\n"
IN_QUERY_PARAMETER = ["vmw-task", "display_name", "health"]
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
    argument_spec["vmw-task"] = {
        "type": "str",
        "choices": ["true"],
        "operationIds": ["get", "list"],
    }
    argument_spec["version"] = {"type": "str", "operationIds": ["get", "list"]}
    argument_spec["health"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["display_name"] = {"type": "list", "operationIds": ["list"]}
    argument_spec["cluster"] = {"type": "str", "operationIds": ["get", "list"]}
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
    if params["version"]:
        return "https://{vcenter_hostname}/rest/api/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/attestation/os/esx/base-images/{version}".format(
            **params
        ) + gen_args(
            params, IN_QUERY_PARAMETER
        )
    else:
        return "https://{vcenter_hostname}/rest/api/vcenter/trusted-infrastructure/trust-authority-clusters/{cluster}/attestation/os/esx/base-images".format(
            **params
        ) + gen_args(
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