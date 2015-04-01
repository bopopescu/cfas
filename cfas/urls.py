from django.conf.urls import patterns, include, url
from django.contrib import admin
#from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from policies import views, models
from policies.serializers import OpenstackPolicySerializer

# Serializers define the API representation.
#class UserSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = User
#        fields = ('url', 'username', 'email', 'is_staff')

class Attribute_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attribute_type
        fields = ('description',)

class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Operator
        fields = ('description',)

class Cloud_platformSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cloud_platform
        fields = ('description', 'accept_negated_conditions', 'operators', 'attribute_types')

class Cloud_providerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cloud_provider
        fields = ('description', 'cloud_platform')

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Policy
        fields = ('description', 'cloud_provider', 'external_policy_ref', 'external_policy')

class And_ruleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.And_rule
        fields = ('policy', 'description', 'enabled', 'conditions')

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Condition
        fields = ('negated', 'attribute_type', 'attribute', 'operator', 'value', 'description')

class PolicyUploadSerializer(OpenstackPolicySerializer):
    class Meta:
        model = models.Policy
        fields = ('description', 'cloud_provider', 'external_policy_ref', 'external_policy')

# ViewSets define the view behavior.
#class UserViewSet(viewsets.ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer

class Attribute_typeViewSet(viewsets.ModelViewSet):
    queryset = models.Attribute_type.objects.all()
    serializer_class = Attribute_typeSerializer

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
router.register(r'attribute_type', views.Attribute_typeViewSet)
router.register(r'operator', views.OperatorViewSet)
router.register(r'cloud_platform', views.Cloud_platformViewSet)
router.register(r'cloud_provider', views.Cloud_providerViewSet)
router.register(r'policy', views.PolicyViewSet)
router.register(r'policy_upload', views.PolicyUploadViewSet)
router.register(r'and_rule', views.And_ruleViewSet)
router.register(r'condition', views.ConditionViewSet)

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
