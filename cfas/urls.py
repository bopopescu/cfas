from django.conf.urls import patterns, include, url
from django.contrib import admin
#from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from policies import views, models
#from policies.serializers import OpenstackPolicySerializer

# Serializers define the API representation.
#class UserSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = User
#        fields = ('url', 'username', 'email', 'is_staff')

class Attribute_categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attribute_category
        fields = ('description',)

class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Operator
        fields = ('description',)

class Cloud_platformSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cloud_platform
        fields = ('description', 'accept_negated_conditions', 'operators', 'attribute_categorys')

class Cloud_providerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cloud_provider
        fields = ('description', 'cloud_platform')

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Policy
        fields = ('description', 'cloud_provider')

class And_ruleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.And_rule
        fields = ('policy', 'description', 'enabled', 'conditions')

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Condition
        fields = ('negated', 'attribute_category', 'attribute', 'operator', 'value', 'description')

# ViewSets define the view behavior.
#class UserViewSet(viewsets.ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer

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

class And_ruleViewSet(viewsets.ModelViewSet):
    queryset = models.And_rule.objects.all()
    serializer_class = And_ruleSerializer

class ConditionViewSet(viewsets.ModelViewSet):
    queryset = models.Condition.objects.all()
    serializer_class = ConditionSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)
router.register(r'fpas/attribute_categories', views.Attribute_categoryViewSet)
router.register(r'fpas/operators', views.OperatorViewSet)
router.register(r'fpas/cloud_platforms', views.Cloud_platformViewSet)
router.register(r'fpas/cloud_providers', views.Cloud_providerViewSet)
router.register(r'fpas/and_rules', views.And_ruleViewSet)
router.register(r'fpas/conditions', views.ConditionViewSet)
router.register(r'fpas/policies', views.PolicyViewSet)

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
