from policies import models
from policies import serializers
import json
import re

def list_attribute_hierarchies(policy):
    resp = []

    attributes = models.Attribute.objects.filter(policy=policy)
    for attribute in attributes:
        attribute_serializer = serializers.AttributeSerializer(attribute)
        item = {}
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


