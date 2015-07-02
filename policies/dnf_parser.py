from policies import models
from policies import serializers
from policies import hierarchy
from pyeda.inter import *
import json
import re
import copy

def to_dnf(conds, cnf_rule):
    # Define global variables for each condition as a boolean expression
    gbl = globals()
    for i in range(len(conds)):
        var = "c"+str(i)
        gbl[var] = exprvar(var)

    # Define expression based on subject rules and convert them to DNF
    rule = eval(cnf_rule)
    dnf_rule = rule.to_dnf()

    return dnf_rule

def create_and_rules_and_conditions(instance, policy):
    if 'and_rules' in policy: # If there is no and_rules, do nothing
        # Delete all and rules from the database for a Policy ID
        models.And_rule.objects.filter(policy = instance.id).delete()

        for ar in policy['and_rules']:         # For each and rule...
            # Create and_rule in database, associated to the current policy
            enabled = True
            if 'enabled' in ar:
                enabled = ar['enabled']

            data = {
                     "policy": instance,
                     "description": ar['description'],
                     "enabled": enabled,
                   }

            new_ar = models.And_rule.objects.create(**data)

            # Create conditions in database (if they are not already there), and add them to the new_ar
            if 'conditions' in ar:     # If there is no condition, do nothing
                for c in ar['conditions']:
                    num = models.Condition.objects.filter(attribute=c['attribute'], operator=c['operator'], value=c['value'], type=c['type']).count()
                    if num == 0:
                        new_c = models.Condition.objects.create(**c)
                        new_ar.conditions.add(new_c)
                    elif num == 1:
                        old_c = models.Condition.objects.get(attribute=c['attribute'], operator=c['operator'], value=c['value'], type=c['type'])
                        new_ar.conditions.add(old_c)

def expand_and_rule_using_hierarchy(and_rule):
    attributes = models.Attribute.objects.filter(policy = and_rule.policy.id)

    conds = []    # Expanded list of conditions (from and_rule and from the hierarchy)
    cnf_rule = "" # AND Rule in CNF, eg: (C1 & (C2 | C2a | C2b) & C3) 

    has_ancestors =  False

    for cond in and_rule.conditions.all():

        # Add condition to conds
        cond_serializer = serializers.ConditionSerializer(cond)
        if not cond_serializer.data in conds:
            conds.append(cond_serializer.data)

        # Add condition to rule
        idx = conds.index(cond_serializer.data)
        if cnf_rule == "":
            cnf_rule = "(c"+str(idx) # open parantheses
        else:
            cnf_rule = cnf_rule + " & (c" + str(idx)

        for attribute in attributes:
            # If condition is in attribute list
            if cond.attribute == attribute.attribute:
                child = None
                # Get the value of the child
                try:
                    child = models.Value.objects.get(value = cond.value, attribute = attribute.id)
                except:
                    pass # Child not found

                if child != None:
                    #print(child.value)
                    # Get ancestors list for the child
                    ancestors = hierarchy.list_ancestors(child, [])
                    #print(ancestors)
                    if ancestors != []:
                        has_ancestors = True
                        for ancestor in ancestors:
                            cond_serializer = serializers.ConditionSerializer(cond)
                            new_cond = copy.copy(cond_serializer.data)
                            new_cond['value'] = ancestor
                            new_cond['description'] = "Derived from: " + new_cond['description']

                            # Add ancestor condition to conds
                            if not new_cond in conds:
                                 conds.append(new_cond)

                            # Add ancestor condition to rule
                            cnf_rule = cnf_rule + " | c" + str(conds.index(new_cond))

        cnf_rule = cnf_rule + ")" # close parentheses

    and_rules = []

    and_rule_serializer = serializers.And_ruleSerializer(and_rule)

    if has_ancestors:
        exp = to_dnf(conds, cnf_rule)
#        print(exp)
#        print("================")
        s = str(exp).strip()     # Or(And(c0, c1, c2), And(c0, c1, c3))
        s = re.sub(' ', '', s)   # Or(And(c0,c1,c2),And(c0,c1,c3))
        s = s[3:-1]              # And(c0,c1,c2),And(c0,c1,c3)
        s = s.strip('And')       # (c0,c1,c2),And(c0,c1,c3)
        ands = s.split(",And")   # ['(c0,c1,c2)', '(c0,c1,c3)']
        for a in ands:
            andr = copy.copy(and_rule_serializer.data)
            cs = a.split(",")
            conditions = []
            derived = False
            for c in cs:
                c = re.sub('[,()c]','',c)
                if (c != "") and c is not None:
                    c = int(float(c))
                    cd = copy.copy(conds[c])                    
                    conditions.append(cd)
                    if cd['description'].find("Derived from:") == 0:
                        derived = True
                andr['conditions'] = conditions
                if derived:
                    andr['description'] = "Derived from: " + andr['description']
            and_rules.append(andr)
    else:
        andr = copy.copy(and_rule_serializer.data)
        conditions = []
        for cond in and_rule.conditions.all():     # Check all Conditions
            cond_serializer = serializers.ConditionSerializer(cond)
            conditions.append(cond_serializer.data)
        andr['conditions'] = conditions
        and_rules.append(andr)

    #print(and_rules)

    return and_rules

def export_dnf_policy(policy_id, use_hierarchy):
    policy = {}
    and_rules = models.And_rule.objects.filter(policy = policy_id).all()
    policy_and_rules = []
    for and_rule in and_rules: # For each and_rule
        if and_rule.enabled:  # If it is enabled

            and_rules = expand_and_rule_using_hierarchy(and_rule)

            for and_rule in and_rules:
                policy_and_rules.append(and_rule)

    policy['and_rules'] = policy_and_rules
    return policy

def search(policy_id, data):
    and_rules = models.And_rule.objects.filter(policy = policy_id).all()
    policy_and_rules = []
    for and_rule in and_rules: # For each and_rule
        if and_rule.enabled:  # If it is enabled
            policy_and_rule = {}
            policy_and_rule['id'] = and_rule.id
            policy_and_rule['description'] = and_rule.description
            policy_and_rule['conditions'] = []

            if data['criteria'] == []:
                all_criteria_matched = False
            else:
                all_criteria_matched = True

            one_criterium_matched = False                # Start with none criterium matched
            for cri_cond in data['criteria']:            # For each criterium
                this_criterium_matched = False               # Start not matching this criterium
                for cond in and_rule.conditions.all():       # For each condition
                    if cri_cond["attribute"] == cond.attribute and cri_cond["operator"] == cond.operator:
                        if (cond.type == 'c' and cri_cond["value"] == cond.value) or cond.type == 'v':
                            one_criterium_matched = True     # At least one criterium matched
                            this_criterium_matched = True    # This criterium matched

                    serializer = serializers.ConditionSerializer(cond)
                    if serializer.data not in policy_and_rule["conditions"]:
                        policy_and_rule["conditions"].append(serializer.data)

                all_criteria_matched = all_criteria_matched and this_criterium_matched # Check if all criteria matched

            if (data['combining_rule'] == "or" and one_criterium_matched) or (data['combining_rule'] == "and" and all_criteria_matched):
                policy_and_rules.append(policy_and_rule)

    return policy_and_rules
