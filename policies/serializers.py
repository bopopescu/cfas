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

    #subject_rules => Object with policy.json lines for subject rules
    #subject_rules_cond => New JSON object. Will be populated with subject rules in conditional way
    #conds => New JSON set object. Will be populated with the conditions

    def parse_conds(self, attr, value, subject_rules, conds):
        # ( -L- AND -R- )
        if (' and ' in value):
            left = value[:value.find(' and ')]
            right = value[value.find(' and ')+5:]
            conds = self.parse_conds(attr, left, subject_rules, conds)
            conds = self.parse_conds(attr, right, subject_rules, conds)

        # ( -L- OR -R- )
        elif (' or ' in value):
            left = value[:value.find(' or ')]
            right = value[value.find(' or ')+4:]
            conds = self.parse_conds(attr, left, subject_rules, conds)
            conds = self.parse_conds(attr, right, subject_rules, conds)

        # ( COND:VALUE )
        elif (':' in value):
            left = value[:value.find(':')]
            right = value[value.find(':')+1:]
            if left == "rule":
                conds = self.parse_conds(attr, subject_rules[right], subject_rules, conds)
            else:
                entry = {'attr_type':'S', 'attr': left, 'op':'=', 'value': right}
                if entry not in conds:
                    conds = conds + [entry]                
        else:
            print("bad condition: "+value)
        return conds

    def parse_subrules(self, attr, value, subject_rules, conds, subject_rules_conds):
        # ( -L- AND -R- )
        if (' and ' in value):
            left = value[:value.find(' and ')]
            right = value[value.find(' and ')+5:]
            subject_rules_conds_l = self.parse_subrules(attr, left, subject_rules, conds, {})
            subject_rules_conds_r = self.parse_subrules(attr, right, subject_rules, conds, {})
            subject_rules_conds[attr] = "("+subject_rules_conds_l[attr]+") & ("+subject_rules_conds_r[attr]+")"

        # ( -L- OR -R- )
        elif (' or ' in value):
            left = value[:value.find(' or ')]
            right = value[value.find(' or ')+4:]
            subject_rules_conds_l = self.parse_subrules(attr, left, subject_rules, conds, {})
            subject_rules_conds_r = self.parse_subrules(attr, right, subject_rules, conds, {})
            subject_rules_conds[attr] = "("+subject_rules_conds_l[attr]+") | ("+subject_rules_conds_r[attr]+")"

        # ( COND:VALUE )
        elif (':' in value):
            left = value[:value.find(':')]
            right = value[value.find(':')+1:]
            if left == "rule":
                subject_rules_conds = self.parse_subrules(attr, subject_rules[right], subject_rules, conds, subject_rules_conds)
            else:
                entry = {'attr_type':'S', 'attr': left, 'op':'=', 'value': right}
                if entry not in conds:
                    print("Error. Condition not found: "+entry)
                #print (str(conds.index(entry))+" - "+str(entry))
                subject_rules_conds[attr] = "c"+str(conds.index(entry))
        else:
            print("bad condition: "+value)
        return subject_rules_conds

    def parse(self, subject_rules, conds, subject_rules_conds):
        for attr, value in subject_rules.items():
            conds  = self.parse_conds(attr, value, subject_rules, conds)
        for attr, value in subject_rules.items():
            subject_rules_conds = self.parse_subrules(attr, value, subject_rules, conds, subject_rules_conds)
        return conds, subject_rules_conds

    def update(self, instance, data):
        print("update")
        instance.description = data.get('description', instance.description)
        instance.cloud_provider = data.get('cloud_provider', instance.cloud_provider)
        instance.external_policy_ref = data.get('external_policy_ref', instance.external_policy_ref)
        instance.external_policy = data.get('external_policy', instance.external_policy)
        instance.save()
        ext_pol=json.loads(instance.external_policy)
        #print(ext_pol)
        #read lines from json and classify them in Subject Rules and Policy Rules

        subject_rules = {}
        policy_rules = {}

        for attr, value in ext_pol.items():
            if (':' in attr):
                policy_rules[attr] = value
            else:
                subject_rules[attr] = value

        #print(subject_rules)

        conds = []
        # eg.: [{"attr_type": "S", "attr": "role", "op": "=", "value", "admin"}, ...]
        subject_rules_conds = {}
        # eg.: {"admin_required": "C1 OR C2", ...}

        conds, subject_rules_conds = self.parse(subject_rules, conds, subject_rules_conds)

        print(conds)
        print(subject_rules_conds)

        # Define global variables for each condition as a boolean expression
        gbl = globals()
        for i in range(len(conds)):
            var = "c"+str(i)
            gbl[var] = exprvar(var)

        # Define expression based on subject rules
        for rk, rv in subject_rules_conds.items():
            gbl[rk] = eval(rv)

        print(vo_admin.to_dnf())

        return instance

class PolicyUploadSerializer(OpenstackPolicySerializer):
    class Meta:
        model = models.Policy
        fields = ('description', 'cloud_provider', 'external_policy_ref', 'external_policy')
