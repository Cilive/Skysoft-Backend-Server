from django.urls import path, include


from . import views
from rest_framework import routers
from .views import AppPasswordChange, BranchBankViewSet, BranchCustomersViewSet, BranchSupplierViewSet, CustomerBalanceViewSet, DepositReportViewSet, ExpenseReportViewSet, FuelStockViewSet, IncomeReportViewSet, MeterReadingReportViewSet, PaymentDetailsViewSet, PaymentDueViewSet, PaymentInReportViewSet, PaymentOutReportViewSet, PendingBalance, PurchasePendingBalance, SessionAccountReportViewSet, SessionReportViewSet, SingleAccountViewSet, SupplierReportViewSet, DebtorsReportViewSet, OwnerViewSet, PurchaseReportViewSet, SaleReportViewSet, ExpenseViewSet, CashMasterViewSet, CustomerViewSet, BankViewSet, DailySessionViewSet, DashboardViewSet, DepositViewSet, DispenceViewSet, EmployeeRegistration, FuelRegistrationViewSet, InvoiceViewSet, ReciptViewSet, SupplierViewSet, VatRegistrationViewset


router = routers.DefaultRouter()


router.register("customer", CustomerViewSet, basename="customer")
router.register("supplier", SupplierViewSet, basename="supplier")
router.register("invoice", InvoiceViewSet, basename="invoice")
router.register("recipt", ReciptViewSet, basename="recipt")
router.register("vatmaster", VatRegistrationViewset, basename="vat_master")
router.register("fuelmaster", FuelRegistrationViewSet, basename="fuel_master")
router.register("fuel_stock", FuelStockViewSet, basename="fuel_stock")
router.register("bank", BankViewSet, basename="bank")
router.register("owner", OwnerViewSet, basename="owner")
router.register("deposit", DepositViewSet, basename="deposit")
router.register("dispense", DispenceViewSet, basename="dispense")
router.register("cashmaster", CashMasterViewSet, basename="cash_master")
router.register("session", DailySessionViewSet, basename="session")
router.register("employee", EmployeeRegistration, basename="employee")
router.register("dashboard", DashboardViewSet, basename="dashboard")
router.register("expense", ExpenseViewSet, basename="expense_invoice")
router.register("report/sale", SaleReportViewSet, basename="sale_report")
router.register("report/expense", ExpenseReportViewSet, basename="sale_report")
router.register("report/purchase", PurchaseReportViewSet,
                basename="purchase_report")
router.register("report/debtors", DebtorsReportViewSet,
                basename="debtors_statement")
router.register("report/creditors", SupplierReportViewSet,
                basename="supplier_statement")
router.register("report/expense", ExpenseReportViewSet, basename="expense")
router.register("report/meter_reading", MeterReadingReportViewSet,
                basename="meter_reading_report")
router.register("report/customer_balance",
                CustomerBalanceViewSet, basename="customer_balance")
router.register("report/deposit", DepositReportViewSet,
                basename="deposit_report")
router.register("report/payment_details",
                PaymentDetailsViewSet, basename="payment_details")
router.register("report/payment_due", PaymentDueViewSet,
                basename="payment_due")
router.register("report/payment_in", PaymentInReportViewSet,
                basename="payment_in_report")
router.register("report/payment_out", PaymentOutReportViewSet,
                basename="payment_out_report")
# router.register("sale/employee", EmployeeSaleReportViewSet, basename="sale_employee_report")
router.register("report/income", IncomeReportViewSet, basename="income")
router.register("branch_customers", BranchCustomersViewSet,
                basename="barnch_customers")
router.register("branch_suppliers", BranchSupplierViewSet,
                basename="barnch_suppliers")
router.register("branch_bankac", BranchBankViewSet, basename="barnch_bankac")
router.register("single_account", SingleAccountViewSet,
                basename="single_bank_account")
router.register("old_balance", PendingBalance, basename="old_balance_account")
router.register("old_balance_purchase", PurchasePendingBalance,
                basename="old_balance_purchase")
router.register("session_report", SessionReportViewSet,
                basename="session_report"),
router.register("accounts_report", SessionAccountReportViewSet,
                basename="session_account_report"),
router.register("password_change", AppPasswordChange,
                basename="app_password_change")


urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
