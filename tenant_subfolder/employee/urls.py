from django.urls import path,include
from rest_framework import routers

from employee.views import AppPasswordChange, BankViewSet, BranchDetailsViewset,  DispenceViewSet, EmployeeInvoiceViewSet, FuelMasterViewset, MeterReadingViewSet, PreviousMeterReading, VatMasterViewset



router = routers.DefaultRouter()

router.register("generateinvoice", EmployeeInvoiceViewSet, basename="generate_invoice")
router.register("meterreading", MeterReadingViewSet, basename="meter_reading")
router.register("fuel", FuelMasterViewset, basename="fuel_details")
router.register("vat", VatMasterViewset, basename="vat_details")
router.register("bank", BankViewSet, basename="bank")
router.register("dispencer", DispenceViewSet, basename="dispencer")
router.register("company_details", BranchDetailsViewset, basename="company")
router.register("previous_reading", PreviousMeterReading, basename="previous_reading")
router.register("password_change", AppPasswordChange, basename="app_password_change")


urlpatterns = [
    path('', include(router.urls)),
]

