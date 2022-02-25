from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics, status
from django.db import connection
import datetime
from django.db.models import Q
from rest_framework import serializers

from django.db.models.aggregates import Sum


from rest_framework.permissions import IsAuthenticated
from company.models import AccountLedger, BankAccountMaster, CashMaster, Contact, DailySession, Deposit, Dispence, FuelMaster, FuelStock, Invoice, MeterReading, Owner, VatMaster
from company.serielizer import ChangePasswordSerializer

from .serielizer import BankAccountListSerielizer, CustomerListSerielizer, DebtorsReportSerializer, DepositReportSerializer, ExpenseCreateSerializer, DashboardSerielzer, EmployeeSerializer, EmployeeRegistrationSerializer, EmployeeUpdateSerializer, ExpenseListSerielizer, ExpenseReportSerializer, FuelStockCreateSerializer, FuelStockSerializer, IncomeReportSerializer, InvoiceListSerielizer, MeterReadingReporSerielizer, PaymentDueReportSerializer, PaymentInReportSerializer, PaymentOutReportSerializer, PurchaseReportSerializer, ReciptUpdateSerializer, BankCreateSerializer, BankSerializer, CashMasterCreateSerializer, CustomerCraeteSerializer, CustomerSerializer, DepositCreateSerializer, DepositSerializer, DispenceCreateSerializer, DispenceSerializer, FirstSessionCreateSerializer, FuelListSerializer,  FuelSerializer, InvoiceCreateSerializer,  InvoiceUpdateSerializer, OwnerCreateSerializer, OwnerSerializer, OwnerUpdateSerializer, ReciptCreateSerializer, ReciptSerializer, SaleReportSerializer, SessionAccountReportSerializer, SessionCloseResultSerielizer, SessionCloseSerielizer, SessionCreateSerializer, SessionListViewSerielizer, SessionReportSerializer, SupplierCreateSerializer, SupplierListSerielizer, SupplierReportSerializer, SupplierSerializer, VatRegistrationSerializer, VatSerializer
from administrator.models import BranchManager, Branches, Company, Employee
from .permissions import (IsManager)


