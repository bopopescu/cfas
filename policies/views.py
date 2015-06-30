from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.views import APIView
from policies import models
from policies import dnf_parser
from policies import hierarchy
from policies.serializers import PolicySerializer, And_ruleSerializer, ConditionSerializer\
    , AttributeSerializer, ValueSerializer, HierarchySerializer

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = models.Policy.objects.all()
    serializer_class = PolicySerializer

    def perform_destroy(self, instance):
        models.And_rule.objects.filter(policy = instance.id).delete() # Delete And rules for this policy
        instance.delete()                                             # Now, delete the policy itself

    def perform_create(self, serializer):
        instance = serializer.save(description=self.request.data['description'])
        if 'content' in self.request.data:
            dnf_parser.create_and_rules_and_conditions(instance, self.request.data['content'])

    def perform_update(self, serializer):
        instance = serializer.save()
        if 'content' in self.request.data:
            dnf_parser.create_and_rules_and_conditions(instance, self.request.data['content'])

    def retrieve(self, request, pk=None):
        resp = {}
        try:
            policy = models.Policy.objects.get(id=pk)
            serializer = PolicySerializer(policy)
            resp['policy'] = serializer.data
            resp['policy']['content'] = dnf_parser.export_dnf_policy(pk)
            return Response(resp)
        except:
            resp['detail'] = "Not found."
            return Response(resp, status=404)

    def list(self, request):
        queryset = models.Policy.objects.all()
        serializer = PolicySerializer(queryset, many=True)
        resp = {}
        resp['policies'] = serializer.data
        return Response(resp)

    @detail_route(methods=['post'], url_path='search')
    def search(self, request, pk=None):
        resp = {}
        if not "criteria" in request.data or not "combining_rule" in request.data:
            resp['detail'] = "Missing argument"
            return Response(resp, status=412)
        elif request.data['combining_rule'] == "and" or request.data['combining_rule'] == "or":
            resp['and_rules'] = dnf_parser.search(pk, request.data)
            return Response(resp)
        else:
            resp['detail'] = "Combining Rule not Supported"
            return Response(resp, status=415)

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

        policy = self.request.query_params.get('policy', None)
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

class AttributeViewSet(viewsets.ModelViewSet):
    queryset = models.Attribute.objects.all()
    serializer_class = AttributeSerializer

class ValueViewSet(viewsets.ModelViewSet):
    queryset = models.Value.objects.all()
    serializer_class = ValueSerializer

class HierarchyViewSet(viewsets.ModelViewSet):
    queryset = models.Hierarchy.objects.all()
    serializer_class = ValueSerializer

class HierarchyView(APIView):

    def get(self, request):
        policy = self.request.query_params.get('policy', None)
        resp = {}
        resp['attribute_hierarchies'] = hierarchy.list_attribute_hierarchies(policy)
        return Response(resp)

    def post(self, request, *args, **kwargs):
        resp = {}
        if not 'attribute' in request.data or not 'hierarchy' in request.data or not 'policy' in request.data:
            resp['detail'] = "Missing argument"
            return Response(resp, status=412)
        else:
            try:
                policy = models.Policy.objects.get(id=request.data['policy'])
            except:
                resp['detail'] = "Policy not found."
                return Response(resp, status=404)

            resp = hierarchy.create_attribute_hierarchy(request.data)
            return Response(resp)
