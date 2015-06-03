from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers, serializers, viewsets
from policies import views, models

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Policy
        fields = ('description')

class And_ruleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.And_rule
        fields = ('policy', 'description', 'enabled', 'conditions')

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Condition
        fields = ('negated', 'attribute', 'operator', 'value', 'type', 'description')

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = models.Policy.objects.all()
    serializer_class = PolicySerializer

class And_ruleViewSet(viewsets.ModelViewSet):
    queryset = models.And_rule.objects.all()
    serializer_class = And_ruleSerializer

class ConditionViewSet(viewsets.ModelViewSet):
    queryset = models.Condition.objects.all()
    serializer_class = ConditionSerializer

router = routers.DefaultRouter()
router.register(r'v3/policies/and_rules', views.And_ruleViewSet)
router.register(r'v3/policies/conditions', views.ConditionViewSet)
router.register(r'v3/policies', views.PolicyViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

#urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cfas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),
#)
