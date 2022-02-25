from django.urls import path, include


# from . import views
from .views import AllSessionCloseViewSet, AppPasswordChange, BankViewSet, BranchBankViewSet, BranchCustomersViewSet, BranchEmployeesViewSet, BranchExpenseViewSet, BranchInvoicesViewSet, BranchReciptViewSet, BranchSupplierViewSet, CashMasterViewSet, CustomerBalanceViewSet, CustomerViewSet, DailySessionViewSet, DashboardViewSet, DebtorsReportViewSet, DepositReportViewSet, DepositViewSet,  DispenceViewSet, EmployeeSaleReportViewSet, ExpenseReportViewSet, ExpenseViewSet, FuelRegistrationViewSet, FuelStockViewSet, IncomeReportViewSet,  InvoiceViewSet, MeterReadingReportViewSet,  OwnerViewSet, PaymentDetailsViewSet, PaymentDueViewSet, PaymentInReportViewSet, PaymentOutReportViewSet, PendingBalance, PurchasePendingBalance, PurchaseReportViewSet, ReciptViewSet, SaleReportViewSet, SessionAccountReportViewSet, SessionReportViewSet, SingleAccountViewSet, SupplierReportViewSet, SupplierViewSet, SuspendSupplierViewSet, VatRegistrationViewset
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers


router = routers.DefaultRouter()


router.register("customer", CustomerViewSet, basename="customer")
router.register("supplier", SupplierViewSet, basename="supplier")
router.register("suspend_supplier", SuspendSupplierViewSet,
                basename="suspend_supplier")
router.register("invoice", InvoiceViewSet, basename="invoice")
router.register("recipt", ReciptViewSet, basename="recipt")
router.register("vatmaster", VatRegistrationViewset, basename="vat_master")
router.register("fuelmaster", FuelRegistrationViewSet, basename="fuel_master")
router.register("bank", BankViewSet, basename="bank")
router.register("owner", OwnerViewSet, basename="owner")
router.register("deposit", DepositViewSet, basename="deposit")
router.register("dispense", DispenceViewSet, basename="dispense")
router.register("fuel_stock", FuelStockViewSet, basename="fuel_stock")
router.register("report/sale", SaleReportViewSet, basename="sale_report")
router.register("report/purchase", PurchaseReportViewSet,
                basename="purchase_report")
router.register("report/debtors", DebtorsReportViewSet,
                basename="debtors_statement")
router.register("report/creditors", SupplierReportViewSet,
                basename="supplier_statement")
router.register("sale/employee", EmployeeSaleReportViewSet,
                basename="sale_employee_report")
router.register("report/income", IncomeReportViewSet, basename="income")
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
router.register("session", DailySessionViewSet, basename="session")
router.register("cashmaster", CashMasterViewSet, basename="cash_master")
router.register("expense", ExpenseViewSet, basename="expense_invoice")
router.register("dashboard", DashboardViewSet, basename="dashboard")
router.register("branch_customers", BranchCustomersViewSet,
                basename="barnch_customers")
router.register("branch_suppliers", BranchSupplierViewSet,
                basename="barnch_suppliers")
router.register("branch_employees", BranchEmployeesViewSet,
                basename="barnch_employees")
router.register("branch_bankac", BranchBankViewSet, basename="barnch_bankac")
router.register("single_account", SingleAccountViewSet,
                basename="single_bank_account")
router.register("old_balance", PendingBalance, basename="old_balance_account")
router.register("all_session_close", AllSessionCloseViewSet,
                basename="all_session_close")
router.register("branch_sale_invoices", BranchInvoicesViewSet,
                basename="branch_invoice")
router.register("branch_expense_invoices",
                BranchExpenseViewSet, basename="branch_expense")
router.register("branch_purchase_invoices", BranchReciptViewSet,
                basename="branch_purchase_invoice")
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
