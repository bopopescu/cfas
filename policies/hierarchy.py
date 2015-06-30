from policies import models
from policies import serializers
import json
import re

def retrieve_attribute_hierarchy(attribute):
    resp = {}

    attribute_serializer = serializers.AttributeSerializer(attribute)
    resp['id'] = attribute_serializer.data['id']
    resp['policy'] = attribute_serializer.data['policy']
    resp['attribute'] = attribute_serializer.data['attribute']
    resp['hierarchy'] = {}
    parents = models.Value.objects.filter(attribute=attribute)
    for parent in parents:
        parent_serializer = serializers.ValueSerializer(parent)
        resp['hierarchy'][parent_serializer.data['value']] = []
        hierarchies = models.Hierarchy.objects.filter(parent=parent)
        hierarchies_serializer = serializers.HierarchySerializer(hierarchies, many=True)
        for hierarchy in hierarchies_serializer.data:
            child = models.Value.objects.get(id=hierarchy['child'])
            child_serializer = serializers.ValueSerializer(child)
            resp['hierarchy'][parent_serializer.data['value']].append(child_serializer.data['value'])

    return(resp)

def list_attribute_hierarchies(policy):
    resp = []

    if policy == None:
        attributes = models.Attribute.objects.all()
    else:
        attributes = models.Attribute.objects.filter(policy=policy)

    for attribute in attributes:
        item = retrieve_attribute_hierarchy(attribute)
        resp.append(item)

    return(resp)

def update_attribute_hierarchy(attribute, policy, data):

    attribute_serializer = serializers.AttributeSerializer(attribute)

    if 'hierarchy' in data:
        # Delete all the accepted values/hierarchies for this attribute (if exists any)
        delete_attribute_hierarchy(attribute_serializer.data, att=False)
        create_hierarchy(attribute_serializer.data, data['hierarchy'])

    if 'attribute' in data:
        attribute.attribute = data['attribute']
    if 'policy' in data:
        attribute.policy = policy
    if 'attribute' in data or 'policy' in data:
        attribute.save()

    resp = retrieve_attribute_hierarchy(attribute)

    return(resp)

def delete_attribute_hierarchy(attribute, att=False):
    try:
        values = models.Value.objects.filter(attribute=attribute['id'])
        for value in values:
            try:
                hierarchies = models.Hierarchy.objects.filter(parent=value)
                for hierarchy in hierarchies:
                    hierarchy.delete()
            except:
                print("No parent found.")
            value.delete()
    except:
        print("No value found.")

    if att:
        attribute.delete()

def create_attribute_hierarchy(data):
    resp = {}

    # Create the attribute object
    att = {}
    att['policy'] = data['policy']
    att['attribute'] = data['attribute']

    serializer = serializers.AttributeSerializer(data=att)
    if serializer.is_valid():
        instance = serializer.save()    # Create the attribute
        attribute = serializer.data
        create_hierarchy(attribute, data['hierarchy'])

        # Set the response
        resp = data
        resp['id'] = attribute['id']

    else:
        print("Attribute Error!")
        print(att)
        print(serializer.errors) # Error!

    return(resp)

def create_hierarchy(attribute, hierarchy):

    for parent, children in hierarchy.items():
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
