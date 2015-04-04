from rest_framework import viewsets
from policies import models
from policies.serializers import Attribute_categorySerializer, OperatorSerializer, PolicySerializer
from policies.serializers import Cloud_platformSerializer, Cloud_providerSerializer
from policies.serializers import And_ruleSerializer, ConditionSerializer, PolicyUploadSerializer

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

class PolicyUploadViewSet(viewsets.ModelViewSet):
    queryset = models.Policy.objects.all()
    serializer_class = PolicyUploadSerializer
    def perform_destroy(self, instance):

        # Delete And rules for this policy
        models.And_rule.objects.filter(policy = instance.id).delete()

        instance.delete()

class And_ruleViewSet(viewsets.ModelViewSet):
    queryset = models.And_rule.objects.all()
    serializer_class = And_ruleSerializer

class ConditionViewSet(viewsets.ModelViewSet):
    queryset = models.Condition.objects.all()
    serializer_class = ConditionSerializer
