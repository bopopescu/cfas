from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from policies import views, models

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Policy
        fields = ('id', 'description')

class And_ruleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.And_rule
        fields = ('id', 'policy', 'description', 'enabled', 'conditions')

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Condition
        fields = ('id', 'attribute', 'operator', 'value', 'type', 'description')

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attribute
        fields = ('id', 'policy', 'attribute')

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Value
        fields = ('id', 'attribute', 'value')

class HierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hierarchy
        fields = ('id', 'parent', 'child')

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = models.Policy.objects.all()
    serializer_class = PolicySerializer

class And_ruleViewSet(viewsets.ModelViewSet):
    queryset = models.And_rule.objects.all()
    serializer_class = And_ruleSerializer

class ConditionViewSet(viewsets.ModelViewSet):
    queryset = models.Condition.objects.all()
    serializer_class = ConditionSerializer

'''class AttributeViewSet(viewsets.ModelViewSet):
    queryset = models.Attribute.objects.all()
    serializer_class = AttributeSerializer

class ValueViewSet(viewsets.ModelViewSet):
    queryset = models.Value.objects.all()
    serializer_class = ValueSerializer'''

router = routers.DefaultRouter()
#router.register(r'v3/policies/values', views.ValueViewSet)
#router.register(r'v3/policies/attributes', views.AttributeViewSet)
router.register(r'v3/policies/and_rules', views.And_ruleViewSet)
router.register(r'v3/policies/conditions', views.ConditionViewSet)
router.register(r'v3/policies', views.PolicyViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^v3/policies/attribute_hierarchies/$', views.HierarchyListView.as_view()),
    url(r'^v3/policies/attribute_hierarchies/(?P<pk>[0-9]+)/$', views.HierarchyDetailView.as_view()),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

#urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cfas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),
#)
