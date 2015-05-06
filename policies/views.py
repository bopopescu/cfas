from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from policies import models
from policies import openstack_parser
from policies.serializers import Attribute_categorySerializer, OperatorSerializer, PolicySerializer
from policies.serializers import Cloud_platformSerializer, Cloud_providerSerializer
from policies.serializers import And_ruleSerializer, ConditionSerializer

#from django.shortcuts import render

# Create your views here.

class Attribute_categoryViewSet(viewsets.ModelViewSet):
    queryset = models.Attribute_category.objects.all()
    serializer_class = Attribute_categorySerializer

class OperatorViewSet(viewsets.ModelViewSet):
    queryset = models.Operator.objects.all()
    serializer_class = OperatorSerializer

class Cloud_platformViewSet(viewsets.ModelViewSet):
    queryset = models.Cloud_platform.objects.all()
    serializer_class = Cloud_platformSerializer

class Cloud_providerViewSet(viewsets.ModelViewSet):
    queryset = models.Cloud_provider.objects.all()
    serializer_class = Cloud_providerSerializer

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = models.Policy.objects.all()
    serializer_class = PolicySerializer

    def perform_destroy(self, instance):
        # Delete And rules for this policy
        models.And_rule.objects.filter(policy = instance.id).delete()
        instance.delete()

    # get /policies/1/openstack = Retrieve the policy from database and return Openstack JSON policy 
    # put /policies/1/openstack = Parse Openstack Policy in the Database and create Openstack structure
    @detail_route(methods=['get','put'])
    def openstack(self, request, pk=None):
        if request.method == 'GET':
            policy = {}
            and_rules = models.And_rule.objects.filter(policy = pk).all()
            for and_rule in and_rules: # For each and_rule
                 if and_rule.enabled:  # If it is enabled
                     service = ""
                     action  = ""
                     condition = ""
                     # TODO: Check if Operator is = (equals). If it is != (not equals), append not in front of value.
                     for cond in and_rule.conditions.all():     # Check all Conditions
                         if cond.attribute == "service":        # Retrieve the Service
                             service = cond.value         
                         elif cond.attribute == "action":       # Retrieve the Action
                             action = cond.value
                         else:                                  # Retrieve the other Conditions (combining with "and"s)
                             if condition == "":
                                 condition = cond.attribute + ":" + cond.value
                             else:
                                 condition = condition + " and " + cond.attribute + ":" + cond.value
                     if service+":"+action in policy:           # Set the policy entry. If already exists, combine with "or"s
                         if condition.find("and") == -1:
                             policy[service+":"+action] = policy[service+":"+action] + " or " + condition
                         else:
                             policy[service+":"+action] = policy[service+":"+action] + " or (" + condition + ")"
                     else:
                         if condition == "":
                             policy[service+":"+action] = condition
                         else:
                             if condition.find("and") == -1:
                                 policy[service+":"+action] = condition
                             else:
                                 policy[service+":"+action] = "(" + condition + ")"
                     
            return Response(policy)

        elif request.method == 'PUT':
            instance = models.Policy.objects.get(id=pk)
            openstack_parser.create_and_rules_and_conditions(instance, request.data['policy'])
            return Response(request.data['policy'])

class And_ruleViewSet(viewsets.ModelViewSet):
    queryset = models.And_rule.objects.all()
    serializer_class = And_ruleSerializer

class ConditionViewSet(viewsets.ModelViewSet):
    queryset = models.Condition.objects.all()
    serializer_class = ConditionSerializer
