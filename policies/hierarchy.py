from policies import models
from policies import serializers
import json
import re

def list_attribute_hierarchies(policy):
    resp = []

    if policy == None:
        attributes = models.Attribute.objects.all()
    else:
        attributes = models.Attribute.objects.filter(policy=policy)

    for attribute in attributes:
        attribute_serializer = serializers.AttributeSerializer(attribute)
        item = {}
        item['policy'] = attribute_serializer.data['policy']
        item['attribute'] = attribute_serializer.data['attribute']
        item['hierarchy'] = {}
        parents = models.Value.objects.filter(attribute=attribute)
        for parent in parents:
            parent_serializer = serializers.ValueSerializer(parent)
            item['hierarchy'][parent_serializer.data['value']] = []
            hierarchies = models.Hierarchy.objects.filter(parent=parent)
            hierarchies_serializer = serializers.HierarchySerializer(hierarchies, many=True)
            for hierarchy in hierarchies_serializer.data:
                child = models.Value.objects.get(id=hierarchy['child'])
                child_serializer = serializers.ValueSerializer(child)
                item['hierarchy'][parent_serializer.data['value']].append(child_serializer.data['value'])
        resp.append(item)

    return(resp)

def create_attribute_hierarchy(data):
    resp = {}
    
    #print(data)
    '''{
     'policy': '2',
     'attribute': 'role', 
     'hierarchy': {'professor': ['lecturer'], 
                   'msc_student': ['undergrad_student'], 
                   'phd_student': ['msc_student'], 
                   'undergrad_student': [], 
                   'admin': ['staff', 'professor'], 
                   'lecturer': ['phd_student'], 
                   'staff': ['phd_student']}
    }'''

    # Retrieve attribute, or create if doesn't exist

    attribute = {}

    try:
        att = models.Attribute.objects.get(attribute=data['attribute'], policy=data['policy'])
        serializer = serializers.AttributeSerializer(att)
        attribute = serializer.data
    except:
        att = {}
        att['policy'] = data['policy']
        att['attribute'] = data['attribute']

        serializer = serializers.AttributeSerializer(data=att)
        if serializer.is_valid():
            instance = serializer.save()
            attribute = serializer.data
        else:
            print("Attribute Error!")
            print(att)
            print(serializer.errors) # Error!

    #resp = attribute # Debug

    # Delete all the accepted values/hierarchies for this attribute (if exists any)

    try:
        values = models.Value.objects.filter(attribute=attribute['id'])
        for value in values:
            try:
                hierarchies = models.Hierarchy.objects.filter(parent=value)
                for hierarchy in hierarchies:
                    hierarchy.delete()
            except:
                print("No parent found")
            value.delete()
    except:
        print("No value found")

    # Create hierarchy for this attribute

    for parent, children in data['hierarchy'].items():
        # Verify if exists parent in values and create if not
        parent_value = {}
        try:
            val = models.Value.objects.get(value=parent, attribute=attribute['id'])
            serializer = serializers.ValueSerializer(val)
            parent_value = serializer.data
        except:
            val = {}
            val['attribute'] = attribute['id']
            val['value'] = parent

        serializer = serializers.ValueSerializer(data=val)
        if serializer.is_valid():
            instance = serializer.save()
            parent_value = serializer.data
        else:
            print("Parent Error!")
            print(val)
            print(serializer.errors) # Error!

        # For all children...
        for child in children:
            # Verify if exists child in values and create if not
            child_value = {}
            try:
                val = models.Value.objects.get(value=child, attribute=attribute['id'])
                serializer = serializers.ValueSerializer(val)
                child_value = serializer.data
            except:
                val = {}
                val['attribute'] = attribute['id']
                val['value'] = child

            serializer = serializers.ValueSerializer(data=val)
            if serializer.is_valid():
                instance = serializer.save()
                child_value = serializer.data
            else:
                print("Child Error!")
                print(val)
                print(serializer.errors) # Error!

            # Create hierarchy Parent-Child

            print(parent_value)
            print(child_value)

            hierarchy_entry = {}
            hierarchy_entry['parent'] = parent_value['id']
            hierarchy_entry['child'] = child_value['id']

            serializer = serializers.HierarchySerializer(data=hierarchy_entry)
            if serializer.is_valid():
                instance = serializer.save()
            else:
                print("Hierarchy Error!")
                print(hierarchy_entry)
                print(serializer.errors) # Error!

    return(data)