class EmployeeRegistration(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]
    queryset = Employee.objects.all()
    serializer_class = EmployeeRegistrationSerializer

    def list(self, request):
        try:
            manger = BranchManager.objects.get(user=request.user)
            employee = Employee.objects.filter(company=Company.objects.get(
                id=manger.company_id), branches=Branches.objects.get(id=manger.branches_id))
            serializer = EmployeeSerializer(
                employee, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, format=None):
        print("request data =============================>", request.data)
        # user=self.context['request'].user
        print("request user from toke", request.user)
        try:
            serializer = EmployeeRegistrationSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
            return Response({'msg': 'Invalid data', 'error': serializer.errors}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(e)
            return Response({'message': "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            employee = Employee.objects.filter(pk=pk)
            if not employee:
                return Response({'message': "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = EmployeeSerializer(
                employee[0], context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            employee = Employee.objects.filter(pk=pk)
            if not employee:
                return Response({'message': "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = EmployeeUpdateSerializer(
                employee[0], data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            employee = Employee.objects.filter(pk=pk)
            if not employee:
                return Response({'message': "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
            print(connection.queries)

            employee[0].delete()
            print(connection.queries)

            return Response({'msg': 'Success'}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def create(self, request):
        try:
            serializer = CustomerCraeteSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            manger = BranchManager.objects.get(user=request.user)

            customer = Contact.objects.filter(type=1, company=Company.objects.get(
                id=manger.company_id), branches=Branches.objects.get(id=manger.branches_id))
            serializer = CustomerSerializer(
                customer, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            manger = BranchManager.objects.get(user=request.user)

            customer = Contact.objects.filter(type=1, pk=pk, company=Company.objects.get(
                id=manger.company_id), branches=Branches.objects.get(id=manger.branches_id))
            if not customer:
                return Response({'message': "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CustomerSerializer(
                customer[0], context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            manger = BranchManager.objects.get(user=request.user)

            customer = Contact.objects.filter(type=1, pk=pk, company=Company.objects.get(
                id=manger.company_id), branches=Branches.objects.get(id=manger.branches_id))
            if not customer:
                return Response({'message': "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CustomerSerializer(
                customer[0], data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            customer = Contact.objects.filter(pk=pk, type=1)
            if not customer:
                return Response({'message': "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
            customer[0].delete()
            return Response({'msg': 'Success'}, status.HTTP_200_OK)

        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SupplierViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def create(self, request):
        try:
            serializer = SupplierCreateSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            manger = BranchManager.objects.get(user=request.user)

            customer = Contact.objects.filter(type=2, company=Company.objects.get(
                id=manger.company_id), branches=Branches.objects.get(id=manger.branches_id))
            serializer = SupplierSerializer(
                customer, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            manger = BranchManager.objects.get(user=request.user)

            customer = Contact.objects.filter(type=2, pk=pk, company=Company.objects.get(
                id=manger.company_id), branches=Branches.objects.get(id=manger.branches_id))
            if not customer:
                return Response({'message': "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = SupplierSerializer(
                customer[0], context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            manger = BranchManager.objects.get(user=request.user)

            customer = Contact.objects.filter(type=2, pk=pk, company=Company.objects.get(
                id=manger.company_id), branches=Branches.objects.get(id=manger.branches_id))
            if not customer:
                return Response({'message': "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = SupplierSerializer(
                customer[0], data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            customer = Contact.objects.filter(pk=pk, type=2)
            if not customer:
                return Response({'message': "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
            customer[0].delete()
            return Response({'msg': 'Success'}, status.HTTP_200_OK)

        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class InvoiceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            manger = BranchManager.objects.get(user=request.user)
            # request.data['branches']=manger.branches_id

            print("Payment Type", request.data['payment_type'])
            date_today = datetime.date.today()
            print("date today", date_today)
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            print(today_min, today_max)
            session = DailySession.objects.filter(
                branches_id=manger.branches_id, date__range=(today_min, today_max), status=False)
            # session=DailySession.objects.filter(branches_id=request.data['branches'])
            print("session", session.query)
            print(connection.queries)
            print("last session command woeking", session)
            if session:
                request.data['session_id'] = session[0].id
                print("matching session found for today")
                if int(request.data['payment_type']) == 2:
                    print("request", request)
                    print("request data", request.data)
                    print("Paid Amount", request.data['paid_amt'])
                    bank_id = request.data['bank_ac_id']
                    if bank_id:
                        account_balance = BankAccountMaster.objects.get(
                            pk=bank_id)
                        print("Rbank account", account_balance)
                        print("Rbank account", account_balance.balance)
                        bank_balance = float(account_balance.balance)
                        print("is default bank account",
                              account_balance.is_default)
                        if account_balance.is_default:
                            serializer = InvoiceCreateSerializer(data=request.data, context={
                                                                 "request": request, "data": request.data})
                            if serializer.is_valid():
                                serializer.save()
                                saved_paid_amt = float(
                                    serializer.data['paid_amt'])
                                saved_qty = float(serializer.data['qty'])
                                print("saved purchase quantity", saved_qty)
                                saved_fuel = float(serializer.data['fuel'])
                                # branches=int(serializer.data['branches'])
                                try:
                                    print("fuel stock updation")
                                    fuel_stock = FuelStock.objects.get(
                                        Fuel=saved_fuel, branches=manger.branches_id)
                                    if fuel_stock:
                                        new_current_stock = float(
                                            fuel_stock.qty)-saved_qty
                                        FuelStock.objects.filter(Fuel=saved_fuel, branches=manger.branches_id).update(
                                            qty=new_current_stock)
                                except FuelStock.DoesNotExist:
                                    print("no matching Fuel found")
                                    return Response({'msg': 'Fuel not found'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                                sale_balance = bank_balance+saved_paid_amt
                                balance_amt = Invoice.objects.filter(
                                    type=2, payment_type=2, bank=bank_id).aggregate(Sum('balance_amt'))
                                # print(connection.queries)
                                print("balance amount", balance_amt)
                                total_bank_debit = balance_amt['balance_amt__sum']
                                print("current debit balance=",
                                      account_balance.debit_balance)
                                print("Account responsible", bank_id)
                                print("total bank debit balance=",
                                      total_bank_debit)
                                print("bank balance amout after Sale ",
                                      sale_balance,)
                                BankAccountMaster.objects.filter(pk=bank_id).update(
                                    balance=sale_balance, debit_balance=total_bank_debit)
                                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                        else:
                            serializer = InvoiceCreateSerializer(data=request.data, context={
                                                                 "request": request, "data": request.data})
                            if serializer.is_valid():
                                serializer.save()
                                saved_paid_amt = float(
                                    serializer.data['paid_amt'])
                                saved_qty = float(serializer.data['qty'])
                                print("saved purchase quantity", saved_qty)
                                saved_fuel = float(serializer.data['fuel'])
                                # branches=int(serializer.data['branches'])
                                try:
                                    print("fuel stock updation")
                                    fuel_stock = FuelStock.objects.get(
                                        Fuel=saved_fuel, branches=manger.branches_id)
                                    if fuel_stock:
                                        new_current_stock = float(
                                            fuel_stock.qty)-saved_qty
                                        FuelStock.objects.filter(Fuel=saved_fuel, branches=manger.branches_id).update(
                                            qty=new_current_stock)
                                except FuelStock.DoesNotExist:
                                    print("no matching Fuel found")
                                    return Response({'msg': 'Fuel not found'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                                sale_balance = bank_balance+saved_paid_amt
                                balance_amt = Invoice.objects.filter(
                                    type=2, payment_type=2, bank=bank_id).aggregate(Sum('balance_amt'))
                                print(connection.queries)
                                print("balance amount", balance_amt)
                                total_bank_debit = balance_amt['balance_amt__sum']
                                print("current debit balance=",
                                      account_balance.debit_balance)
                                print("Account responsible", bank_id)
                                print("total bank debit balance=",
                                      total_bank_debit)
                                print("bank balance amout after Sale ",
                                      sale_balance,)
                                BankAccountMaster.objects.filter(pk=bank_id).update(
                                    balance=sale_balance, debit_balance=total_bank_debit)
                                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                elif int(request.data['payment_type']) == 1:
                    print(
                        "============================================payment type is cash=============================")
                    print("request data", request.data)
                    print("Paid Amount", request.data['paid_amt'])
                    branch_id = manger.branches_id
                    if branch_id:
                        cash_account = CashMaster.objects.get(
                            branches=branch_id)
                        print("Cash account", cash_account)
                        print("cash account balance", cash_account.balance)
                        cash_balance = float(cash_account.balance)
                        serializer = InvoiceCreateSerializer(data=request.data, context={
                                                             "request": request, "data": request.data})
                        if serializer.is_valid():
                            serializer.save()
                            saved_paid_amt = float(serializer.data['paid_amt'])
                            saved_qty = float(serializer.data['qty'])
                            print("saved purchase quantity", saved_qty)
                            saved_fuel = float(serializer.data['fuel'])
                            try:
                                print("fuel stock updation")
                                fuel_stock = FuelStock.objects.get(
                                    Fuel=saved_fuel, branches=manger.branches_id)
                                if fuel_stock:
                                    new_current_stock = float(
                                        fuel_stock.qty)-saved_qty
                                    FuelStock.objects.filter(Fuel=saved_fuel, branches=manger.branches_id).update(
                                        qty=new_current_stock)
                            except FuelStock.DoesNotExist:
                                print("no matching Fuel found")
                                return Response({'msg': 'Fuel not found'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                            sale_cash_balance = cash_balance+saved_paid_amt
                            balance_amt = Invoice.objects.filter(
                                type=2, payment_type=1, branches=branch_id).aggregate(Sum('balance_amt'))
                            total_cash_debit = balance_amt['balance_amt__sum']
                            print("total cash debit balance=", total_cash_debit)
                            print("current cash debit balance=",
                                  cash_account.debit_balance)
                            print("cash balance amout after sale ",
                                  sale_cash_balance)
                            CashMaster.objects.filter(branches=branch_id).update(
                                balance=sale_cash_balance, debit_balance=total_cash_debit)
                            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                        return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            elif session == None:
                return Response({'msg': 'There is no sesion currently ,Please mak sure there is an open session'}, status.HTTP_403_FORBIDDEN)
            else:
                return Response({'msg': 'There is no sesion currently ,Please mak sure there is an open session'}, status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            manger = BranchManager.objects.get(user=request.user)
            invoices = Invoice.objects.filter(company=Company.objects.get(
                id=manger.company_id), branches=Branches.objects.get(id=manger.branches_id))
            serializer = InvoiceListSerielizer(
                invoices, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)
            invoice = Invoice.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not invoice:
                return Response({'message': "invoice not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = InvoiceListSerielizer(
                invoice[0], context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """used to update the banak balance and cash balance after the amount paid to the corresponding creditor,
        the amount  will be deduced from the account and it will affect the corresponding account balance 
        if paying from a diffrent account the amount will be deduced from that account aslo the remaining credit
        will be added to the corresponding account,the credit will be removed from the corresponding account"""
        try:
            print("Payment Type", request.data['payment_type'])
            if int(request.data['payment_type']) == 2:
                manager = BranchManager.objects.get(user=request.user)
                print(
                    "===========Sale Invoice updating payment type BAnk================")
                bank_id = request.data['bank_ac_id']
                initial_invoice = Invoice.objects.filter(
                    pk=pk, type=2, company=manager.company_id, branches=manager.branches_id)
                print("initial_recipt balance", initial_invoice[0].balance_amt)
                initial_payment_type = initial_invoice[0].payment_type
                print("initial payment type", initial_payment_type)
                if int(initial_payment_type) == 1:
                    print("initial payment in cash condition working")
                    initial_paid_amt = initial_invoice[0].paid_amt
                    branches = manager.branches_id
                    serializer = InvoiceUpdateSerializer(
                        initial_invoice[0], data=request.data, context={"request": request})
                    if serializer.is_valid():
                        serializer.save()
                        initial_invoice = Invoice.objects.filter(
                            pk=pk).update(bank=bank_id)
                        new_paid_amt = serializer.data['paid_amt']
                        diffrence = new_paid_amt-initial_paid_amt
                        print("diffrenece amt after updation", diffrence)
                        new_bank_account = BankAccountMaster.objects.filter(
                            pk=bank_id)
                        new_account_current_balance = new_bank_account[0].balance
                        new_balance = new_account_current_balance+diffrence
                        print("new cash balance after update for bank", new_balance)
                        new_bank_balance_amt = Invoice.objects.filter(
                            type=2, payment_type=2, bank=bank_id).aggregate(Sum('balance_amt'))
                        total_new_bank_debit = new_bank_balance_amt['balance_amt__sum']
                        print("total_new_bank debit", total_new_bank_debit)
                        update = BankAccountMaster.objects.filter(pk=bank_id).update(
                            debit_balance=total_new_bank_debit, balance=new_balance)
                        print("bank account master object after update", update)
                        cash_master = CashMaster.objects.filter(
                            branches=branches)
                        balance_amt = Invoice.objects.filter(
                            type=2, payment_type=1, cash=cash_master[0].id).aggregate(Sum('balance_amt'))
                        total_new_cash_debit = balance_amt['balance_amt__sum']
                        update_cash_master = CashMaster.objects.filter(
                            pk=cash_master[0].id).update(debit_balance=total_new_cash_debit)
                        print("cash master update working", update_cash_master)
                        return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
                # breakpoint()
                elif int(initial_payment_type) == 2:
                    initial_account_id = initial_invoice[0].bank
                    print("initial bank account ================>",
                          initial_account_id.id)
                    initial_paid_amt = initial_invoice[0].paid_amt
                    print("initial paid amount  ================>",
                          initial_paid_amt)
                    account = BankAccountMaster.objects.filter(pk=bank_id)
                    current_balance = account[0].balance
                    print("current bank balance", current_balance)
                    """used to identify the account used for recieving the initial tranaction"""
                    new_bank_account_id = request.data['bank_ac_id']
                    print("New bank account in request  ================>",
                          new_bank_account_id)
                    if not initial_invoice:
                        return Response({'message': "invoice not found"}, status=status.HTTP_404_NOT_FOUND)
                    if int(initial_account_id.id) == int(new_bank_account_id):
                        print(
                            "=================new bank account and initial bank accounts match=============")
                        serializer = InvoiceUpdateSerializer(
                            initial_invoice[0], data=request.data, context={"request": request})
                        if serializer.is_valid():
                            serializer.save()
                            debit_balance_amt = Invoice.objects.filter(
                                type=2, payment_type=2, bank=bank_id).aggregate(Sum('balance_amt'))
                            total_debit_blance = debit_balance_amt['balance_amt__sum']
                            if total_debit_blance is None:
                                print("if condition workig")
                                new_total_debit = 0
                            else:
                                new_total_debit = total_debit_blance
                            print("new paid amt========================>",
                                  serializer.data['paid_amt'])
                            print(
                                "Initial paid amt========================>", initial_paid_amt)
                            current_paid_amt_ac_chnaged = serializer.data['paid_amt']
                            diffrence = current_paid_amt_ac_chnaged-initial_paid_amt
                            print("difference after update", diffrence)
                            """the aount will added to the account balance which is used for initial transaction"""
                            new_balance_after_invoice_update = current_balance+diffrence
                            print("new balance after update",
                                  new_balance_after_invoice_update)
                            print("total bank Debit", new_total_debit)
                            update = BankAccountMaster.objects.filter(pk=bank_id).update(
                                debit_balance=new_total_debit, balance=new_balance_after_invoice_update)
                            print("bank account master object after update", update)
                            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
                        return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                    else:
                        print(
                            "=================Bank accounts does not match=============")
                        print("Invoice before sending serielizer",)
                        initial_invoice[0].bank_id = bank_id
                        serializer = InvoiceUpdateSerializer(
                            initial_invoice[0], data=request.data, context={"request": request})
                        if serializer.is_valid():
                            serializer.save()
                            balance_amt = Invoice.objects.filter(
                                type=2, payment_type=2, bank=new_bank_account_id).aggregate(Sum('balance_amt'))
                            # print(connection.queries)
                            total_debit = balance_amt['balance_amt__sum']
                            if total_debit is None:
                                print("if condition workig")
                                new_total_debit = 0
                            else:
                                new_total_debit = total_debit
                            new_bank_account = BankAccountMaster.objects.filter(
                                pk=bank_id)
                            new_account_current_balance = new_bank_account[0].balance
                            print("new account current balance",
                                  new_account_current_balance)
                            new_account_current_debit_balance = account[0].debit_balance
                            if new_account_current_debit_balance is None:
                                print("if condition workig")
                                new_account_current_debit_balance = 0
                            print("new account current blaance",
                                  new_account_current_balance)
                            print("new account current debit blaance",
                                  new_account_current_debit_balance)
                            print("new account total debit", new_total_debit)
                            print("new paid amt========================>",
                                  serializer.data['paid_amt'])
                            print(
                                "Initial paid amt========================>", initial_paid_amt)
                            current_paid_amt_ac_chnaged = serializer.data['paid_amt']
                            if initial_paid_amt == current_paid_amt_ac_chnaged:
                                print(
                                    "initial paid amt and after update paid amt are equal")
                                update = BankAccountMaster.objects.filter(pk=bank_id).update(
                                    debit_balance=new_total_debit, balance=new_account_current_balance)
                                old_account_debit_new = Invoice.objects.filter(
                                    type=2, payment_type=2, bank=initial_account_id.id).aggregate(Sum('balance_amt'))
                                old_account_new_debit_balance = old_account_debit_new['balance_amt__sum']
                                old_account_update = BankAccountMaster.objects.filter(
                                    pk=initial_account_id.id).update(debit_balance=old_account_new_debit_balance)
                                print(
                                    "new bank account  master object after update", old_account_update)
                            else:
                                diffrence = current_paid_amt_ac_chnaged-initial_paid_amt
                                print("difference after update", diffrence)
                                new_balance_after_invoice_update = new_account_current_balance+diffrence
                                balance_amt = Invoice.objects.filter(
                                    type=2, payment_type=2, bank=new_bank_account_id).aggregate(Sum('balance_amt'))
                                total_debit_balance = balance_amt['balance_amt__sum']
                                if total_debit_balance is None:
                                    print("if condition workig")
                                    new_total_debit = 0
                                else:
                                    new_total_debit = total_debit_balance
                                print("new total debit balance",
                                      new_total_debit)
                                update = BankAccountMaster.objects.filter(pk=bank_id).update(
                                    debit_balance=new_total_debit, balance=new_balance_after_invoice_update)
                                old_account_credit_new_credit = Invoice.objects.filter(
                                    type=2, payment_type=2, bank=initial_account_id.id).aggregate(Sum('balance_amt'))
                                old_account_new_debit_balance = old_account_credit_new_credit[
                                    'balance_amt__sum']
                                old_account_update = BankAccountMaster.objects.filter(
                                    pk=initial_account_id.id).update(debit_balance=old_account_new_debit_balance)
                                print(
                                    "new bank account  master object after update", old_account_update)
                            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
                        return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            elif int(request.data['payment_type']) == 1:
                manager = BranchManager.objects.get(user=request.user)
                print("===========updating payment type cash================")
                branches = manager.branches_id
                initial_invoice = Invoice.objects.filter(
                    pk=pk, type=2, company=manager.company_id, branches=manager.branches_id)
                if not initial_invoice:
                    return Response({'message': "invoice not found"}, status=status.HTTP_404_NOT_FOUND)
                # print("initial_bank account affected",initial_invoice[0].bank.id)
                initial_payment_type = initial_invoice[0].payment_type
                initial_paid_amt = initial_invoice[0].paid_amt
                if int(initial_payment_type) == 2:
                    bank_id = initial_invoice[0].bank.id
                    print("initial payment in cash condition working")
                    initial_paid_amt = initial_invoice[0].paid_amt
                    branches = manager.branches_id
                    serializer = InvoiceUpdateSerializer(
                        initial_invoice[0], data=request.data, context={"request": request})
                    if serializer.is_valid():
                        serializer.save()
                        cash_master = CashMaster.objects.filter(
                            branches=branches)
                        # initial_invoice = Invoice.objects.filter(pk=pk).update(bank=bank_id)
                        new_paid_amt = serializer.data['paid_amt']
                        diffrence = new_paid_amt-initial_paid_amt
                        print("diffrenece amt after updation", diffrence)
                        cash_master_current_balance = cash_master[0].balance
                        new_balance = cash_master_current_balance+diffrence
                        print("new cash balance after update for bank", new_balance)
                        balance_amt = Invoice.objects.filter(
                            type=2, payment_type=1, cash=cash_master[0].id).aggregate(Sum('balance_amt'))
                        total_new_cash_debit = balance_amt['balance_amt__sum']
                        print("total_new_cash debit", total_new_cash_debit)
                        update_cash_master = CashMaster.objects.filter(pk=cash_master[0].id).update(
                            debit_balance=total_new_cash_debit, balance=new_balance)
                        print("bank account master object after update",
                              update_cash_master)
                        new_bank_balance_amt = Invoice.objects.filter(
                            type=2, payment_type=2, bank=bank_id).aggregate(Sum('balance_amt'))
                        total_new_bank_debit = new_bank_balance_amt['balance_amt__sum']
                        update_bank = BankAccountMaster.objects.filter(
                            pk=bank_id).update(debit_balance=total_new_bank_debit)
                        print("bank update working", update_bank)
                        return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
                elif int(initial_payment_type) == 1:
                    initial_paid_amt = initial_invoice[0].paid_amt
                    branches = manager.branches_id
                    serializer = InvoiceUpdateSerializer(
                        initial_invoice[0], data=request.data, context={"request": request})
                    if serializer.is_valid():
                        serializer.save()
                        cash_master = CashMaster.objects.filter(
                            branches=branches)
                        balance_amt = Invoice.objects.filter(
                            type=2, payment_type=1, cash=cash_master[0].id).aggregate(Sum('balance_amt'))
                        total_new_cash_debit = balance_amt['balance_amt__sum']
                        print("total cashmster debit", total_new_cash_debit)
                        print("cash master balance", cash_master[0].balance)
                        cash_master_current_balance = cash_master[0].balance
                        new_paid_amt = serializer.data['paid_amt']
                        diffrence = new_paid_amt-initial_paid_amt
                        print("diffrenece amt after updation", diffrence)
                        new_balance = cash_master_current_balance+diffrence
                        print("new cash balance after update", new_balance)
                        update_cash_master = CashMaster.objects.filter(pk=cash_master[0].id).update(
                            debit_balance=total_new_cash_debit, balance=new_balance)
                        print("cash master update working", update_cash_master)
                        return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
                    # return Response({'errors':serializer.errors,'msg':'Invalid data'},status.HTTP_422_UNPROCESSABLE_ENTITY)
            # return Response({'msg':'invalid data'})
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            invoice = Invoice.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not invoice:
                return Response({'message': "invoice not found"}, status=status.HTTP_404_NOT_FOUND)
            invoice[0].delete()
            return Response({'msg': 'Success'}, status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class VatRegistrationViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def create(self, request):
        try:
            serializer = VatRegistrationSerializer(
                data=request.data, context={"request": request})
            print(type(request.data['vat']))
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': ' Vat inserton Success', 'data': serializer.data}, status.HTTP_201_CREATED)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)

            vat = VatMaster.objects.filter(company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            serializer = VatSerializer(
                vat, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            supplier = VatMaster.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not supplier:
                return Response({'message': "Vat not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = VatSerializer(
                supplier[0], context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            vat = VatMaster.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not vat:
                return Response({'message': "Vat not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = VatSerializer(
                vat[0], data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            vat = VatMaster.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not vat:
                return Response({'message': "Vat not found"}, status=status.HTTP_404_NOT_FOUND)
            vat[0].delete()
            return Response({'msg': 'Success'}, status.HTTP_200_OK)

        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class FuelRegistrationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    # def create(self, request):
    #     try:
    #         serializer = FuelRegistrationSerializer(data=request.data,context={"request": request})
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response({'msg':'Fuel added succesfully', 'data':serializer.data},status.HTTP_201_CREATED)
    #         return Response({'errors':serializer.errors,'msg':'Invalid data'},status.HTTP_422_UNPROCESSABLE_ENTITY)
    #     except Exception as e:
    #         print(e)
    #         return Response({'msg':'Server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)

            fuel = FuelMaster.objects.filter(
                company=Company.objects.get(id=manager.company_id))
            serializer = FuelListSerializer(
                fuel, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            fuel = FuelMaster.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not fuel:
                return Response({'message': "Fuel not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = FuelSerializer(
                fuel[0], data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            fuel = FuelMaster.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not fuel:
                return Response({'message': "Fuel not found"}, status=status.HTTP_404_NOT_FOUND)
            fuel[0].delete()
            return Response({'msg': 'Success'}, status.HTTP_200_OK)

        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            fuel = FuelMaster.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not fuel:
                return Response({'message': "Fuel not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = FuelSerializer(fuel[0], context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class BankViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def create(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)
            is_default = request.data['is_default']
            if is_default:
                print("account")
                if BankAccountMaster.objects.filter(branches=manager.branches_id, is_default=True).exists():
                    return Response({'msg': 'Default account already exist'}, status.HTTP_422_UNPROCESSABLE_ENTITY)

            serializer = BankCreateSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(e)
            return Response({'errors': serializer.errors, 'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)

            bank = BankAccountMaster.objects.filter(company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            serializer = BankSerializer(
                bank, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            bank = BankAccountMaster.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not bank:
                return Response({'message': "Bank not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = BankSerializer(
                bank[0], data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            bank = BankAccountMaster.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not bank:
                return Response({'message': "Bank not found"}, status=status.HTTP_404_NOT_FOUND)
            bank[0].delete()
            return Response({'msg': 'Success'}, status.HTTP_200_OK)

        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            bank = BankAccountMaster.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not bank:
                return Response({'message': "Bank not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = BankSerializer(bank[0], context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepositViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def create(self, request):
        try:
            serializer = DepositCreateSerializer(data=request.data, context={
                                                 "request": request, "data": request.data})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)
            deposit = Deposit.objects.filter(company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            serializer = DepositSerializer(
                deposit, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            deposit = Deposit.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not deposit:
                return Response({'message': "Deposit not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DepositSerializer(
                deposit[0], data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            deposit = Deposit.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not deposit:
                return Response({'message': "Deposit not found"}, status=status.HTTP_404_NOT_FOUND)
            deposit[0].delete()
            return Response({'msg': 'Success'}, status.HTTP_200_OK)

        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            deposit = Deposit.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not deposit:
                return Response({'message': "Deposit not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DepositSerializer(
                deposit[0], context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class DispenceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def create(self, request):
        try:
            serializer = DispenceCreateSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:

            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)

            dispence = Dispence.objects.filter(company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            serializer = DispenceSerializer(
                dispence, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            dispence = Dispence.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not dispence:
                return Response({'message': "Dispence not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DispenceSerializer(
                dispence[0], data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            dispence = Dispence.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not dispence:
                return Response({'message': "Dispence not found"}, status=status.HTTP_404_NOT_FOUND)
            dispence[0].delete()
            return Response({'msg': 'Success'}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            dispence = Dispence.objects.filter(pk=pk, company=Company.objects.get(
                id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
            if not dispence:
                return Response({'message': "Dispence not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DispenceSerializer(
                dispence[0], context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class DailySessionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def create(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)
            print("checking for session")
            print("Request Data", request.data)
            try:
                date_today = datetime.datetime.today()
                today_min = datetime.datetime.combine(
                    datetime.date.today(), datetime.time.min)
                today_max = datetime.datetime.combine(
                    datetime.date.today(), datetime.time.max)
                branch = Branches.objects.get(id=manager.branches_id),
                print("responsible branch", branch[0].id)
                print("todays date", date_today)
                # Sale.objects.all().order_by('id').last()
                # session=DailySession.objects.filter(branches_id=request.data['branches'],date__range=(today_min, today_max),status=False)

                session = DailySession.objects.filter(
                    branches=manager.branches_id).last()
                print("last session command woeking", session)
                if session:
                    print("matching session found")
                    try:
                        print("inner condition working")
                        today_session = DailySession.objects.get(
                            branches=branch[0].id, date__range=(today_min, today_max), status=False)
                        print(connection.queries)
                        if today_session:
                            return Response({'msg': 'Already created a session today'}, status.HTTP_405_METHOD_NOT_ALLOWED)
                    except Exception as e:
                        print(e)
                        serializer = SessionCreateSerializer(data=request.data, context={
                                                             "request": request, "data": session})
                        if serializer.is_valid():
                            serializer.save()
                            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                        return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                elif session == None:
                    print("no matching session found for this branch")
                    branch_details = CashMaster.objects.get(
                        Q(branches=manager.branches_id))
                    print(connection.queries)
                    if branch_details:
                        print("have branch detail entered")
                        serializer = FirstSessionCreateSerializer(
                            data=request.data, context={"request": request, "data": branch_details})
                        if serializer.is_valid():
                            serializer.save()
                            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                        return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            except DailySession.DoesNotExist:
                print("no matching session found")
                branch_details = CashMaster.objects.get(
                    branches=manager.branches_id)
                if branch_details:
                    print("have branch detail entered")
                    serializer = FirstSessionCreateSerializer(
                        data=request.data, context={"request": request, "data": branch_details})
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                    return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)
            session = DailySession.objects.filter(
                pk=pk, branches=manager.branches_id)
            serializer = SessionCloseSerielizer(session, data=request.data, context={
                                                "request": request, "data": session})
            if serializer.is_valid():
                serializer.save()
                session = DailySession.objects.filter(
                    pk=pk, branches=manager.branches_id)
                serializer = SessionCloseResultSerielizer(
                    session[0], context={"request": request})
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            sessions = DailySession.objects.filter(
                date__range=(today_min, today_max))
            serializer = SessionListViewSerielizer(
                sessions, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            session = DailySession.objects.filter(pk=pk)
            if not session:
                return Response({'message': "session not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = SessionListViewSerielizer(
                session[0], context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class CashMasterViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def create(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)
            if CashMaster.objects.filter(branches=manager.branches_id).exists():
                return Response({'msg': 'Opening blance already added for this branch'}, status.HTTP_422_UNPROCESSABLE_ENTITY)

            serializer = CashMasterCreateSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:

            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReciptViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReciptCreateSerializer


""""
calculations will be done in front end
   Purchase and invoice management with invoice table,Purchase amount will be deducted from coreesponding accounts
   cash balance or bank balance,if it's a credit purchase the credit cash balance and bank balance will be shown in he
   bank account master,if a invoice is made the amount will be added to cash balnce or bank balnce,if it's debit sale,
   the amount will be shown in cash  debit blance/bank debit balance,before transaction to be done the creation of a session must necessary
   if two account used for transaction the amount should be diplayed in the total,
   a session foreign key table is created to store each accounts and its values,
   -need of company info
   -branch wise accounts
   -opening balance management
"""


class ReciptViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReciptCreateSerializer

    def create(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)
            print("Payment Type", request.data['payment_type'])
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            session = DailySession.objects.filter(
                branches_id=manager.branches_id, date__range=(today_min, today_max), status=False)
            print("session", session.query)
            # session=DailySession.objects.filter(branches_id=request.data['branches'])
            print("last session command woeking", session)
            if session:
                request.data['session_id'] = session[0].id
                print("matching session found")
                if int(request.data['payment_type']) == 2:
                    print("request", request)
                    print("request data", request.data)
                    print("Paid Amount", request.data['paid_amt'])
                    bank_id = request.data['bank_ac_id']
                    if bank_id:
                        account_balance = BankAccountMaster.objects.get(
                            pk=bank_id)
                        print("Rbank account", account_balance)
                        print("Rbank account", account_balance.balance)
                        bank_balance = float(account_balance.balance)
                        print("is default bank account",
                              account_balance.is_default)
                        if account_balance.is_default:
                            if float(request.data['paid_amt']) > bank_balance:
                                print("float condition working")
                                return Response({'msg': 'Do not have enough balance to make payment,'+'available balance='+str(account_balance.balance) + ' pleasemake a deposit to  continue transaction'}, status.HTTP_400_BAD_REQUEST)
                            elif float(request.data['paid_amt']) == bank_balance:
                                print(
                                    "===============paid amount and bank balance amount are equal======")
                                serializer = ReciptCreateSerializer(data=request.data, context={
                                                                    "request": request, "data": request.data})
                                if serializer.is_valid():
                                    serializer.save()
                                    saved_paid_amt = float(
                                        serializer.data['paid_amt'])
                                    saved_qty = float(serializer.data['qty'])
                                    print("saved purchase quantity", saved_qty)
                                    saved_fuel = float(serializer.data['fuel'])
                                    try:
                                        print("fuel stock updation")
                                        fuel_stock = FuelStock.objects.get(
                                            Fuel=saved_fuel, branches=manager.branches_id)
                                        if fuel_stock:
                                            new_current_stock = float(
                                                fuel_stock.qty)+saved_qty
                                            FuelStock.objects.filter(Fuel=saved_fuel, branches=manager.branches_id).update(
                                                qty=new_current_stock)
                                    except FuelStock.DoesNotExist:
                                        print("no matching Fuel found")
                                        return Response({'msg': 'Fuel not found'}, status.HTTP_422_UNPROCESSABLE_ENTITY)

                                    invoice_balance = Invoice.objects.filter(
                                        type=1, payment_type=2, bank=bank_id).aggregate(Sum('balance_amt'))
                                    total_credit = invoice_balance['balance_amt__sum']
                                    purchase_balance = bank_balance-saved_paid_amt
                                    print("current credit balance=",
                                          account_balance.credit_balance)
                                    print(
                                        "bank balance amout after purchase ", purchase_balance,)
                                    BankAccountMaster.objects.filter(pk=bank_id).update(
                                        balance=purchase_balance, credit_balance=total_credit)
                                    return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                                return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                            else:
                                serializer = ReciptCreateSerializer(data=request.data, context={
                                                                    "request": request, "data": request.data})
                                if serializer.is_valid():
                                    serializer.save()
                                    saved_paid_amt = float(
                                        serializer.data['paid_amt'])
                                    saved_qty = float(serializer.data['qty'])
                                    print("saved purchase quantity", saved_qty)
                                    saved_fuel = float(serializer.data['fuel'])
                                    # branches=int(serializer.data['branches'])
                                    try:
                                        print("fuel stock updation")
                                        fuel_stock = FuelStock.objects.get(
                                            Fuel=saved_fuel, branches=manager.branches_id)
                                        if fuel_stock:
                                            new_current_stock = float(
                                                fuel_stock.qty)+saved_qty
                                            FuelStock.objects.filter(Fuel=saved_fuel, branches=manager.branches_id).update(
                                                qty=new_current_stock)
                                    except FuelStock.DoesNotExist:
                                        print("no matching Fuel found")
                                        return Response({'msg': 'Fuel not found'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                                    invoice_balance = Invoice.objects.filter(
                                        type=1, payment_type=2, bank=bank_id).aggregate(Sum('balance_amt'))
                                    total_credit = invoice_balance['balance_amt__sum']
                                    purchase_balance = bank_balance-saved_paid_amt
                                    print(
                                        "bank balance amout after purchase ", purchase_balance)
                                    print("Data after purachase ",
                                          serializer.data)
                                    print("current credit balance=",
                                          account_balance.credit_balance)
                                    BankAccountMaster.objects.filter(pk=bank_id).update(
                                        balance=purchase_balance, credit_balance=total_credit)
                                    return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                                return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                        else:
                            if float(request.data['paid_amt']) > bank_balance:
                                print("float condition working")
                                return Response({'msg': 'Do not have enough balance to make payment,'+'available balance='+str(account_balance.balance) + ' pleasemake a deposit to  continue transaction'}, status.HTTP_400_BAD_REQUEST)
                            elif float(request.data['paid_amt']) == bank_balance:
                                print(
                                    "===============paid amount and bank balance amount are equal")
                                serializer = ReciptCreateSerializer(data=request.data, context={
                                                                    "request": request, "data": request.data})
                                if serializer.is_valid():
                                    serializer.save()
                                    saved_paid_amt = float(
                                        serializer.data['paid_amt'])
                                    saved_qty = float(serializer.data['qty'])
                                    print("saved purchase quantity", saved_qty)
                                    saved_fuel = float(serializer.data['fuel'])
                                    try:
                                        print("fuel stock updation")
                                        fuel_stock = FuelStock.objects.get(
                                            Fuel=saved_fuel, branches=manager.branches_id)
                                        if fuel_stock:
                                            new_current_stock = float(
                                                fuel_stock.qty)+saved_qty
                                            FuelStock.objects.filter(Fuel=saved_fuel, branches=manager.branches_id).update(
                                                qty=new_current_stock)
                                    except FuelStock.DoesNotExist:
                                        print("no matching Fuel found")
                                        return Response({'msg': 'Fuel not found'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                                    invoice_balance = Invoice.objects.filter(
                                        type=1, payment_type=2, bank=bank_id).aggregate(Sum('balance_amt'))
                                    total_credit = invoice_balance['balance_amt__sum']
                                    purchase_balance = bank_balance-saved_paid_amt
                                    print("current credit balance=",
                                          account_balance.credit_balance)
                                    print(
                                        "bank balance amout after purchase ", purchase_balance,)
                                    BankAccountMaster.objects.filter(pk=bank_id).update(
                                        balance=purchase_balance, credit_balance=total_credit)
                                    return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                                return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                            else:
                                serializer = ReciptCreateSerializer(data=request.data, context={
                                                                    "request": request, "data": request.data})
                                if serializer.is_valid():
                                    serializer.save()
                                    saved_paid_amt = float(
                                        serializer.data['paid_amt'])
                                    saved_qty = float(serializer.data['qty'])
                                    print("saved purchase quantity", saved_qty)
                                    saved_fuel = float(serializer.data['fuel'])
                                    branches = int(serializer.data['branches'])
                                    try:
                                        print("fuel stock updation")
                                        fuel_stock = FuelStock.objects.get(
                                            Fuel=saved_fuel, branches=manager.branches_id)
                                        if fuel_stock:
                                            new_current_stock = float(
                                                fuel_stock.qty)+saved_qty
                                            FuelStock.objects.filter(Fuel=saved_fuel, branches=manager.branches_id).update(
                                                qty=new_current_stock)
                                    except FuelStock.DoesNotExist:
                                        print("no matching Fuel found")
                                        return Response({'msg': 'Fuel not found'}, status.HTTP_422_UNPROCESSABLE_ENTITY)

                                    invoice_balance = Invoice.objects.filter(
                                        type=1, payment_type=2, bank=bank_id).aggregate(Sum('balance_amt'))
                                    total_credit = invoice_balance['balance_amt__sum']
                                    purchase_balance = bank_balance-saved_paid_amt
                                    print(
                                        "bank balance amout after purchase ", purchase_balance)
                                    print("Data after purachase ",
                                          serializer.data)
                                    print("current credit balance=",
                                          account_balance.credit_balance)
                                    BankAccountMaster.objects.filter(pk=bank_id).update(
                                        balance=purchase_balance, credit_balance=total_credit)
                                    return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                                return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)

                elif int(request.data['payment_type']) == 1:
                    print("payment type is cash")
                    print("request data", request.data)
                    print("Paid Amount", request.data['paid_amt'])
                    branch_id = manager.branches_id
                    if branch_id:
                        cash_ac_balance = CashMaster.objects.get(
                            branches=branch_id)
                        print("cash account balance", cash_ac_balance)
                        print("Balance", cash_ac_balance.balance)
                        cash_balance = float(cash_ac_balance.balance)
                        # if account_balance.is_default:
                        if float(request.data['paid_amt']) > cash_balance:
                            print("float condition working")
                            return Response({'msg': 'Do not have enough balance to make payment,'+'available cash balance='+str(cash_ac_balance.balance) + ' pleasemake a deposit to company continue transaction'}, status.HTTP_400_BAD_REQUEST)
                        elif float(request.data['paid_amt']) == cash_balance:
                            print(
                                "===============paid amount and bank balance amount are equal")
                            serializer = ReciptCreateSerializer(data=request.data, context={
                                                                "request": request, "data": request.data})
                            if serializer.is_valid():
                                serializer.save()
                                saved_paid_amt = float(
                                    serializer.data['paid_amt'])
                                cash_balance_purchase = cash_balance-saved_paid_amt
                                balance_amt = Invoice.objects.filter(
                                    type=1, payment_type=1, branch=branch_id).aggregate(Sum('balance_amt'))
                                total_cash_credit = balance_amt['balance_amt__sum']
                                saved_qty = float(serializer.data['qty'])
                                print("saved purchase quantity", saved_qty)
                                saved_fuel = float(serializer.data['fuel'])
                                try:
                                    print("fuel stock updation")
                                    fuel_stock = FuelStock.objects.get(
                                        Fuel=saved_fuel, branches=manager.branches_id)
                                    if fuel_stock:
                                        new_current_stock = float(
                                            fuel_stock.qty)+saved_qty
                                        FuelStock.objects.filter(Fuel=saved_fuel, branches=manager.branches_id).update(
                                            qty=new_current_stock)
                                except FuelStock.DoesNotExist:
                                    print("no matching Fuel found")
                                    return Response({'msg': 'Fuel not found'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                                print("current credit balance=",
                                      cash_ac_balance.credit_balance)
                                print("cash balance amout after purchase ",
                                      cash_balance_purchase,)
                                CashMaster.objects.filter(branches=branch_id).update(
                                    balance=cash_balance_purchase, credit_balance=total_cash_credit)
                                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                        else:
                            serializer = ReciptCreateSerializer(data=request.data, context={
                                                                "request": request, "data": request.data})
                            if serializer.is_valid():
                                serializer.save()
                                saved_paid_amt = float(
                                    serializer.data['paid_amt'])
                                cash_balance_purchase = cash_balance-saved_paid_amt
                                saved_qty = float(serializer.data['qty'])
                                print("saved purchase quantity", saved_qty)
                                saved_fuel = float(serializer.data['fuel'])
                                try:
                                    print("fuel stock updation")
                                    fuel_stock = FuelStock.objects.get(
                                        Fuel=saved_fuel, branches=manager.branches_id)
                                    if fuel_stock:
                                        new_current_stock = float(
                                            fuel_stock.qty)+saved_qty
                                        FuelStock.objects.filter(Fuel=saved_fuel, branches=manager.branches_id).update(
                                            qty=new_current_stock)
                                except FuelStock.DoesNotExist:
                                    print("no matching Fuel found")
                                    return Response({'msg': 'Fuel not found'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                                balance_amt = Invoice.objects.filter(
                                    type=1, payment_type=1, branches=branch_id).aggregate(Sum('balance_amt'))
                                total_cash_credit = balance_amt['balance_amt__sum']
                                print("cash balance amout after purchase ",
                                      cash_balance_purchase)
                                print("Data after purachase ", serializer.data)
                                print("current credit balance=",
                                      cash_ac_balance.credit_balance)
                                CashMaster.objects.filter(branches=branch_id).update(
                                    balance=cash_balance_purchase, credit_balance=total_cash_credit)
                                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response({'msg': 'There is no sesion currently ,Please mak sure there is an open session'}, status.HTTP_403_FORBIDDEN)

        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            recipts = Invoice.objects.filter(
                type=1, company=Company.objects.get(user=request.user))
            serializer = ReciptSerializer(
                recipts, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            recipt = Invoice.objects.filter(
                pk=pk, type=1, company=Company.objects.get(user=request.user))
            if not recipt:
                return Response({'message': "invoice not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ReciptSerializer(
                recipt[0], context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """used to update the bank balance and cash balance after the amount paid to the corresponding creditor,
        the amount  will be deduced from the account and it will affect the corresponding account balance 
        if paying from a diffrent account the amount will be deduced from that account aslo the remaining credit
        will be added to the corresponding account,the credit will be removed from the corresponding account"""
        try:
            print("Payment Type", request.data['payment_type'])
            if int(request.data['payment_type']) == 2:
                manager = BranchManager.objects.get(user=request.user)
                print("===========updating payment type BAnk================")
                print("========================Recipt Update====================")
                bank_id = request.data['bank_ac_id']
                initial_recipt = Invoice.objects.filter(
                    pk=pk, type=1, company=manager.company_id, branches=manager.branches_id)
                print("initial_recipt balance", initial_recipt[0].balance_amt)
                initial_payment_type = initial_recipt[0].payment_type
                print("initial payment type", initial_payment_type)
                if int(initial_payment_type) == 1:
                    print("initial payment in cash condition working")
                    initial_paid_amt = initial_recipt[0].paid_amt
                    branches = manager.branches_id
                    serializer = ReciptUpdateSerializer(
                        initial_recipt[0], data=request.data, context={"request": request})
                    if serializer.is_valid():
                        serializer.save()
                        initial_recipt = Invoice.objects.filter(
                            pk=pk).update(bank=bank_id)
                        new_paid_amt = serializer.data['paid_amt']
                        diffrence = new_paid_amt-initial_paid_amt
                        print("diffrenece amt after updation", diffrence)
                        new_bank_account = BankAccountMaster.objects.filter(
                            pk=bank_id)
                        new_account_current_balance = new_bank_account[0].balance
                        new_balance = new_account_current_balance-diffrence
                        print("new cash balance after update for bank", new_balance)
                        new_bank_balance_amt = Invoice.objects.filter(
                            type=1, payment_type=2, bank=bank_id).aggregate(Sum('balance_amt'))
                        total_new_bank_credit = new_bank_balance_amt['balance_amt__sum']
                        print("total_new_bank debit", total_new_bank_credit)
                        update = BankAccountMaster.objects.filter(pk=bank_id).update(
                            credit_balance=total_new_bank_credit, balance=new_balance)
                        print("bank account master object after update", update)
                        cash_master = CashMaster.objects.filter(
                            branches=branches)
                        balance_amt = Invoice.objects.filter(
                            type=1, payment_type=1, cash=cash_master[0].id).aggregate(Sum('balance_amt'))
                        total_new_cash_credit = balance_amt['balance_amt__sum']
                        update_cash_master = CashMaster.objects.filter(
                            pk=cash_master[0].id).update(credit_balance=total_new_cash_credit)
                        print("cash master update working", update_cash_master)
                        return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
                elif int(initial_payment_type) == 2:
                    initial_account_id = initial_recipt[0].bank
                    print("initial bank account ================>",
                          initial_account_id.id)
                    initial_paid_amt = initial_recipt[0].paid_amt
                    print("initial paid amount  ================>",
                          initial_paid_amt)
                    recipt = Invoice.objects.filter(
                        pk=pk, type=1, company=manager.company_id, branches=manager.branches_id)
                    account = BankAccountMaster.objects.filter(pk=bank_id)
                    print("currnt credit balance", account[0].credit_balance)
                    current_credit_balance = account[0].credit_balance
                    print("current bank credit", current_credit_balance)
                    current_balance = account[0].balance
                    print("current bank balance", current_balance)
                    new_bank_account_id = request.data['bank_ac_id']
                    print("New bank account in request  ================>",
                          new_bank_account_id)
                    if not recipt:
                        return Response({'message': "invoice not found"}, status=status.HTTP_404_NOT_FOUND)
                    if int(initial_account_id.id) == int(new_bank_account_id):
                        print(
                            "=================new bank account and initial bank accounts match=============")
                        serializer = ReciptUpdateSerializer(
                            recipt[0], data=request.data, context={"request": request})
                        if serializer.is_valid():
                            serializer.save()
                            balance_amt = Invoice.objects.filter(
                                type=1, payment_type=2, bank=bank_id).aggregate(Sum('balance_amt'))
                            total_credit = balance_amt['balance_amt__sum']
                            if total_credit is None:
                                print("if condition workig")
                                new_total_credit = 0
                            else:
                                new_total_credit = total_credit
                            print("new paid amt========================>",
                                  serializer.data['paid_amt'])
                            print(
                                "Initial paid amt========================>", initial_paid_amt)
                            current_paid_amt_ac_chnaged = serializer.data['paid_amt']
                            diffrence = current_paid_amt_ac_chnaged-initial_paid_amt
                            print("difference after update", diffrence)
                            new_balance_after_invoice_update = current_balance-diffrence
                            print("new balance after update",
                                  new_balance_after_invoice_update)
                            print("total bank credit", new_total_credit)
                            update = BankAccountMaster.objects.filter(pk=bank_id).update(
                                credit_balance=new_total_credit, balance=new_balance_after_invoice_update)
                            print("bank account master object after update", update)
                            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
                        return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                    else:
                        print(
                            "=================Bank accounts does not match=============")
                        print("recipt before sending serielizer",)
                        recipt[0].bank_id = bank_id
                        serializer = ReciptUpdateSerializer(
                            recipt[0], data=request.data, context={"request": request})
                        if serializer.is_valid():
                            serializer.save()
                            balance_amt = Invoice.objects.filter(
                                type=1, payment_type=2, bank=new_bank_account_id).aggregate(Sum('balance_amt'))
                            # print(connection.queries)
                            total_credit = balance_amt['balance_amt__sum']
                            if total_credit is None:
                                print("if condition workig")
                                new_total_credit = 0
                            else:
                                new_total_credit = total_credit
                            new_bank_account = BankAccountMaster.objects.filter(
                                pk=bank_id)
                            new_account_current_balance = new_bank_account[0].balance
                            print("new account current balance",
                                  new_account_current_balance)
                            new_account_current_credit_balance = account[0].credit_balance
                            if new_account_current_credit_balance is None:
                                print("if condition workig")
                                new_account_current_credit_balance = 0
                            print("new account credit blaance",
                                  new_account_current_balance)
                            print("new account current credit blaance",
                                  new_account_current_credit_balance)
                            print("new account tottal_credit", new_total_credit)
                            print("new paid amt========================>",
                                  serializer.data['paid_amt'])
                            print(
                                "Initial paid amt========================>", initial_paid_amt)
                            current_paid_amt_ac_chnaged = serializer.data['paid_amt']
                            if initial_paid_amt == current_paid_amt_ac_chnaged:
                                print(
                                    "initial paid amt and cafter update paid amt are equal")
                                update = BankAccountMaster.objects.filter(pk=bank_id).update(
                                    credit_balance=new_total_credit, balance=new_account_current_balance)
                                old_account_credit_new_credit = Invoice.objects.filter(
                                    type=1, payment_type=2, bank=initial_account_id.id).aggregate(Sum('balance_amt'))
                                old_account_new_credit_balance = old_account_credit_new_credit[
                                    'balance_amt__sum']
                                old_account_update = BankAccountMaster.objects.filter(
                                    pk=initial_account_id.id).update(credit_balance=old_account_new_credit_balance)
                                print(
                                    "new bank account  master object after update", old_account_update)
                            else:
                                diffrence = current_paid_amt_ac_chnaged-initial_paid_amt
                                print("difference after update", diffrence)
                                new_balance_after_invoice_update = new_account_current_balance-diffrence
                                balance_amt = Invoice.objects.filter(
                                    type=1, payment_type=2, bank=new_bank_account_id).aggregate(Sum('balance_amt'))
                                new_total_credit = balance_amt['balance_amt__sum']
                                if total_credit is None:
                                    print("if condition workig")
                                    new_total_credit = 0
                                else:
                                    new_total_credit = total_credit
                                update = BankAccountMaster.objects.filter(pk=bank_id).update(
                                    credit_balance=new_total_credit, balance=new_balance_after_invoice_update)
                                old_account_credit_new_credit = Invoice.objects.filter(
                                    type=1, payment_type=2, bank=initial_account_id.id).aggregate(Sum('balance_amt'))
                                old_account_new_credit_balance = old_account_credit_new_credit[
                                    'balance_amt__sum']
                                old_account_update = BankAccountMaster.objects.filter(
                                    pk=initial_account_id.id).update(credit_balance=old_account_new_credit_balance)
                                print(
                                    "new bank account  master object after update", old_account_update)
                            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
                        return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)

            elif int(request.data['payment_type']) == 1:
                print("===========updating payment type cash================")
                manager = BranchManager.objects.get(user=request.user)
                branches = manager.branches_id
                initial_recipt = Invoice.objects.filter(
                    pk=pk, type=1, company=manager.company_id, branches=manager.branches_id)
                # print("initial_bank account affected",initial_recipt[0].bank.id)
                initial_payment_type = initial_recipt[0].payment_type
                initial_paid_amt = initial_recipt[0].paid_amt
                print("initial paid amt", initial_paid_amt)
                print("branch responsible", branches)
                if not initial_recipt:
                    return Response({'message': "invoice not found"}, status=status.HTTP_404_NOT_FOUND)
                if int(initial_payment_type) == 2:
                    bank_id = initial_recipt[0].bank.id
                    print("initial payment in cash condition working")
                    initial_paid_amt = initial_recipt[0].paid_amt
                    branches = manager.branches_id
                    serializer = ReciptUpdateSerializer(
                        initial_recipt[0], data=request.data, context={"request": request})
                    if serializer.is_valid():
                        serializer.save()
                        cash_master = CashMaster.objects.filter(
                            branches=branches)
                        # initial_recipt = Invoice.objects.filter(pk=pk).update(bank=bank_id)
                        new_paid_amt = serializer.data['paid_amt']
                        diffrence = new_paid_amt-initial_paid_amt
                        print("diffrenece amt after updation", diffrence)
                        cash_master_current_balance = cash_master[0].balance
                        new_balance = cash_master_current_balance-diffrence
                        print("new cash balance after update for bank", new_balance)
                        balance_amt = Invoice.objects.filter(
                            type=1, payment_type=1, cash=cash_master[0].id).aggregate(Sum('balance_amt'))
                        total_new_cash_credit = balance_amt['balance_amt__sum']
                        print("total_new_cash debit", total_new_cash_credit)
                        update_cash_master = CashMaster.objects.filter(pk=cash_master[0].id).update(
                            credit_balance=total_new_cash_credit, balance=new_balance)
                        print("bank account master object after update",
                              update_cash_master)
                        new_bank_balance_amt = Invoice.objects.filter(
                            type=1, payment_type=2, bank=bank_id).aggregate(Sum('balance_amt'))
                        total_new_bank_credit = new_bank_balance_amt['balance_amt__sum']
                        update_bank = BankAccountMaster.objects.filter(
                            pk=bank_id).update(credit_balance=total_new_bank_credit)
                        print("bank update working", update_bank)
                        return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
                elif int(initial_payment_type) == 1:
                    manager = BranchManager.objects.get(user=request.user)
                    initial_paid_amt = initial_recipt[0].paid_amt
                    branches = manager.branches_id
                    serializer = ReciptUpdateSerializer(
                        initial_recipt[0], data=request.data, context={"request": request})
                    if serializer.is_valid():
                        serializer.save()
                        cash_master = CashMaster.objects.filter(
                            branches=branches)
                        balance_amt = Invoice.objects.filter(
                            type=1, payment_type=1, cash=cash_master[0].id).aggregate(Sum('balance_amt'))
                        total_new_cash_credit = balance_amt['balance_amt__sum']
                        print("total cashmster credit", total_new_cash_credit)
                        print("cash master balance", cash_master[0].balance)
                        cash_master_current_balance = cash_master[0].balance
                        new_paid_amt = serializer.data['paid_amt']
                        diffrence = new_paid_amt-initial_paid_amt
                        print("diffrenece amt after updation", diffrence)
                        new_balance = cash_master_current_balance-diffrence
                        print("new cash balance after update", new_balance)
                        update_cash_master = CashMaster.objects.filter(pk=cash_master[0].id).update(
                            credit_balance=total_new_cash_credit, balance=new_balance)
                        print("cash master update working", update_cash_master)
                        return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            recipt = Invoice.objects.filter(
                pk=pk, type=1, company=Company.objects.get(user=request.user))
            if not recipt:
                return Response({'message': "invoice not found"}, status=status.HTTP_404_NOT_FOUND)
            recipt[0].delete()
            return Response({'msg': 'Success'}, status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)
            branches = Branches.objects.get(id=manager.branches_id)
            serializer = DashboardSerielzer(
                branches, many=False, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExpenseViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReciptCreateSerializer

    def create(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            session = DailySession.objects.filter(
                branches_id=manager.branches_id, date__range=(today_min, today_max), status=False)
            print("last session command woeking", session)
            if session:
                request.data['session_id'] = session[0].id
                print("matching session found")
                if int(request.data['payment_type']) == 2:
                    print("request", request)
                    print("request data", request.data)
                    print("Paid Amount", request.data['paid_amt'])
                    bank_id = BankAccountMaster.objects.get(
                        branches_id=manager.branches_id)
                    if bank_id:
                        account_balance = BankAccountMaster.objects.get(
                            pk=bank_id.id)
                        print("Rbank account", account_balance)
                        print("Rbank account", account_balance.balance)
                        bank_balance = float(account_balance.balance)
                        print("is default bank account",
                              account_balance.is_default)
                        if float(request.data['paid_amt']) > bank_balance:
                            print("float condition working")
                            return Response({'msg': 'Do not have enough balance to make payment,'+'available balance='+str(account_balance.balance) + ' pleasemake a deposit to  continue transaction'}, status.HTTP_400_BAD_REQUEST)
                        elif float(request.data['paid_amt']) == bank_balance:
                            print(
                                "===============paid amount and bank balance amount are equal")
                            serializer = ExpenseCreateSerializer(data=request.data, context={
                                                                 "request": request, "data": request.data})
                            if serializer.is_valid():
                                serializer.save()
                                saved_paid_amt = float(
                                    serializer.data['paid_amt'])
                                saved_qty = float(serializer.data['qty'])
                                print("saved purchase quantity", saved_qty)
                                invoice_balance = Invoice.objects.filter(
                                    type=1, payment_type=2, bank=bank_id.id, branches=manager.branches_id).aggregate(Sum('balance_amt'))
                                total_credit = invoice_balance['balance_amt__sum']
                                purchase_balance = bank_balance-saved_paid_amt
                                print("current credit balance=",
                                      account_balance.credit_balance)
                                print("bank balance amout after purchase ",
                                      purchase_balance,)
                                BankAccountMaster.objects.filter(pk=bank_id.id).update(
                                    balance=purchase_balance, credit_balance=total_credit)
                                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                        else:
                            serializer = ExpenseCreateSerializer(data=request.data, context={
                                                                 "request": request, "data": request.data})
                            if serializer.is_valid():
                                serializer.save()
                                saved_paid_amt = float(
                                    serializer.data['paid_amt'])
                                saved_qty = float(serializer.data['qty'])
                                print("saved purchase quantity", saved_qty)
                                invoice_balance = Invoice.objects.filter(
                                    type=1, payment_type=2, bank=bank_id.id, branches=manager.branches_id).aggregate(Sum('balance_amt'))
                                total_credit = invoice_balance['balance_amt__sum']
                                purchase_balance = bank_balance-saved_paid_amt
                                print("bank balance amout after purchase ",
                                      purchase_balance)
                                print("Data after purachase ", serializer.data)
                                print("current credit balance=",
                                      account_balance.credit_balance)
                                BankAccountMaster.objects.filter(pk=bank_id.id).update(
                                    balance=purchase_balance, credit_balance=total_credit)
                                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                elif int(request.data['payment_type']) == 1:
                    print("payment type is cash")
                    print("request data", request.data)
                    print("Paid Amount", request.data['paid_amt'])
                    branch_id = manager.branches_id
                    if branch_id:
                        cash_ac_balance = CashMaster.objects.get(
                            branches_id=manager.branches_id)
                        print("cash account balance", cash_ac_balance)
                        print("Balance", cash_ac_balance.balance)
                        cash_balance = float(cash_ac_balance.balance)
                        # if account_balance.is_default:
                        if float(request.data['paid_amt']) > cash_balance:
                            print("float condition working")
                            return Response({'msg': 'Do not have enough balance to make payment,'+'available cash balance='+str(cash_ac_balance.balance) + ' pleasemake a deposit to company continue transaction'}, status.HTTP_400_BAD_REQUEST)
                        elif float(request.data['paid_amt']) == cash_balance:
                            print(
                                "===============paid amount and bank balance amount are equal")
                            serializer = ExpenseCreateSerializer(data=request.data, context={
                                                                 "request": request, "data": request.data})
                            if serializer.is_valid():
                                serializer.save()
                                saved_paid_amt = float(
                                    serializer.data['paid_amt'])
                                cash_balance_purchase = cash_balance-saved_paid_amt
                                balance_amt = Invoice.objects.filter(
                                    type=1, payment_type=1, branches=manager.branches_id).aggregate(Sum('balance_amt'))
                                total_cash_credit = balance_amt['balance_amt__sum']
                                print("current credit balance=",
                                      cash_ac_balance.credit_balance)
                                print("cash balance amout after purchase ",
                                      cash_balance_purchase,)
                                CashMaster.objects.filter(branches=branch_id).update(
                                    balance=cash_balance_purchase, credit_balance=total_cash_credit)
                                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                        else:
                            serializer = ExpenseCreateSerializer(data=request.data, context={
                                                                 "request": request, "data": request.data})
                            if serializer.is_valid():
                                serializer.save()
                                saved_paid_amt = float(
                                    serializer.data['paid_amt'])
                                cash_balance_purchase = cash_balance-saved_paid_amt
                                saved_qty = float(serializer.data['qty'])
                                print("saved purchase quantity", saved_qty)
                                balance_amt = Invoice.objects.filter(
                                    type=1, payment_type=1, branches=manager.branches_id).aggregate(Sum('balance_amt'))
                                total_cash_credit = balance_amt['balance_amt__sum']
                                print("cash balance amout after purchase ",
                                      cash_balance_purchase)
                                print("Data after purachase ", serializer.data)
                                print("current credit balance=",
                                      cash_ac_balance.credit_balance)
                                CashMaster.objects.filter(branches=branch_id).update(
                                    balance=cash_balance_purchase, credit_balance=total_cash_credit)
                                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
                            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
                        # else:
                        #     if float(request.data['paid_amt'])>cash_balance:
                        #         print("float condition working")
                        #         return Response({'msg':'Do not have enough balance to make payment,'+'available cash balance='+str(account_balance.balance) +' pleasemake a deposit to company continue transaction'},status.HTTP_400_BAD_REQUEST)
                        #     elif float(request.data['paid_amt'])==cash_balance:
                        #         print("===============paid amount and bank balance amount are equal")
                        #         serializer = ReciptCreateSerializer(data=request.data, context={"request": request,"data":request.data})
                        #         if serializer.is_valid():
                        #             serializer.save()
                        #             saved_paid_amt=float(serializer.data['paid_amt'])
                        #             cash_balance_purchase=cash_balance-saved_paid_amt
                        #             balance_amt = Invoice.objects.filter(type=1,payment_type=1).aggregate(Sum('balance_amt'))
                        #             total_cash_credit=balance_amt['balance_amt__sum']
                        #             saved_qty=float(serializer.data['qty'])
                        #             print("saved purchase quantity",saved_qty)
                        #             saved_fuel=float(serializer.data['fuel'])
                        #             branches=int(serializer.data['branches'])
                        #             try:
                        #                 fuel_stock=FuelStock.objects.get(Fuel=saved_fuel)

                        #                 if fuel_stock:
                        #                     print("fuel stock quantity",fuel_stock.qty)
                        #                     qty=float(fuel_stock.qty)+saved_qty
                        #                     FuelStock.objects.filter(pk=fuel_stock.id).update(qty=qty)
                        #                 elif fuel_stock==None:
                        #                     stock=FuelStock(Fuel=FuelMaster.objects.get(id=saved_fuel), qty=saved_qty,
                        #                                     branches=Branches.objects.get(id=branches),
                        #                                     company=Company.objects.get(user=request.user)
                        #                                     )
                        #                     stock.save()
                        #             except FuelStock.DoesNotExist:
                        #                     print("no matching Fuel found")
                        #                     stock=FuelStock(Fuel=FuelMaster.objects.get(id=saved_fuel), qty=saved_qty,
                        #                                     branches=Branches.objects.get(id=branches),
                        #                                     company=Company.objects.get(user=request.user)
                        #                                     )
                        #                     stock.save()

                        #             print("current credit balance=",account_balance.credit_balance)
                        #             print("cash balance amout after purchase ",cash_balance_purchase,)
                        #             BankAccountMaster.objects.filter(pk=bank_id).update(cash_balance=cash_balance_purchase,cash_credit_balance=total_cash_credit)
                        #             return Response({'msg':'Success', 'data':serializer.data},status.HTTP_201_CREATED)
                        #         return Response({'errors':serializer.errors,'msg':'Invalid data'},status.HTTP_422_UNPROCESSABLE_ENTITY)
                        #     else:
                        #         serializer = ReciptCreateSerializer(data=request.data, context={"request": request,"data":request.data})
                        #         if serializer.is_valid():
                        #             serializer.save()
                        #             saved_paid_amt=float(serializer.data['paid_amt'])
                        #             cash_balance_purchase=cash_balance-saved_paid_amt
                        #             saved_qty=float(serializer.data['qty'])
                        #             print("saved purchase quantity",saved_qty)
                        #             saved_fuel=float(serializer.data['fuel'])
                        #             branches=int(serializer.data['branches'])
                        #             try:
                        #                 fuel_stock=FuelStock.objects.get(Fuel=saved_fuel)

                        #                 if fuel_stock:
                        #                     print("fuel stock quantity",fuel_stock.qty)
                        #                     qty=float(fuel_stock.qty)+saved_qty
                        #                     FuelStock.objects.filter(pk=fuel_stock.id).update(qty=qty)
                        #                 elif fuel_stock==None:
                        #                     stock=FuelStock(Fuel=FuelMaster.objects.get(id=saved_fuel), qty=saved_qty,
                        #                                     branches=Branches.objects.get(id=branches),
                        #                                     company=Company.objects.get(user=request.user)
                        #                                     )
                        #                     stock.save()
                        #             except FuelStock.DoesNotExist:
                        #                     print("no matching Fuel found")
                        #                     stock=FuelStock(Fuel=FuelMaster.objects.get(id=saved_fuel), qty=saved_qty,
                        #                                     branches=Branches.objects.get(id=branches),
                        #                                     company=Company.objects.get(user=request.user)
                        #                                     )
                        #                     stock.save()
                        #             balance_amt = Invoice.objects.filter(type=1,payment_type=1).aggregate(Sum('balance_amt'))
                        #             total_cash_credit=balance_amt['balance_amt__sum']
                        #             print("cash balance amout after purchase ",cash_balance_purchase)
                        #             print("Data after purachase ",serializer.data)
                        #             print("current credit balance=",account_balance.credit_balance)
                        #             BankAccountMaster.objects.filter(pk=bank_id).update(cash_balance=cash_balance_purchase,cash_credit_balance=total_cash_credit)
                        #             return Response({'msg':'Success', 'data':serializer.data},status.HTTP_201_CREATED)
                        #         return Response({'errors':serializer.errors,'msg':'Invalid data'},status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                return Response({'msg': 'There is no sesion currently ,Please mak sure there is an open session'}, status.HTTP_403_FORBIDDEN)

        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)
            recipts = Invoice.objects.filter(
                type=3, company=manager.company_id, branches=manager.branches_id)
            serializer = ExpenseListSerielizer(
                recipts, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def retrieve(self, request, pk=None):
    #     try:
    #         recipt = Invoice.objects.filter(pk=pk,type=1,company=Company.objects.get(user=request.user))
    #         if not recipt:
    #             return  Response({'message':"invoice not found"},status=status.HTTP_404_NOT_FOUND)
    #         serializer = ReciptSerializer(recipt[0], context={"request": request})
    #         return Response({'msg':'Success', 'data':serializer.data},status.HTTP_200_OK)
    #     except Exception as e:
    #         print(e)
    #         return Response({'msg':'Server error' },status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def update(self, request, pk=None):
    #     try:
    #         print("Payment Type",request.data['payment_type'])
    #         if int(request.data['payment_type'])==2:
    #             print("===========updating payment type BAnk================")
    #             bank_id=request.data['bank_ac_id']

    #             recipt = Invoice.objects.filter(pk=pk,type=1,bank=bank_id,company=Company.objects.get(user=request.user))
    #             account=BankAccountMaster.objects.filter(pk=bank_id)
    #             print("currnt credit balance",account[0].credit_balance)
    #             current_credit_balance=account[0].credit_balance
    #             print("current bank credit",current_credit_balance)
    #             current_balance=account[0].balance
    #             print("current bank balance",current_balance)

    #             if not recipt:
    #                 return  Response({'message':"invoice not found"},status=status.HTTP_404_NOT_FOUND)
    #             serializer = ReciptUpdateSerializer(recipt[0], data=request.data, context={"request": request})
    #             if serializer.is_valid():
    #                 serializer.save()
    #                 balance_amt = Invoice.objects.filter(type=1,payment_type=2,bank=bank_id).aggregate(Sum('balance_amt'))
    #                 total_credit=balance_amt['balance_amt__sum']
    #                 credit_after_deduced_amt=current_credit_balance-total_credit
    #                 print("deduced amt after updation",credit_after_deduced_amt)
    #                 new_balance=current_balance-credit_after_deduced_amt
    #                 print("new balance after update",new_balance)

    #                 print("total bank credit",total_credit)
    #                 update=BankAccountMaster.objects.filter(pk=bank_id).update(credit_balance=total_credit,balance=new_balance)
    #                 print("bank account master object after update",update)

    #                 return Response({'msg':'Success', 'data':serializer.data},status.HTTP_200_OK)
    #             return Response({'errors':serializer.errors,'msg':'Invalid data'},status.HTTP_422_UNPROCESSABLE_ENTITY)
    #         elif int(request.data['payment_type'])==1:
    #             print("===========updating payment type cash================")
    #             bank_id=request.data['bank_ac_id']

    #             recipt = Invoice.objects.filter(pk=pk,type=1,bank=bank_id,company=Company.objects.get(user=request.user))
    #             account=BankAccountMaster.objects.filter(pk=bank_id)
    #             print("currnt credit balance",account[0].cash_credit_balance)
    #             current_cash_credit_balance=account[0].cash_credit_balance
    #             print("current cash credit",current_cash_credit_balance)
    #             current_balance=account[0].cash_balance
    #             print("current bank balance",current_balance)

    #             # balance_amt = Invoice.objects.filter(type=1,payment_type=1).aggregate(Sum('balance_amt'))
    #             if not recipt:
    #                 return  Response({'message':"invoice not found"},status=status.HTTP_404_NOT_FOUND)
    #             serializer = ReciptUpdateSerializer(recipt[0], data=request.data, context={"request": request})
    #             if serializer.is_valid():
    #                 serializer.save()
    #                 balance_amt = Invoice.objects.filter(type=1,payment_type=1,bank=bank_id).aggregate(Sum('balance_amt'))
    #                 total_cash_credit=balance_amt['balance_amt__sum']
    #                 print("total cash credit",total_cash_credit)
    #                 credit_after_deduced_amt=current_cash_credit_balance-total_cash_credit
    #                 print("deduced amt after updation",credit_after_deduced_amt)
    #                 new_balance=current_balance-credit_after_deduced_amt
    #                 print("new cash balance after update",new_balance)
    #                 update=BankAccountMaster.objects.filter(pk=bank_id).update(cash_credit_balance=total_cash_credit,cash_balance=new_balance)
    #                 print("bank account master object after update",update)
    #                 return Response({'msg':'Success', 'data':serializer.data},status.HTTP_200_OK)
    #             return Response({'errors':serializer.errors,'msg':'Invalid data'},status.HTTP_422_UNPROCESSABLE_ENTITY)

    #     except Exception as e:
    #         print(e)
    #         return Response({'msg':'Server error' },status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def destroy(self, request, pk=None):
    #     try:
    #         recipt = Invoice.objects.filter(pk=pk,type=1,company=Company.objects.get(user=request.user))
    #         if not recipt:
    #             return  Response({'message':"invoice not found"},status=status.HTTP_404_NOT_FOUND)
    #         recipt[0].delete()
    #         return Response({'msg':'Success'},status.HTTP_200_OK)

    #     except Exception as e:
    #         print(e)
    #         return Response({'msg':'Server error' },status.HTTP_500_INTERNAL_SERVER_ERROR)


class SaleReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, format=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            frm = request.query_params.get('from')
            to = request.query_params.get('to')
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            customer = request.query_params.get('customer')

            kwargs = {}

            if customer:
                kwargs['contact'] = customer
            if frm:
                today_min = frm
            if to:
                today_max = to
            # kwargs['branches']=manager.branches_id
            print('kwargs before retrieving data', kwargs)
            sale_data = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), type=2, branches=manager.branches_id)
            print("sale_data", sale_data.query)
            serializer = SaleReportSerializer(sale_data, many=True, context={
                                              "request": request, "data": kwargs, "datefrom": today_min, "dateto": today_max})
            data = serializer.data
            net_amount_sum_ag = Invoice.objects.filter(**kwargs, date__range=(
                today_min, today_max), type=2, branches=manager.branches_id).aggregate(Sum('total_amt'))
            # print(connection.queries)
            print("net amount sum", net_amount_sum_ag['total_amt__sum'])
            net_amount_sum = net_amount_sum_ag['total_amt__sum']
            print("after assigning", net_amount_sum)
            gross_amt_sum = Invoice.objects.filter(**kwargs, date__range=(
                today_min, today_max), type=2, branches=manager.branches_id).aggregate(Sum('gross_amt'))
            gross_amt_sum = gross_amt_sum['gross_amt__sum']
            net_vat_sum = Invoice.objects.filter(**kwargs, date__range=(
                today_min, today_max), type=2, branches=manager.branches_id).aggregate(Sum('vat_amount'))
            net_vat_sum = net_vat_sum['vat_amount__sum']
            totals = {}
            totals['net_amount_sum'] = net_amount_sum
            totals['gross_amt_sum'] = gross_amt_sum
            totals['net_vat_sum'] = net_vat_sum
            data.append(totals)
            return Response({'data': data, 'msg': 'Success'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExpenseReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, format=None):
        try:
            manager = BranchManager.objects.get(user=request.user)
            frm = request.query_params.get('from')
            to = request.query_params.get('to')
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            customer = request.query_params.get('customer')
            kwargs = {}
            if customer:
                kwargs['contact'] = customer
            if frm:
                today_min = frm
            if to:
                today_max = to
            # kwargs['branches']=manager.branches_id
            print('kwargs before retrieving data', kwargs)
            sale_data = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), type=3, branches=manager.branches_id)
            print("sale_data", sale_data.query)
            serializer = ExpenseReportSerializer(sale_data, many=True, context={
                                                 "request": request, "data": kwargs, "datefrom": today_min, "dateto": today_max})
            data = serializer.data
            net_amount_sum_ag = Invoice.objects.filter(**kwargs, date__range=(
                today_min, today_max), type=3, branches=manager.branches_id).aggregate(Sum('total_amt'))
            # print(connection.queries)
            print("net amount sum", net_amount_sum_ag['total_amt__sum'])
            net_amount_sum = net_amount_sum_ag['total_amt__sum']
            print("after assigning", net_amount_sum)
            gross_amt_sum = Invoice.objects.filter(**kwargs, date__range=(
                today_min, today_max), type=3, branches=manager.branches_id).aggregate(Sum('gross_amt'))
            gross_amt_sum = gross_amt_sum['gross_amt__sum']
            net_vat_sum = Invoice.objects.filter(**kwargs, date__range=(
                today_min, today_max), type=3, branches=manager.branches_id).aggregate(Sum('vat_amount'))
            net_vat_sum = net_vat_sum['vat_amount__sum']
            totals = {}
            totals['net_amount_sum'] = net_amount_sum
            totals['gross_amt_sum'] = gross_amt_sum
            data.append(totals)
            return Response({'data': data, 'msg': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class OwnerViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def create(self, request):
        try:

            serializer = OwnerCreateSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:

            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)
            owner = Owner.objects.filter(
                company=manager.company_id, branches=manager.branches_id)
            serializer = OwnerSerializer(
                owner, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            owner = Owner.objects.filter(
                pk=pk, company=manager.company_id, branches=manager.branches_id)
            if not owner:
                return Response({'message': "Owner not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = OwnerUpdateSerializer(
                owner[0], data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(e)

            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)
            owner = Owner.objects.filter(
                pk=pk, branches=manager.branches_id, company=manager.company_id)
            if not owner:
                return Response({'message': "Owner not found"}, status=status.HTTP_404_NOT_FOUND)
            owner[0].delete()
            return Response({'msg': 'Success'}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:

            manager = BranchManager.objects.get(user=request.user)
            owner = Owner.objects.filter(
                pk=pk, branches=manager.branches_id, company=manager.company_id)
            if not owner:
                return Response({'message': "Owner not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = OwnerSerializer(
                owner[0], context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class PurchaseReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, format=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            frm = request.query_params.get('from')
            to = request.query_params.get('to')
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            supllier = request.query_params.get('supplier')
            kwargs = {}

            if supllier:
                kwargs['contact'] = supllier
            if frm:
                today_min = frm
            if to:
                today_max = to

            print("kwargs", kwargs)
            purchase_details = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), type=1, branches=manager.branches_id)
            print(purchase_details.query)
            serializer = PurchaseReportSerializer(purchase_details, many=True, context={
                                                  "request": request, "data": kwargs, })
            data = serializer.data
            net_amount_sum_ag = Invoice.objects.filter(**kwargs, date__range=(
                today_min, today_max), type=1, branches=manager.branches_id).aggregate(Sum('total_amt'))
            # print(connection.queries)
            print("net amount sum", net_amount_sum_ag['total_amt__sum'])
            net_amount_sum = net_amount_sum_ag['total_amt__sum']
            print("after assigning", net_amount_sum)
            gross_amt_sum = Invoice.objects.filter(**kwargs, date__range=(
                today_min, today_max), type=1, branches=manager.branches_id).aggregate(Sum('gross_amt'))
            gross_amt_sum = gross_amt_sum['gross_amt__sum']
            net_vat_sum = Invoice.objects.filter(**kwargs, date__range=(
                today_min, today_max), type=1, branches=manager.branches_id).aggregate(Sum('vat_amount'))
            net_vat_sum = net_vat_sum['vat_amount__sum']
            totals = {}
            totals['net_amount_sum'] = net_amount_sum
            totals['gross_amt_sum'] = gross_amt_sum
            totals['net_vat_sum'] = net_vat_sum
            data.append(totals)
            return Response({'data': data, 'msg': 'Success'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class DebtorsReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, format=None):
        try:
            manager = BranchManager.objects.get(user=request.user)
            frm = request.query_params.get('from')
            to = request.query_params.get('to')
            branches = request.query_params.get('branches')
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            customer = request.query_params.get('customer')
            invoice_no = request.query_params.get('invoice_no')
            kwargs = {}
            if customer:
                kwargs['contact'] = customer
            if frm:
                today_min = frm
            if to:
                today_max = to

            if invoice_no:
                kwargs['invoice_no'] = invoice_no
            print("kwargs=", kwargs)
            sale_data = Invoice.objects.filter(**kwargs, date__range=(
                today_min, today_max), type=2, branches=manager.branches_id, balance_amt__gt=0)
            print(sale_data.query)
            serializer = DebtorsReportSerializer(sale_data, many=True, context={
                                                 "request": request, "data": kwargs, "datefrom": today_min, "dateto": today_max})
            return Response({'data': serializer.data, 'msg': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SupplierReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, format=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            # all =request.query_params.get('all')
            frm = request.query_params.get('from')
            to = request.query_params.get('to')
            # today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
            supllier = request.query_params.get('supplier')
            invoice_no = request.query_params.get('invoice_no')
            kwargs = {}

            if supllier:
                print("supplier statement")
                kwargs['contact'] = supllier

            if frm:
                today_min = frm
            if to:
                today_max = to

            if invoice_no:
                kwargs['invoice_no'] = invoice_no
            print("kwargs=", kwargs)
            supplier_data = Invoice.objects.filter(**kwargs, date__range=(
                today_min, today_max), type=1, branches=manager.branches_id, balance_amt__gt=0)

            print(supplier_data.query)

            serializer = SupplierReportSerializer(supplier_data, many=True, context={
                                                  "request": request, "data": kwargs})
            return Response({'data': serializer.data, 'msg': 'Success'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class IncomeReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, format=None):
        try:
            manager = BranchManager.objects.get(user=request.user)
            frm = request.query_params.get('from')
            to = request.query_params.get('to')
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            customer = request.query_params.get('customer')
            kwargs = {}
            if customer:
                kwargs['contact'] = customer
            kwargs = {}
            if frm:
                min = datetime.time.min
                today_min = frm+' '+str(min)
                print("date min", today_min)
            if to:
                max = datetime.time.max
                today_max = to+' '+str(max)
                print("date max", today_max)

            print("kwargs", kwargs)
            print("dates", today_min)
            print("dates", today_max)
            # details = Invoice.objects.filter(**kwargs,date__range=(today_min, today_max))
            total_sale = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), branches=manager.branches_id, type=2).aggregate(Sum('total_amt'))
            total_purchase = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), branches=manager.branches_id, type=1).aggregate(Sum('total_amt'))

            if total_sale['total_amt__sum'] is None:
                total_sale = 0
            else:
                total_sale = total_sale['total_amt__sum']

            if total_purchase['total_amt__sum'] is None:
                total_purchase = 0
            else:
                total_purchase = total_purchase['total_amt__sum']
            try:
                income = total_sale-total_purchase
            except Exception as e:
                print(e)
                return Response({'msg': 'Please contact system administrator'}, status=status.HTTP_200_OK)
            print("total_purchase", total_purchase)
            totals = {}
            totals['total_purchase'] = total_purchase
            totals['total_sale'] = total_sale
            totals['balance'] = income
            invoices = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), branches=manager.branches_id)
            print("Invoices List", invoices.query)
            # print(connection.queries)

            serializer = IncomeReportSerializer(invoices, many=True, context={
                                                "request": request, "data": kwargs, "datefrom": today_min, "dateto": today_max})
            data = {}
            data['data'] = serializer.data
            data['total'] = totals

            return Response({'data': data, 'msg': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class BranchCustomersViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)
            customers = Contact.objects.filter(
                branches=manager.branches_id, type=1)
            serializer = CustomerListSerielizer(
                customers, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class BranchBankViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)
            customers = BankAccountMaster.objects.filter(
                branches=manager.branches_id)
            serializer = BankAccountListSerielizer(
                customers, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SingleAccountViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def retrieve(self, request, pk=None):
        try:
            bank_ac = BankAccountMaster.objects.filter(pk=pk)
            if not bank_ac:
                return Response({'message': "Account not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = BankAccountListSerielizer(
                bank_ac[0], context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class PendingBalance(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def retrieve(self, request, pk=None):
        try:
            balance_amt = Invoice.objects.filter(
                type=2, contact=pk).aggregate(Sum('balance_amt'))
            balance = balance_amt['balance_amt__sum']
            if not balance_amt:
                return Response({'message': "Account not found"}, status=status.HTTP_404_NOT_FOUND)
            totals = {}
            totals['balance_amt_sum'] = balance
            return Response({'msg': 'Success', 'data': totals}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class BranchSupplierViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)
            customers = Contact.objects.filter(
                branches=manager.branches_id, type=2)
            serializer = SupplierListSerielizer(
                customers, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class PurchasePendingBalance(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def retrieve(self, request, pk=None):
        try:
            balance_amt = Invoice.objects.filter(
                type=1, contact=pk).aggregate(Sum('balance_amt'))
            balance = balance_amt['balance_amt__sum']
            if not balance_amt:
                return Response({'message': "Account not found"}, status=status.HTTP_404_NOT_FOUND)
            totals = {}
            totals['balance_amt_sum'] = balance
            return Response({'msg': 'Success', 'data': totals}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExpenseReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, format=None):
        try:
            manager = BranchManager.objects.get(user=request.user)
            frm = request.query_params.get('from')
            to = request.query_params.get('to')
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            customer = request.query_params.get('customer')
            kwargs = {}
            if customer:
                kwargs['contact'] = customer
            if frm:
                today_min = frm
            if to:
                today_max = to
            kwargs['branches'] = manager.branches_id
            sale_data = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), type=3)
            print("sale_data", sale_data.query)
            serializer = ExpenseReportSerializer(sale_data, many=True, context={
                                                 "request": request, "data": kwargs, "datefrom": today_min, "dateto": today_max})
            list_data = serializer.data
            net_amount_sum_ag = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), type=3).aggregate(Sum('total_amt'))
            # print(connection.queries)
            print("net amount sum", net_amount_sum_ag['total_amt__sum'])
            net_amount_sum = net_amount_sum_ag['total_amt__sum']
            print("after assigning", net_amount_sum)
            gross_amt_sum = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), type=3).aggregate(Sum('gross_amt'))
            gross_amt_sum = gross_amt_sum['gross_amt__sum']
            # net_vat_sum = Invoice.objects.filter(**kwargs,date__range=(today_min, today_max),type=2).aggregate(Sum('vat_amount'))
            # net_vat_sum =net_vat_sum['vat_amount__sum']
            totals = {}
            totals['net_amount_sum'] = net_amount_sum
            totals['gross_amt_sum'] = gross_amt_sum
            # data.append(totals)
            data = {}
            data['data'] = list_data
            data['total'] = totals
            # totals['net_vat_sum']=net_vat_sum
            # data.append(totals)
            return Response({'data': data, 'msg': 'Success'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class MeterReadingReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, format=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            frm = request.query_params.get('from')
            to = request.query_params.get('to')
            branches = request.query_params.get('branches')
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            dispencer = request.query_params.get('dispencer')
            kwargs = {}
            if dispencer:

                kwargs['dispence'] = dispencer
            if frm:
                # date=datetime.datetime.strptime(frm, "%Y-%m-%d").date()

                # date=dateutil.par
                min = datetime.time.min
                today_min = frm+' '+str(min)
                print("date min", today_min)
            if to:
                max = datetime.time.max
                today_max = to+' '+str(max)
                print("date max", today_max)

            kwargs['branches'] = manager.branches_id
            meter_reading = MeterReading.objects.filter(
                **kwargs, date__range=(today_min, today_max))
            print("sale_data", meter_reading.query)
            serializer = MeterReadingReporSerielizer(meter_reading, many=True, context={
                                                     "request": request, "data": kwargs, "datefrom": today_min, "dateto": today_max})
            list_data = serializer.data
            total_payable_amount = MeterReading.objects.filter(
                **kwargs, date__range=(today_min, today_max)).aggregate(Sum('payable_amt'))
            print("Toatl payable amount", total_payable_amount)
            # print("net amount sum",total_payable_amount['total_amt__sum'])
            net_amount_sum = total_payable_amount['payable_amt__sum']
            print("after assigning", net_amount_sum)
            totals = {}
            totals['payable_amount_sum'] = net_amount_sum
            data = {}
            data['data'] = list_data
            data['total'] = totals
            # data.append(totals)
            return Response({'data': data, 'msg': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerBalanceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, format=None):
        try:
            manager = BranchManager.objects.get(user=request.user)
            frm = request.query_params.get('from')
            to = request.query_params.get('to')
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            customer = request.query_params.get('customer')
            invoice_no = request.query_params.get('invoice_no')
            mobile_no = request.query_params.get('phone')
            lan_no = request.query_params.get('lan')
            en_name = request.query_params.get('name')
            ar_name = request.query_params.get('ar_name')
            kwargs = {}
            if mobile_no:
                try:
                    customer = Contact.objects.filter(
                        mobile_no__contains=mobile_no)
                    print(customer.query)
                    print("cutomer mobile number", customer[0].en_name)
                    # print("cutomer name",customer.en_name)
                    kwargs['contact'] = customer[0].id
                except IndexError:
                    pass
            if lan_no:
                try:
                    customer = Contact.objects.filter(lan_no__contains=lan_no)
                    print(customer.query)
                    print("cutomer mobile number", customer[0].en_name)
                    # print("cutomer name",customer.en_name)
                    kwargs['contact'] = customer[0].id
                except IndexError:
                    pass
            if en_name:
                try:
                    customer = Contact.objects.filter(
                        en_name__contains=en_name)
                    print(customer.query)
                    print("cutomer mobile number", customer[0].en_name)
                    # print("cutomer name",customer.en_name)
                    kwargs['contact'] = customer[0].id
                except IndexError:
                    pass
            if ar_name:
                try:
                    customer = Contact.objects.filter(
                        ar_name__contains=ar_name)
                    print(customer.query)
                    print("cutomer mobile number", customer[0].ar_name)
                    # print("cutomer name",customer.en_name)
                    kwargs['contact'] = customer[0].id
                except IndexError:
                    pass
            if frm:
                min = datetime.time.min
                today_min = frm+' '+str(min)
                print("date min", today_min)
            if to:
                max = datetime.time.max
                today_max = to+' '+str(max)
                print("date max", today_max)

            kwargs['branches'] = manager.branches_id
            if invoice_no:
                kwargs['invoice_no'] = invoice_no
            print("kwargs=", kwargs)
            sale_data = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), type=2, balance_amt__gt=0)
            print(sale_data.query)
            serializer = DebtorsReportSerializer(sale_data, many=True, context={
                                                 "request": request, "data": kwargs, "datefrom": today_min, "dateto": today_max})
            list_data = serializer.data
            amount = Invoice.objects.filter(**kwargs, date__range=(
                today_min, today_max), type=2, balance_amt__gt=0).aggregate(Sum('balance_amt'))
            net_amt_sum = amount['balance_amt__sum']
            totals = {}
            totals['amount'] = net_amt_sum
            # data.append(totals)
            data = {}
            data['data'] = list_data
            data['amount'] = totals
            return Response({'data': data, 'msg': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepositReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, format=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            frm = request.query_params.get('from')
            to = request.query_params.get('to')
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            owner = request.query_params.get('owner')
            account = request.query_params.get('account')
            kwargs = {}
            if frm:
                min = datetime.time.min
                today_min = frm+' '+str(min)
                print("date min", today_min)
            if to:
                max = datetime.time.max
                today_max = to+' '+str(max)
            if owner:
                kwargs['owner'] = owner
            if account:
                kwargs['bank'] = account
            kwargs['branches'] = manager.branches_id
            deposit_data = Deposit.objects.filter(
                **kwargs, date__range=(today_min, today_max))
            print(deposit_data.query)
            serializer = DepositReportSerializer(deposit_data, many=True, context={
                                                 "request": request, "data": kwargs, "datefrom": today_min, "dateto": today_max})
            list_data = serializer.data
            amount = Deposit.objects.filter(
                **kwargs, date__range=(today_min, today_max)).aggregate(Sum('amount'))
            net_amt_sum = amount['amount__sum']
            totals = {}
            totals['amount'] = net_amt_sum
            data = {}
            data['data'] = list_data
            data['amount'] = totals
            return Response({'data': data, 'msg': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentDetailsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, format=None):
        try:
            manager = BranchManager.objects.get(user=request.user)
            month = request.query_params.get('month')
            year = request.query_params.get('year')
            kwargs = {}
            if month:
                kwargs['date__month'] = month
            if year:
                kwargs['date__year'] = year

            kwargs['branches'] = manager.branches_id
            print("kwargs", kwargs)
            purchase_details = Invoice.objects.filter(**kwargs, type=1)
            print(purchase_details.query)
            serializer = PurchaseReportSerializer(purchase_details, many=True, context={
                                                  "request": request, "data": kwargs, })
            list_data = serializer.data
            net_amount_sum_ag = Invoice.objects.filter(
                **kwargs, type=1).aggregate(Sum('total_amt'))
            net_amount_sum = net_amount_sum_ag['total_amt__sum']
            print("after assigning", net_amount_sum)
            gross_amt_sum = Invoice.objects.filter(
                **kwargs, type=1).aggregate(Sum('gross_amt'))
            gross_amt_sum = gross_amt_sum['gross_amt__sum']
            net_vat_sum = Invoice.objects.filter(
                **kwargs, type=1).aggregate(Sum('vat_amount'))
            net_vat_sum = net_vat_sum['vat_amount__sum']
            totals = {}
            totals['net_amount_sum'] = net_amount_sum
            totals['gross_amt_sum'] = gross_amt_sum
            totals['net_vat_sum'] = net_vat_sum
            data = {}
            data['data'] = list_data
            data['total'] = totals
            return Response({'data': data, 'msg': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentDueViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, format=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            frm = request.query_params.get('from')
            to = request.query_params.get('to')
            invoice_type = request.query_params.get('invoice_type')
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            contact = request.query_params.get('contact')
            kwargs = {}
            if contact:
                kwargs['contact'] = contact
            if frm:
                min = datetime.time.min
                today_min = frm+' '+str(min)
                print("date min", today_min)
            if to:
                max = datetime.time.max
                today_max = to+' '+str(max)
            if invoice_type:
                kwargs['type'] = invoice_type
            print("kwargs=", kwargs)
            kwargs['branches'] = manager.branches_id
            sale_data = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), balance_amt__gt=0)
            print(sale_data.query)
            serializer = PaymentDueReportSerializer(sale_data, many=True, context={
                                                    "request": request, "data": kwargs, "datefrom": today_min, "dateto": today_max})
            list_data = serializer.data
            amount = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), balance_amt__gt=0).aggregate(Sum('balance_amt'))
            net_amt_sum = amount['balance_amt__sum']
            totals = {}
            totals['amount'] = net_amt_sum
            data = {}
            data['data'] = list_data
            data['amount'] = totals
            return Response({'data': data, 'msg': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentInReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, format=None):
        try:
            manager = BranchManager.objects.get(user=request.user)
            frm = request.query_params.get('from')
            to = request.query_params.get('to')
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            supllier = request.query_params.get('supplier')
            invoice_no = request.query_params.get('invoice_no')
            kwargs = {}
            if supllier:
                kwargs['contact'] = supllier
            if frm:
                min = datetime.time.min
                today_min = frm+' '+str(min)
                print("date min", today_min)
            if to:
                max = datetime.time.max
                today_max = to+' '+str(max)
                print("date max", today_max)
            if invoice_no:
                kwargs['invoice_no'] = invoice_no
            kwargs['branches'] = manager.branches_id
            print("kwargs", kwargs)
            purchase_details = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), type=1)
            print(purchase_details.query)
            serializer = PaymentInReportSerializer(purchase_details, many=True, context={
                                                   "request": request, "data": kwargs, })
            list_data = serializer.data
            net_amount_sum_ag = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), type=1).aggregate(Sum('total_amt'))
            # print(connection.queries)
            print("net amount sum", net_amount_sum_ag['total_amt__sum'])
            net_amount_sum = net_amount_sum_ag['total_amt__sum']
            print("after assigning", net_amount_sum)
            gross_amt_sum = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), type=1).aggregate(Sum('gross_amt'))
            gross_amt_sum = gross_amt_sum['gross_amt__sum']
            net_vat_sum = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), type=1).aggregate(Sum('vat_amount'))
            net_vat_sum = net_vat_sum['vat_amount__sum']
            totals = {}
            totals['net_amount_sum'] = net_amount_sum
            totals['gross_amt_sum'] = gross_amt_sum
            totals['net_vat_sum'] = net_vat_sum
            data = {}
            data['data'] = list_data
            data['total'] = totals
            # data.append(totals)
            return Response({'data': data, 'msg': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentOutReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, format=None):
        try:
            manager = BranchManager.objects.get(user=request.user)
            frm = request.query_params.get('from')
            to = request.query_params.get('to')
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            customer = request.query_params.get('customer')
            invoice_no = request.query_params.get('invoice_no')
            kwargs = {}
            if customer:
                kwargs['contact'] = customer
            if frm:
                min = datetime.time.min
                today_min = frm+' '+str(min)
                print("date min", today_min)
            if to:
                max = datetime.time.max
                today_max = to+' '+str(max)
                print("date max", today_max)
            if invoice_no:
                kwargs['invoice_no'] = invoice_no
            kwargs['branches'] = manager.branches_id
            print("kwargs=", kwargs)
            sale_data = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), type=2)
            print("sale_data", sale_data.query)
            serializer = PaymentOutReportSerializer(sale_data, many=True, context={
                                                    "request": request, "data": kwargs, "datefrom": today_min, "dateto": today_max})
            list_data = serializer.data
            net_amount_sum_ag = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), type=2).aggregate(Sum('total_amt'))
            print("net amount sum", net_amount_sum_ag['total_amt__sum'])
            net_amount_sum = net_amount_sum_ag['total_amt__sum']
            print("after assigning", net_amount_sum)
            gross_amt_sum = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), type=2).aggregate(Sum('gross_amt'))
            gross_amt_sum = gross_amt_sum['gross_amt__sum']
            net_vat_sum = Invoice.objects.filter(
                **kwargs, date__range=(today_min, today_max), type=2).aggregate(Sum('vat_amount'))
            net_vat_sum = net_vat_sum['vat_amount__sum']
            totals = {}
            totals['net_amount_sum'] = net_amount_sum
            totals['gross_amt_sum'] = gross_amt_sum
            totals['net_vat_sum'] = net_vat_sum
            data = {}
            data['data'] = list_data
            data['total'] = totals
            return Response({'data': data, 'msg': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class FuelStockViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def create(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)

            if FuelStock.objects.filter(branches=manager.branches_id, Fuel=request.data['Fuel']).exists():
                return Response({'msg': 'Fuel Stock Already Added'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            serializer = FuelStockCreateSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_201_CREATED)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            manager = BranchManager.objects.get(user=request.user)
            fuelstocks = FuelStock.objects.filter(branches=manager.branches_id)
            serializer = FuelStockSerializer(
                fuelstocks, many=True, context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)
            fuelstock = FuelStock.objects.filter(
                pk=pk, branches=manager.branches_id)
            if not fuelstock:
                return Response({'message': "Dispence not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = FuelStockSerializer(
                fuelstock[0], data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
            return Response({'errors': serializer.errors, 'msg': 'Invalid data'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)
            fuelstock = FuelStock.objects.filter(
                pk=pk, branches=manager.branches_id)
            if not fuelstock:
                return Response({'message': "Not found"}, status=status.HTTP_404_NOT_FOUND)
            fuelstock[0].delete()
            return Response({'msg': 'Success'}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            fuelstock = FuelStock.objects.filter(
                pk=pk, branches=manager.branches_id)
            if not fuelstock:
                return Response({'message': "Fuel stock not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = FuelStockSerializer(
                fuelstock[0], context={"request": request})
            return Response({'msg': 'Success', 'data': serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SessionReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, format=None):
        try:
            manager = BranchManager.objects.get(user=request.user)

            frm = request.query_params.get('from')
            to = request.query_params.get('to')
            today_min = datetime.datetime.combine(
                datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(
                datetime.date.today(), datetime.time.max)
            kwargs = {}
            if frm:
                min = datetime.time.min
                today_min = frm+' '+str(min)
                print("date min", today_min)
            if to:
                max = datetime.time.max
                today_max = to+' '+str(max)
                print("date max", today_max)

            print("kwargs=", kwargs)
            session_data = DailySession.objects.filter(
                branches=manager.branches_id, date__range=(today_min, today_max))
            print(session_data.query)
            serializer = SessionReportSerializer(session_data, many=True, context={
                                                 "request": request})
            list_data = serializer.data
            data = {}
            data['data'] = list_data
            return Response({'data': data, 'msg': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SessionAccountReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def retrieve(self, request, pk=None):
        try:

            session_data = AccountLedger.objects.filter(session_id=pk)
            print(session_data.query)
            serializer = SessionAccountReportSerializer(session_data, many=True, context={
                "request": request})
            list_data = serializer.data
            # data = {}
            # data['data'] = list_data
            return Response({'data': list_data, 'msg': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg': 'Server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class AppPasswordChange(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsManager]

    def create(self, request, format=None):
        try:
            serializer = ChangePasswordSerializer(
                data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Success'}, status.HTTP_201_CREATED)
            return Response({'msg': 'Invalid data', 'error': serializer.errors}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(e)
            return Response({'message': "Invalid Email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
