#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: content_locallibrary
short_description: Updates the properties of a local library. <p> This is an incremental
  update to the local library. {@term Fields} that are {@term unset} in the update
  specification will be left unchanged.
description: Updates the properties of a local library. <p> This is an incremental
  update to the local library. {@term Fields} that are {@term unset} in the update
  specification will be left unchanged.
options:
  client_token:
    description:
    - 'A unique token generated on the client for each creation request. The token
      should be a universally unique identifier (UUID), for example: C(b8a2a2e3-2314-43cd-a871-6ede0f429751).
      This token can be used to guarantee idempotent creation.'
    type: str
  creation_time:
    description:
    - The date and time when this library was created.
    type: str
  description:
    description:
    - A human-readable description for this library.
    type: str
  id:
    description:
    - An identifier which uniquely identifies this Library.
    type: str
  last_modified_time:
    description:
    - The date and time when this library was last updated. This field is updated
      automatically when the library properties are changed. This field is not affected
      by adding, removing, or modifying a library item or its content within the library.
      Tagging the library or syncing the subscribed library does not alter this field.
    type: str
  last_sync_time:
    description:
    - The date and time when this library was last synchronized. This field applies
      only to subscribed libraries. It is updated every time a synchronization is
      triggered on the library. The value is not set for a local library.
    type: str
  library_id:
    description:
    - Identifier of the local library to delete. Required with I(state=['absent',
      'present', 'publish'])
    type: str
  name:
    description:
    - The name of the library. A Library is identified by a human-readable name. Library
      names cannot be undefined or an empty string. Names do not have to be unique.
    type: str
  optimization_info:
    description:
    - Defines various optimizations and optimization parameters applied to this library.
    - 'Valid attributes are:'
    - ' - C(optimize_remote_publishing) (bool): If set to C(True) then library would
      be optimized for remote publishing. Turn it on if remote publishing is dominant
      use case for this library. Remote publishing means here that publisher and subscribers
      are not the part of the same vCenter SSO domain. Any optimizations could be
      done as result of turning on this optimization during library creation. For
      example, library content could be stored in different format but optimizations
      are not limited to just storage format. Note, that value of this toggle could
      be set only during creation of the library and you would need to migrate your
      library in case you need to change this value (optimize the library for different
      use case).'
    type: dict
  publish_info:
    description:
    - Defines how this library is published so that it can be subscribed to by a remote
      subscribed library. The C(publish_info) defines where and how the metadata for
      this local library is accessible. A local library is only published publically
      if C(publish_info.published) is C(True).
    - 'Valid attributes are:'
    - ' - C(authentication_method) (str): The authentication_method indicates how
      a subscribed library should authenticate to the published library endpoint.'
    - '   - Accepted values:'
    - '     - BASIC'
    - '     - NONE'
    - ' - C(published) (bool): Whether the local library is published.'
    - ' - C(publish_url) (str): The URL to which the library metadata is published
      by the Content Library Service. This value can be used to set the C(subscription_info.subscriptionurl)
      property when creating a subscribed library.'
    - ' - C(user_name) (str): The username to require for authentication.'
    - ' - C(password) (str): The new password to require for authentication.'
    - ' - C(current_password) (str): The current password to verify. This field is
      available starting in vSphere 6.7.'
    - ' - C(persist_json_enabled) (bool): Whether library and library item metadata
      are persisted in the storage backing as JSON files. This flag only applies if
      the local library is published. Enabling JSON persistence allows you to synchronize
      a subscribed library manually instead of over HTTP. You copy the local library
      content and metadata to another storage backing manually and then create a subscribed
      library referencing the location of the library JSON file in the C(subscription_info.subscriptionurl).
      When the subscribed library''s storage backing matches the subscription URL,
      files do not need to be copied to the subscribed library. For a library backed
      by a datastore, the library JSON file will be stored at the path contentlib-{library_id}/lib.json
      on the datastore. For a library backed by a remote file system, the library
      JSON file will be stored at {library_id}/lib.json in the remote file system
      path.'
    type: dict
  server_guid:
    description:
    - The unique identifier of the vCenter server where the library exists.
    type: str
  state:
    choices:
    - absent
    - present
    - publish
    default: present
    description: []
    type: str
  storage_backings:
    description:
    - The list of default storage backings which are available for this library. A
      storage backing defines a default storage location which can be used to store
      files for library items in this library. Some library items, for instance, virtual
      machine template items, support files that may be distributed across various
      storage backings. One or more item files may or may not be located on the default
      storage backing. Multiple default storage locations are not currently supported
      but may become supported in future releases.
    - 'Valid attributes are:'
    - ' - C(type) (str): The {@name Type} specifies the type of the storage backing.'
    - '   - Accepted values:'
    - '     - DATASTORE'
    - '     - OTHER'
    - ' - C(datastore_id) (str): Identifier of the datastore used to store the content
      in the library.'
    - ' - C(storage_uri) (str): URI identifying the location used to store the content
      in the library. The following URI formats are supported: vSphere 6.5 <ul> <li>nfs://server/path?version=4
      (for vCenter Server Appliance only) - Specifies an NFS Version 4 server.</li>
      <li>nfs://server/path (for vCenter Server Appliance only) - Specifies an NFS
      Version 3 server. The nfs://server:/path format is also supported.</li> <li>smb://server/path
      - Specifies an SMB server or Windows share.</li> </ul> vSphere 6.0 Update 1
      <ul> <li>nfs://server:/path (for vCenter Server Appliance only)</li> <li>file://unc-server/path
      (for vCenter Server for Windows only)</li> <li>file:///mount/point (for vCenter
      Server Appliance only) - Local file URIs are supported only when the path is
      a local mount point for an NFS file system. Use of file URIs is strongly discouraged.
      Instead, use an NFS URI to specify the remote file system.</li> </ul> vSphere
      6.0 <ul> <li>nfs://server:/path (for vCenter Server Appliance only)</li> <li>file://unc-server/path
      (for vCenter Server for Windows only)</li> <li>file:///path - Local file URIs
      are supported but strongly discouraged because it may interfere with the performance
      of vCenter Server.</li> </ul>'
    elements: dict
    type: list
  subscription_info:
    description:
    - Defines the subscription behavior for this Library. The C(subscription_info)
      defines how this subscribed library synchronizes to a remote source. Setting
      the value will determine the remote source to which the library synchronizes,
      and how. Changing the subscription will result in synchronizing to a new source.
      If the new source differs from the old one, the old library items and data will
      be lost. Setting C(subscription_info.automaticSyncEnabled) to false will halt
      subscription but will not remove existing cached data.
    - 'Valid attributes are:'
    - ' - C(authentication_method) (str): Indicate how the subscribed library should
      authenticate with the published library endpoint.'
    - '   - Accepted values:'
    - '     - BASIC'
    - '     - NONE'
    - ' - C(automatic_sync_enabled) (bool): Whether the library should participate
      in automatic library synchronization. In order for automatic synchronization
      to happen, the global C(configuration_model.automaticSyncEnabled) option must
      also be true. The subscription is still active even when automatic synchronization
      is turned off, but synchronization is only activated with an explicit call to
      Subscribed Library Sync or Subscribed Item Sync. In other words, manual synchronization
      is still available even when automatic synchronization is disabled.'
    - ' - C(on_demand) (bool): Indicates whether a library item''s content will be
      synchronized only on demand. If this is set to C(True), then the library item''s
      metadata will be synchronized but the item''s content (its files) will not be
      synchronized. The Content Library Service will synchronize the content upon
      request only. This can cause the first use of the content to have a noticeable
      delay. Items without synchronized content can be forcefully synchronized in
      advance using the Subscribed Item Sync call with C(forceSyncContent} set to
      true. Once content has been synchronized, the content can removed with the {@link
      SubscribedItem#evict) call. If this value is set to C(False), all content will
      be synchronized in advance.'
    - ' - C(password) (str): The password to use when authenticating. The password
      must be set when using a password-based authentication method; empty strings
      are not allowed.'
    - ' - C(ssl_thumbprint) (str): An optional SHA-1 hash of the SSL certificate for
      the remote endpoint. If this value is defined the SSL certificate will be verified
      by comparing it to the SSL thumbprint. The SSL certificate must verify against
      the thumbprint. When specified, the standard certificate chain validation behavior
      is not used. The certificate chain is validated normally if this value is not
      set.'
    - ' - C(subscription_url) (str): The URL of the endpoint where the metadata for
      the remotely published library is being served. This URL can be the C(publish_info.publishUrl)
      of the published library (for example, https://server/path/lib.json). If the
      source content comes from a published library with C(publish_info.persistJsonEnabled),
      the subscription URL can be a URL pointing to the library JSON file on a datastore
      or remote file system. The supported formats are: vSphere 6.5 <ul> <li>ds:///vmfs/volumes/{uuid}/mylibrary/lib.json
      (for datastore)</li> <li>nfs://server/path/mylibrary/lib.json (for NFSv3 server
      on vCenter Server Appliance)</li> <li>nfs://server/path/mylibrary/lib.json?version=4
      (for NFSv4 server on vCenter Server Appliance) </li> <li>smb://server/path/mylibrary/lib.json
      (for SMB server)</li> </ul> vSphere 6.0 <ul> <li>file://server/mylibrary/lib.json
      (for UNC server on vCenter Server for Windows)</li> <li>file:///path/mylibrary/lib.json
      (for local file system)</li> </ul> When you specify a DS subscription URL, the
      datastore must be on the same vCenter Server as the subscribed library. When
      you specify an NFS or SMB subscription URL, the C(Storage Backing URI) of the
      subscribed library must be on the same remote file server and should share a
      common parent path with the subscription URL.'
    - ' - C(user_name) (str): The username to use when authenticating. The username
      must be set when using a password-based authentication method. Empty strings
      are allowed for usernames.'
    - ' - C(source_info) (dict): Information about the source published library. This
      field will be set for a subscribed library which is associated with a subscription
      of the published library.'
    - '   - Accepted keys:'
    - '     - source_library (string): Identifier of the published library.'
    - '     - subscription (string): Identifier of the subscription associated with
      the subscribed library.'
    type: dict
  subscriptions:
    description:
    - The list of subscriptions to publish this library to.
    - 'Valid attributes are:'
    - ' - C(subscription) (str): Identifier of the subscription associated with the
      subscribed library.'
    - '   This key is required.'
    elements: dict
    type: list
  type:
    choices:
    - LOCAL
    - SUBSCRIBED
    description:
    - The Library Type defines the type of a Library. The type of a library can be
      used to determine which additional services can be performed with a library.
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
  version:
    description:
    - A version number which is updated on metadata changes. This value allows clients
      to detect concurrent updates and prevent accidental clobbering of data. This
      value represents a number which is incremented every time library properties,
      such as name or description, are changed. It is not incremented by changes to
      a library item within the library, including adding or removing items. It is
      also not affected by tagging the library.
    type: str
author:
- Ansible Cloud Team (@ansible-collections)
version_added: 1.0.0
requirements:
- python >= 3.6
- aiohttp
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "create": {
        "query": {"client_token": "client_token"},
        "body": {
            "creation_time": "creation_time",
            "description": "description",
            "id": "id",
            "last_modified_time": "last_modified_time",
            "last_sync_time": "last_sync_time",
            "name": "name",
            "optimization_info": "optimization_info",
            "publish_info": "publish_info",
            "server_guid": "server_guid",
            "storage_backings": "storage_backings",
            "subscription_info": "subscription_info",
            "type": "type",
            "version": "version",
        },
        "path": {},
    },
    "list": {"query": {}, "body": {}, "path": {}},
    "get": {"query": {}, "body": {}, "path": {"library_id": "library_id"}},
    "update": {
        "query": {},
        "body": {
            "creation_time": "creation_time",
            "description": "description",
            "id": "id",
            "last_modified_time": "last_modified_time",
            "last_sync_time": "last_sync_time",
            "name": "name",
            "optimization_info": "optimization_info",
            "publish_info": "publish_info",
            "server_guid": "server_guid",
            "storage_backings": "storage_backings",
            "subscription_info": "subscription_info",
            "type": "type",
            "version": "version",
        },
        "path": {"library_id": "library_id"},
    },
    "delete": {"query": {}, "body": {}, "path": {"library_id": "library_id"}},
    "publish": {
        "query": {},
        "body": {"subscriptions": "subscriptions"},
        "path": {"library_id": "library_id"},
    },
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

    argument_spec["client_token"] = {"no_log": True, "type": "str"}
    argument_spec["creation_time"] = {"type": "str"}
    argument_spec["description"] = {"type": "str"}
    argument_spec["id"] = {"type": "str"}
    argument_spec["last_modified_time"] = {"type": "str"}
    argument_spec["last_sync_time"] = {"type": "str"}
    argument_spec["library_id"] = {"type": "str"}
    argument_spec["name"] = {"type": "str"}
    argument_spec["optimization_info"] = {"type": "dict"}
    argument_spec["publish_info"] = {"type": "dict"}
    argument_spec["server_guid"] = {"type": "str"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["absent", "present", "publish"],
        "default": "present",
    }
    argument_spec["storage_backings"] = {"type": "list", "elements": "dict"}
    argument_spec["subscription_info"] = {"type": "dict"}
    argument_spec["subscriptions"] = {"type": "list", "elements": "dict"}
    argument_spec["type"] = {"type": "str", "choices": ["LOCAL", "SUBSCRIBED"]}
    argument_spec["version"] = {"type": "str"}

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
    return ("https://{vcenter_hostname}" "/api/content/local-library").format(**params)


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


async def _create(params, session):

    if params["library_id"]:
        _json = await get_device_info(session, build_url(params), params["library_id"])
    else:
        _json = await exists(params, session, build_url(params), ["library_id"])
    if _json:
        if "value" not in _json:  # 7.0.2+
            _json = {"value": _json}
        if "_update" in globals():
            params["library_id"] = _json["id"]
            return await globals()["_update"](params, session)
        return await update_changed_flag(_json, 200, "get")

    payload = prepare_payload(params, PAYLOAD_FORMAT["create"])
    _url = ("https://{vcenter_hostname}" "/api/content/local-library").format(**params)
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
    subdevice_type = get_subdevice_type("/api/content/local-library/{library_id}")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}" "/api/content/local-library/{library_id}"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.delete(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


async def _publish(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["publish"]["query"].keys()
    payload = prepare_payload(params, PAYLOAD_FORMAT["publish"])
    subdevice_type = get_subdevice_type(
        "/api/content/local-library/{library_id}?action=publish"
    )
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}"
        # aa
        "/api/content/local-library/{library_id}?action=publish"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if "value" not in _json:  # 7.0.2
            _json = {"value": _json}
        return await update_changed_flag(_json, resp.status, "publish")


async def _update(params, session):
    payload = prepare_payload(params, PAYLOAD_FORMAT["update"])
    _url = (
        "https://{vcenter_hostname}" "/api/content/local-library/{library_id}"
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
            _json["id"] = params.get("library_id")
            return await update_changed_flag(_json, resp.status, "get")
    async with session.patch(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if "value" not in _json:  # 7.0.2
            _json = {"value": _json}
        _json["id"] = params.get("library_id")
        return await update_changed_flag(_json, resp.status, "update")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
