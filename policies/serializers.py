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

        #print(conds)
        #print(rules_conds)
        
        # Delete all conditions from the database for a Policy ID
        ands = models.And_rule.objects.filter(policy = instance.id)
        for a in ands:
            models.Condition.objects.filter(and_rule = a.id).delete()
        
        # Delete all and rules from the database for a Policy ID
        models.And_rule.objects.filter(policy = instance.id).delete()

        # Create conditions in the database
        for c in conds:
            #print(c) #{'value': 'list_policies', 'attr': 'action', 'op': '=', 'attr_type': 'A'}

            at = models.Attribute_type.objects.get(description = c['attr_type'])
            op = models.Operator.objects.get(description = c['op'])

            data = {
                      "negated": False,
                      "attribute_type": at,
                      "attribute": c['attr'],
                      "operator": op,
                      "value": c['value'],
                      "description": c['attr']+c['op']+c['value']
                  }
            #print(data)
            models.Condition.objects.create(**data)
            data = {}

        # Create and_rules in database
        for r in rules_conds.items():
            #print(r) # ('identity:delete_vo_role', Or(And(c0, c2, c143), And(c0, c3, c143), And(c0, c4, c143)))
            #print(type(r[1]))

            # Only consider policy rules
            if ':' in r[0]:
                r1 = str(r[1]).strip()
                r1 = re.sub(' ', '', r1)
                #print("R1:"+r1)
                # Add the conditions
                if "Or(" == r1[0:3]:
                    s = r1[3:-1]
                    #print("OR:"+s)
                    s = s.strip('And') # Remove the And in the beginning of the string
                    ands = s.split(",And") # Split using the ,And
                    #print("AS:"+str(ands))
                    count = 0
                    for a in ands:
                        #print("A:"+a)
                        count = count + 1
                        # Insert the AND Rule for the current policy rule
                        data = {
                                 "policy": instance,
                                 "description": r[0]+":"+str(count),
                                 "enabled": True,
                               }
                        #print(data)
                        models.And_rule.objects.create(**data)

                        # Retrieve the AND Rule entry
                        ar = models.And_rule.objects.get(description = r[0]+":"+str(count))

                        cs = a.split(",")
                        #print("CS:"+str(cs))
                        conditions = []
                        for c in cs:
                            c = re.sub('[,()c]','',c)
                            #print("C:"+c)
                            if (c != "") and c is not None:
                                c = int(float(c))
                                cd = conds[c]
                                #print( cd ) # {'attr': 'action', 'attr_type': 'A', 'op': '=', 'value': 'get_trust'}
                                cd = models.Condition.objects.get(description = cd['attr']+cd['op']+cd['value'])
                                ar.conditions.add(cd)

                elif "And(" == r1[0:4]:
                    s = r1[4:-1]
                    #print("A:"+s)
                    cs = s.split(",")
                    conditions = []
                    # Insert the AND Rule for the current policy rule
                    data = {
                             "policy": instance,
                             "description": r[0],
                             "enabled": True,
                           }
                    #print(data)
                    models.And_rule.objects.create(**data)

                    # Retrieve the AND Rule entry
                    ar = models.And_rule.objects.get(description = r[0])

                    for c in cs:
                        c = re.sub('[,()c]','',c)
                        #print("C:"+c)
                        if (c != "") and c is not None:
                            c = int(float(c))
                            cd = conds[c]
                            #print( cd ) # {'attr': 'action', 'attr_type': 'A', 'op': '=', 'value': 'get_trust'}
                            cd = models.Condition.objects.get(description = cd['attr']+cd['op']+cd['value'])
                            ar.conditions.add(cd)
   
                else:
                    print ("OTHER: Error!?")
                    conditions = []
                    c = r1
                    c = strip(',').strip('(').strip(')').strip('c')
                    print(c)

                    # Insert the AND Rule for the current policy rule
                    data = {
                             "policy": instance,
                             "description": r[0],
                             "enabled": True,
                           }
                    #print(data)
                    models.And_rule.objects.create(**data)

                    # Retrieve the AND Rule entry
                    ar = models.And_rule.objects.get(description = r[0])

                    if (c != "") and c is not None:
                        c = int(float(c))
                        cd = conds[c]
                        #print( cd ) # {'attr': 'action', 'attr_type': 'A', 'op': '=', 'value': 'get_trust'}
                        cd = models.Condition.objects.get(description = cd['attr']+cd['op']+cd['value'])
                        ar.conditions.add(cd)
        return instance

    def create(self, data):
        print("create")

        print(data)
        #{'external_policy': '{}', 'description': 'cinder', 'external_policy_ref': 'cinder_policy.json', 'cloud_provider': <Cloud_provider: Cloud_provider object>}

        #content = data.pop('content')
        return models.Policy.objects.create(**data)

class PolicyUploadSerializer(OpenstackPolicySerializer):
    class Meta:
        model = models.Policy
        fields = ('description', 'cloud_provider', 'external_policy_ref', 'external_policy')
