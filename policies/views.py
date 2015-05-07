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
        resp = {}

        roles = self.request.QUERY_PARAMS.get('roles', None)

        try:
            policy = models.Policy.objects.get(id=pk)
            serializer = PolicySerializer(policy)
            resp['policy'] = {}
            resp['policy'] = serializer.data
            resp['policy']['content'] = openstack_parser.export_openstack_policy(pk)

            #&attributes={"role": ["admin"], "...": []}
            if roles is not None:
                queryset = models.And_rule.objects.filter(policy=pk).all()
                resp['policy']['access'] = openstack_parser.actions_from_roles(queryset, roles)

            return Response(resp)
        except:
            resp['detail'] = "Not found."
            return Response(resp, status=404)

    def list(self, request):
        roles = self.request.QUERY_PARAMS.get('roles', None)
        queryset = models.Policy.objects.all()
        serializer = PolicySerializer(queryset, many=True)
        resp = {}
        resp['policies'] = serializer.data
        return Response(resp)

class And_ruleViewSet(viewsets.ModelViewSet):
    queryset = models.And_rule.objects.all()
    serializer_class = And_ruleSerializer

    def retrieve(self, request, pk=None):
        resp = {}
        try:
            and_rule = models.And_rule.objects.get(id=pk)
            serializer = And_ruleSerializer(and_rule)
            resp['and_rule'] = serializer.data
            return Response(resp)
        except:
            resp['detail'] = "Not found."
            return Response(resp, status=404)

    def list(self, request):
        queryset = models.And_rule.objects.all()

        policy = self.request.QUERY_PARAMS.get('policy', None)
        if policy is not None:
            queryset = queryset.filter(policy=policy)

        serializer = And_ruleSerializer(queryset, many=True)
        resp = {}
        resp['and_rules'] = serializer.data
        return Response(resp)

class ConditionViewSet(viewsets.ModelViewSet):
    queryset = models.Condition.objects.all()
    serializer_class = ConditionSerializer

    def retrieve(self, request, pk=None):
        resp = {}
        try:
            condition = models.Condition.objects.get(id=pk)
            serializer = ConditionSerializer(condition)
            resp['condition'] = serializer.data
            return Response(resp)
        except:
            resp['detail'] = "Not found."
            return Response(resp, status=404)

    def list(self, request):
        queryset = models.Condition.objects.all()
        serializer = ConditionSerializer(queryset, many=True)
        resp = {}
        resp['conditions'] = serializer.data
        return Response(resp)

    def update(self, request, pk=None):
        resp = {}
        resp['detail'] = "Update is not permited on Conditions"
        return Response(resp, status=405)

    def partial_update(self, request, pk=None):
        resp = {}
        resp['detail'] = "Update is not permited on Conditions"
        return Response(resp, status=405)

    def destroy(self, request, pk=None):
        resp = {}
        refd = False
        and_rules = models.And_rule.objects.all()
        for and_rule in and_rules.iterator():
            serializer = And_ruleSerializer(and_rule)
            id = int(pk)
            conds = serializer.data['conditions']
            if id in conds:
                refd = True
                break
        if refd:
            resp['detail'] = "Condition is referenced by one or more And Rules. Can not delete it"
            return Response(resp, status=403)
        else:
            condition = models.Condition.objects.filter(id=pk).delete()
            resp['detail'] = "Condition deleted."
            return Response(resp, status=204)

