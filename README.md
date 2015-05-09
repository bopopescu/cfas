Policies
~~~~~~~~

The key use cases we need to cover:

- CRUD on a policy
- CRD on conditions (update is not desired)
- CRUD on and_rules
- List all granted actions if the user satisfies a set of required attributes
  (eg. role:xyz, user_id:%(user_id)s)

Create policy
^^^^^^^^^^^^^

::

    POST /policies

Relationship:
``http://docs.openstack.org/api/openstack-identity/3/rel/policies``

Optional parameters:

- ``content`` (json): If not specified, an empty policy is created.

Request:

::

    {
        "description": "--policy-description--",
        "content": {--optional-policy-json-object--}
    }

Response:

::

    Status: 201 Created

    {
        "policy": {
            "id": "--policy-id--",
            "description": "--policy-description--",
            "links": {
                "self": "http://identity:5000/v3/policies/--policy-id--"
            }
        }
    }

List policies
^^^^^^^^^^^^^

::

    GET /policies

Relationship:
``http://docs.openstack.org/api/openstack-identity/3/rel/policies``

Response:

::

    Status: 200 OK

    {
        "policies": [
            {
                "id": "--policy-id--",
                "description": "--policy-description--",
                "links": {
                    "self": "http://identity:5000/v3/policies/--policy-id--"
                }
            },
            {
                "id": "--policy-id--",
                "description": "--policy-description--",
                "links": {
                    "self": "http://identity:5000/v3/policies/--policy-id--"
                }
            }
        ],
        "links": {
            "self": "http://identity:5000/v3/policies",
            "previous": null,
            "next": null
        }
    }

Get policy
^^^^^^^^^^

::

    GET /policies/{policy_id}

Relationship:
``https://wiki.openstack.org/w/index.php?title=PolicyDatabase``

Response:

::

    Status: 200 OK

    {
        "policy": {
            "id": "--policy-id--",
            "content": {--policy-json-object--},
            "description": "--policy-description--",
            "links": {
                "self": "http://identity:5000/v3/policies/--policy-id--"
            }
        }
    }

Update policy
^^^^^^^^^^^^^

::

    PATCH /policies/{policy_id}

Relationship:
``https://wiki.openstack.org/w/index.php?title=PolicyDatabase``

The request block is the same as the one for create policy, except that only
the attributes that are being updated need to be included.

The content object is optional and also permited in this operation.
When the content is present, the and_rule structure of this policy is deleted
and a new one created from the content.

Response:

::

    Status: 200 OK

    {
        "policy": {
            "id": "--policy-id--",
            "content": {--policy-json-object--},
            "description": "--policy-description--",
            "links": {
                "self": "http://identity:5000/v3/policies/--policy-id--"
            }
        }
    }

Delete policy
^^^^^^^^^^^^^

::

    DELETE /policies/{policy_id}

Relationship:
``https://wiki.openstack.org/w/index.php?title=PolicyDatabase``

Response:

::

    Status: 204 No Content


Create condition
^^^^^^^^^^^^^^^^

::

    POST /policies/conditions

Relationship:
``http://docs.openstack.org/api/openstack-identity/3/rel/policies``


Request:

::

    {
        "description": "--condition-description--",
        "attribute": "--condition-attribute--",
        "operator": "--condition-operator--",
        "value": "--condition-value--"
    }

Response:

::

    Status: 201 Created

    {
        "condition": {
            "id": "--condition-id--",
            "description": "--condition-description--",
            "attribute": "--condition-attribute--",
            "operator": "--condition-operator--",
            "value": "--condition-value--"
            "links": {
                "self": "http://identity:5000/v3/policies/conditions/--condition-id--"
            }
        }
    }

List conditions
^^^^^^^^^^^^^^^

::

    GET /policies/conditions

Relationship:
``http://docs.openstack.org/api/openstack-identity/3/rel/policies``

Response:

::

    Status: 200 OK

    {
        "conditions": [
            {
                "id": "--condition-id--",
                "description": "--condition-description--",
                "attribute": "--condition-attribute--",
                "operator": "--condition-operator--",
                "value": "--condition-value--"
                "links": {
                    "self": "http://identity:5000/v3/policies/conditions/--condition-id--"
                }
            },
            {
                "id": "--condition-id--",
                "description": "--condition-description--",
                "attribute": "--condition-attribute--",
                "operator": "--condition-operator--",
                "value": "--condition-value--"
                "links": {
                    "self": "http://identity:5000/v3/policies/conditions/--condition-id--"
                }
            }
        ],
        "links": {
            "self": "http://identity:5000/v3/policies/conditions",
            "previous": null,
            "next": null
        }
    }

Get condition
^^^^^^^^^^^^^

::

    GET /policies/conditions/{condition_id}

Relationship:
``https://wiki.openstack.org/w/index.php?title=PolicyDatabase``

