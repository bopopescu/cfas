from rest_framework import viewsets
from policies import models
from policies.serializers import Attribute_categoriesSerializer, OperatorsSerializer, PoliciesSerializer
from policies.serializers import Cloud_platformsSerializer, Cloud_providersSerializer
from policies.serializers import And_rulesSerializer, ConditionsSerializer, PoliciesUploadSerializer

#from django.shortcuts import render

# Create your views here.

class Attribute_categoriesViewSet(viewsets.ModelViewSet):
    queryset = models.Attribute_categories.objects.all()
    serializer_class = Attribute_categoriesSerializer

class OperatorsViewSet(viewsets.ModelViewSet):
    queryset = models.Operators.objects.all()
    serializer_class = OperatorsSerializer

class Cloud_platformsViewSet(viewsets.ModelViewSet):
    queryset = models.Cloud_platforms.objects.all()
    serializer_class = Cloud_platformsSerializer

class Cloud_providersViewSet(viewsets.ModelViewSet):
    queryset = models.Cloud_providers.objects.all()
    serializer_class = Cloud_providersSerializer

class PoliciesViewSet(viewsets.ModelViewSet):
    queryset = models.Policies.objects.all()
    serializer_class = PoliciesSerializer
    def perform_destroy(self, instance):
        # Delete And rules for this policy
        models.And_rules.objects.filter(policy = instance.id).delete()
        instance.delete()

class PoliciesUploadViewSet(viewsets.ModelViewSet):
    queryset = models.Policies.objects.all()
    serializer_class = PoliciesUploadSerializer
    def perform_destroy(self, instance):
        # Delete And rules for this policy
        models.And_rules.objects.filter(policy = instance.id).delete()
        instance.delete()

class And_rulesViewSet(viewsets.ModelViewSet):
    queryset = models.And_rules.objects.all()
    serializer_class = And_rulesSerializer

class ConditionsViewSet(viewsets.ModelViewSet):
    queryset = models.Conditions.objects.all()
    serializer_class = ConditionsSerializer
