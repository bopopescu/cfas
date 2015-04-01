from rest_framework import serializers
from policies import models
from pyeda.inter import *
import json
import re

class Attribute_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attribute_type
        fields = ('description',)

class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Operator
        fields = ('description',)

class Cloud_platformSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cloud_platform
        fields = ('description', 'accept_negated_conditions', 'operators', 'attribute_types')

class Cloud_providerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cloud_provider
        fields = ('description', 'cloud_platform')

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Policy
        fields = ('description', 'cloud_provider', 'external_policy_ref', 'external_policy')

class And_ruleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.And_rule
        fields = ('policy', 'description', 'enabled', 'conditions')

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Condition
        fields = ('negated', 'attribute_type', 'attribute', 'operator', 'value', 'description')

class OpenstackPolicySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(OpenstackPolicySerializer, self).__init__(*args, **kwargs)
        print("init")
        #print(args)
        #print(kwargs)

    def create(self, data):
        print("create")
        print(data)
        #content = data.pop('content')
        return models.Policy.objects.create(**data)

    def parse_conds(self, attr, value, rules, conds):

        # Attr which is <service>:<action> demands two conditions
        if (':' in attr):

            left = attr[:attr.find(':')]
            right = attr[attr.find(':')+1:]

            entry_l = {'attr_type':'R', 'attr': 'service', 'op':'=', 'value': left}
            entry_r = {'attr_type':'A', 'attr': 'action', 'op':'=', 'value': right}

            if entry_l not in conds:
                conds = conds + [entry_l]

            if entry_r not in conds:
                conds = conds + [entry_r]
            
        # ( -L- AND -R- )
        if (' and ' in value):
            left = value[:value.find(' and ')]
            right = value[value.find(' and ')+5:]
            conds = self.parse_conds(attr, left, rules, conds)
            conds = self.parse_conds(attr, right, rules, conds)

        # ( -L- OR -R- )
        elif (' or ' in value):
            left = value[:value.find(' or ')]
            right = value[value.find(' or ')+4:]
            conds = self.parse_conds(attr, left, rules, conds)
            conds = self.parse_conds(attr, right, rules, conds)

        # ( COND:VALUE )
        elif (':' in value):
            left = value[:value.find(':')]
            right = value[value.find(':')+1:]
            if left == "rule":
                conds = self.parse_conds(attr, rules[right], rules, conds)
            else:
                entry = {'attr_type':'S', 'attr': left, 'op':'=', 'value': right}
                if entry not in conds:
                    conds = conds + [entry]                
        elif value is None or value == "":
            pass
        else:
            print("bad condition: ")
            print(attr)
            print(value)
        return conds

    def parse_rules(self, attr, value, rules, conds, rules_conds):

        # ( -L- AND -R- )
        if (' and ' in value):
            left = value[:value.find(' and ')]
            right = value[value.find(' and ')+5:]
            rules_conds_l = self.parse_rules(attr, left, rules, conds, {})
            rules_conds_r = self.parse_rules(attr, right, rules, conds, {})
            rules_conds[attr] = "("+rules_conds_l[attr]+") & ("+rules_conds_r[attr]+")"

        # ( -L- OR -R- )
        elif (' or ' in value):
            left = value[:value.find(' or ')]
            right = value[value.find(' or ')+4:]
            rules_conds_l = self.parse_rules(attr, left, rules, conds, {})
            rules_conds_r = self.parse_rules(attr, right, rules, conds, {})
            rules_conds[attr] = "("+rules_conds_l[attr]+") | ("+rules_conds_r[attr]+")"

        # ( COND:VALUE )
        elif (':' in value):
            left = value[:value.find(':')]
            right = value[value.find(':')+1:]
            if left == "rule":
                rules_conds = self.parse_rules(attr, rules[right], rules, conds, rules_conds)
            else:
                entry = {'attr_type':'S', 'attr': left, 'op':'=', 'value': right}
                if entry not in conds:
                    print("Error. Condition not found: ")
                    print(entry)
                else:
                    #print (str(conds.index(entry))+" - "+str(entry))
                    rules_conds[attr] = "c"+str(conds.index(entry))

        elif value is None or value == "":
            pass
        else:
            print("bad condition: ")
            print(attr)
            print(value)

        return rules_conds

    # Add service/action conditions to policy rules
    def parse_polrules(self, attr, value, rules, conds, rules_conds):
        if (':' in attr):
            left = attr[:attr.find(':')]
            right = attr[attr.find(':')+1:]

            entry_l = {'attr_type':'R', 'attr': 'service', 'op':'=', 'value': left}
            entry_r = {'attr_type':'A', 'attr': 'action', 'op':'=', 'value': right}

            if (entry_l not in conds) or (entry_r not in conds):
                print("Error. Condition not found: ")
                print(entry_l)
                print(entry_r)
            elif attr not in rules_conds:
                rules_conds[attr] = "(c"+str(conds.index(entry_l))+") & (c"+str(conds.index(entry_r))+")"
            else:
                rules_conds[attr] = "(c"+str(conds.index(entry_l))+") & (c"+str(conds.index(entry_r))+") & ("+rules_conds[attr]+")"

        return rules_conds

    def parse(self, ext_pol):

        # Read rules and extract the conditions
        # eg.: [{"attr_type": "S", "attr": "role", "op": "=", "value", "admin"}, ...]
        conds = []

        for attr, value in ext_pol.items():
            conds  = self.parse_conds(attr, value, ext_pol, conds)

        # Read rules and extract the logical expressions
        # eg.: {"admin_required": "C1 OR C2", ...}
        rules_conds = {}

        for attr, value in ext_pol.items():
            rules_conds = self.parse_rules(attr, value, ext_pol, conds, rules_conds)

        # Add service and action rules
        for attr, value in ext_pol.items():
            rules_conds = self.parse_polrules(attr, value, ext_pol, conds, rules_conds)

        return conds, rules_conds

    def to_dnf(self, conds, rules_conds):
        # Define global variables for each condition as a boolean expression
        gbl = globals()
        for i in range(len(conds)):
            var = "c"+str(i)
            gbl[var] = exprvar(var)

        # Define expression based on subject rules and convert them to DNF
        for rk, rv in rules_conds.items():
            gbl[rk] = eval(rv)
            rules_conds[rk] = gbl[rk].to_dnf()

        return rules_conds

    def update(self, instance, data):
        print("update")
        instance.description = data.get('description', instance.description)
        instance.cloud_provider = data.get('cloud_provider', instance.cloud_provider)
        instance.external_policy_ref = data.get('external_policy_ref', instance.external_policy_ref)
        instance.external_policy = data.get('external_policy', instance.external_policy)
        instance.save()

        # Load the variable of the external policy (policy.json content)
        ext_pol=json.loads(instance.external_policy)

        # Parses its content.
        conds, rules_conds = self.parse(ext_pol)

        # Tranform rules to DNF
        rules_conds = self.to_dnf(conds,rules_conds)

        print(conds)
        print(rules_conds)

        return instance

class PolicyUploadSerializer(OpenstackPolicySerializer):
    class Meta:
        model = models.Policy
        fields = ('description', 'cloud_provider', 'external_policy_ref', 'external_policy')
