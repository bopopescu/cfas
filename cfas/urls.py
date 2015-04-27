from django.conf.urls import patterns, include, url
from django.contrib import admin
#from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from policies import views, models
from policies.serializers import OpenstackPoliciesSerializer

# Serializers define the API representation.
#class UserSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = User
#        fields = ('url', 'username', 'email', 'is_staff')

class Attribute_categoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attribute_categories
        fields = ('description',)

class OperatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Operators
        fields = ('description',)

class Cloud_platformsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cloud_platforms
        fields = ('description', 'accept_negated_conditions', 'operators', 'attribute_categories')

class Cloud_providersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cloud_providers
        fields = ('description', 'cloud_platform')

class PoliciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Policies
        fields = ('description', 'cloud_provider', 'external_policy')

class And_rulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.And_rules
        fields = ('policy', 'description', 'enabled', 'conditions')

class ConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Conditions
        fields = ('negated', 'attribute_category', 'attribute', 'operator', 'value', 'description')

class PoliciesUploadSerializer(OpenstackPoliciesSerializer):
    class Meta:
        model = models.Policies
        fields = ('description', 'cloud_provider', 'external_policy')

# ViewSets define the view behavior.
#class UserViewSet(viewsets.ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer

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

class PoliciesUploadViewSet(viewsets.ModelViewSet):
    queryset = models.Policies.objects.all()
    serializer_class = PoliciesUploadSerializer

class And_rulesViewSet(viewsets.ModelViewSet):
    queryset = models.And_rules.objects.all()
    serializer_class = And_rulesSerializer

class ConditionsViewSet(viewsets.ModelViewSet):
    queryset = models.Conditions.objects.all()
    serializer_class = ConditionsSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)
router.register(r'attribute_categories', views.Attribute_categoriesViewSet)
router.register(r'operators', views.OperatorsViewSet)
router.register(r'cloud_platforms', views.Cloud_platformsViewSet)
router.register(r'cloud_providers', views.Cloud_providersViewSet)
router.register(r'policies', views.PoliciesViewSet)
router.register(r'policies_upload', views.PoliciesUploadViewSet)
router.register(r'and_rules', views.And_rulesViewSet)
router.register(r'conditions', views.ConditionsViewSet)

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
