from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import   BranchMangerViewSet, BranchesViewSet, ChangePasswordViewSet, CompanyRegistration, CompanySuspendViewSet, CompanyTokenObtainPairView, EmployeeRegistration, ForgotpasswordViewSet, ProfilePictureUpload
from rest_framework import routers



router = routers.DefaultRouter()

router.register("company", CompanyRegistration, basename="company")
router.register("company_suspend", CompanySuspendViewSet, basename="company-suspend")
router.register("employee", EmployeeRegistration, basename="employee")
router.register("profile_upload", ProfilePictureUpload, basename="profile_upload")
router.register("branches", BranchesViewSet, basename="branches")
router.register("branchmanager", BranchMangerViewSet, basename="branch_manager")
router.register("forgot_password", ForgotpasswordViewSet, basename="forgot_password")
router.register("change_password", ChangePasswordViewSet, basename="change_password")
JWT_SECRET_KEY='JWT_UATHENTICATION'


urlpatterns = [
    path('login/',CompanyTokenObtainPairView.as_view(),name='login'),
    path('', include(router.urls)),

    # path('company/',CompanyRegistration.as_view(),name='company'),
    # path('company/<int:pk>',CompanyRegistration.as_view(),name='company'),
    # path('employee/',EmployeeRegistration.as_view(),name='employee'),
    # path('employee/<int:pk>/',EmployeeRegistration.as_view(),name='employee'),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
