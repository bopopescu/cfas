from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from policies import models
from policies import openstack_parser
from policies.serializers import PolicySerializer, And_ruleSerializer, ConditionSerializer

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = models.Policy.objects.all()
    serializer_class = PolicySerializer

    def perform_destroy(self, instance):
        models.And_rule.objects.filter(policy = instance.id).delete() # Delete And rules for this policy
        instance.delete()                                             # Now, delete the policy itself

    def perform_create(self, serializer):
        instance = serializer.save(description=self.request.data['description'])
        if 'policy' in self.request.data:
            openstack_parser.create_and_rules_and_conditions(instance, self.request.data['content'])

    def perform_update(self, serializer):
        instance = serializer.save(description=self.request.data['description'])
        if 'policy' in self.request.data:
            openstack_parser.create_and_rules_and_conditions(instance, self.request.data['content'])

    def retrieve(self, request, pk=None):
        policy = models.Policy.objects.get(id=pk)
        serializer = PolicySerializer(policy)
        resp = {}
        resp['policy'] = serializer.data
        resp['policy']['content'] = openstack_parser.export_openstack_policy(pk)
        return Response(resp)

    def list(self, request):
        queryset = models.Policy.objects.all()
        serializer = PolicySerializer(queryset, many=True)
        resp = {}
        resp['policies'] = serializer.data
        return Response(resp)

class And_ruleViewSet(viewsets.ModelViewSet):
    queryset = models.And_rule.objects.all()
    serializer_class = And_ruleSerializer

    def retrieve(self, request, pk=None):
        and_rule = models.And_rule.objects.get(id=pk)
        serializer = And_ruleSerializer(and_rule)
        resp = {}
        resp['and_rule'] = serializer.data
        return Response(resp)

    def list(self, request):
        queryset = models.And_rule.objects.all()
        serializer = And_ruleSerializer(queryset, many=True)
        resp = {}
        resp['and_rules'] = serializer.data
        return Response(resp)

class ConditionViewSet(viewsets.ModelViewSet):
    queryset = models.Condition.objects.all()
    serializer_class = ConditionSerializer

    def retrieve(self, request, pk=None):
        condition = models.Condition.objects.get(id=pk)
        serializer = ConditionSerializer(condition)
        resp = {}
        resp['condition'] = serializer.data
        return Response(resp)

    def list(self, request):
        queryset = models.Condition.objects.all()
        serializer = ConditionSerializer(queryset, many=True)
        resp = {}
        resp['conditions'] = serializer.data
        return Response(resp)
