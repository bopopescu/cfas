from policies import models
from policies import serializers
import json
import re

def export_dnf_policy(policy_id):
    policy = {}
    and_rules = models.And_rule.objects.filter(policy = policy_id).all()
    policy_and_rules = []
    for and_rule in and_rules: # For each and_rule
        if and_rule.enabled:  # If it is enabled
            policy_and_rule = {}
            policy_and_rule['id'] = and_rule.id
            policy_and_rule['description'] = and_rule.description
            policy_and_rule['conditions'] = []
            for cond in and_rule.conditions.all():     # Check all Conditions
                serializer = serializers.ConditionSerializer(cond)
                policy_and_rule['conditions'].append(serializer.data)
            policy_and_rules.append(policy_and_rule)
    policy['and_rules'] = policy_and_rules
    return policy