Response:

::

    Status: 200 OK

    {
        "condition": {
            "id": "--condition-id--",
            "description": "--condition-description--",
            "attribute": "--condition-attribute--",
            "operator": "--condition-operator--",
            "value": "--condition-value--"
            "links": {
                "self": "http://identity:5000/v3/policies/conditions/--condition-id--"
            }
        }
    }

Delete condition
^^^^^^^^^^^^^^^^

::

    DELETE /policies/conditions/{condition_id}

Relationship:
``https://wiki.openstack.org/w/index.php?title=PolicyDatabase``

Response:

::

    Status: 204 No Content

Create and_rule
^^^^^^^^^^^^^^^

::

    POST /policies/and_rules

Relationship:
``http://docs.openstack.org/api/openstack-identity/3/rel/policies``

Request:

::

    {
        "policy": "--policy-id--",
        "description": "--and_rule-description--",
        "enabled": "--boolean--",
        "conditions": [--list-of-condition-ids--]
    }

Response:

::

    Status: 201 Created

    {
        "and_rule": {
            "id": "--and-rule-id--",
            "policy": "--policy-id--",
            "description": "--and_rule-description--",
            "enabled": "--boolean--",
            "conditions": [--list-of-condition-ids--]
            "links": {
                "self": "http://identity:5000/v3/policies/and_rules/--and-rule-id--"
            }
        }
    }

List conditions
^^^^^^^^^^^^^^^

::

    GET /policies/conditions

Relationship:
``http://docs.openstack.org/api/openstack-identity/3/rel/policies``

Response:

::

    Status: 200 OK

    {
        "and_rules": [
            {
                "id": "--and-rule-id--",
                "policy": "--policy-id--",
                "description": "--and_rule-description--",
                "enabled": "--boolean--",
                "conditions": [--list-of-condition-ids--]
                "links": {
                    "self": "http://identity:5000/v3/policies/and_rules/--and-rule-id--"
                }
            },
            {
                "id": "--and-rule-id--",
                "policy": "--policy-id--",
                "description": "--and_rule-description--",
                "enabled": "--boolean--",
                "conditions": [--list-of-condition-ids--]
                "links": {
                    "self": "http://identity:5000/v3/policies/and_rules/--and-rule-id--"
                }
            }
        ],
        "links": {
            "self": "http://identity:5000/v3/policies/and_rules",
            "previous": null,
            "next": null
        }
    }

Get and_rules
^^^^^^^^^^^^^

::

    GET /policies/and_rules/{and_rule_id}

Relationship:
``https://wiki.openstack.org/w/index.php?title=PolicyDatabase``

Response:

::

    Status: 200 OK

    {
        "and_rule": {
            "id": "--and-rule-id--",
            "policy": "--policy-id--",
            "description": "--and_rule-description--",
            "enabled": "--boolean--",
            "conditions": [--list-of-condition-ids--]
            "links": {
                "self": "http://identity:5000/v3/policies/and_rules/--and-rule-id--"
            }
        }
    }

Update and_rule
^^^^^^^^^^^^^^^

::

    PATCH /policies/and_rules/{and_rule_id}

Relationship:
``https://wiki.openstack.org/w/index.php?title=PolicyDatabase``

The request block is the same as the one for create and_rule, except that only
the attributes that are being updated need to be included.

Response:

::

    Status: 200 OK

    {
        "and_rule": {
            "id": "--and-rule-id--",
            "policy": "--policy-id--",
            "description": "--and_rule-description--",
            "enabled": "--boolean--",
            "conditions": [--list-of-condition-ids--]
            "links": {
                "self": "http://identity:5000/v3/policies/and_rules/--and-rule-id--"
            }
        }
    }

Delete and_rule
^^^^^^^^^^^^^^^

::

    DELETE /policies/and_rules/{and_rule_id}

Relationship:
``https://wiki.openstack.org/w/index.php?title=PolicyDatabase``

Response:

::

    Status: 204 No Content

List Granted Actions
^^^^^^^^^^^^^^^^^^^^

::
    GET /policies/actions

Optional parameters:

- ``attributes`` (json): If not specified, assumed user doesn't satisfy any attribute.
  eg: GET /policies/actions?attributes={"attr":[--attr-list--], "attr":[--attr-list--]}

Response:

::

    Status: 200 OK

    {
        "actions": [
            "--service--:--action--"
            "--service--:--action--"
        ]
    }


List Granted Actions in a specific Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::
    GET /policies/{policy_id}/actions

Optional parameters:

- ``attributes`` (json): If not specified, assumed user doesn't satisfy any attribute.
  eg: GET /policies/1/actions?attributes={"attr":[--attr-list--], "attr":[--attr-list--]}

Response:

::

    Status: 200 OK

    {
        "actions": [
            "--service--:--action--"
            "--service--:--action--"
        ]
    }
