from django.shortcuts import render
import datetime
from django.db import connection


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from employee.serielizer import BranchSerializer, ChangePasswordSerializer, DispenceSerializer, InvoiceCreateSerializer, MeterCreateSerializer, MeterSerializer,FuelSerializer,VatSerializer,BankSerializer
from employee.permissions import IsEmployee
from company.models import BankAccountMaster, CashMaster, DailySession, Dispence, FuelMaster, FuelStock, Invoice, MeterReading, VatMaster
from administrator.models import BranchManager, Branches, Company, Employee


class EmployeeInvoiceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,IsEmployee]
    
    def create(self, request):
        try:
            employee=Employee.objects.get(user=request.user)
            print("manager id is",employee.id)
            print("Payment Type",request.data['payment_type'])
            date_today=datetime.date.today()
            print("date today",date_today)
            today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
            today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
            session=DailySession.objects.filter(branches_id=employee.branches_id,date__range=(today_min, today_max),status=False)
            print(connection.queries)                  
            print("last session command woeking",session)
            if session:
                request.data['session_id']=session[0].id
                print("matching session found for today") 
                if int(request.data['payment_type'])==2:
                    print("request",request)
                    print("request data",request.data)
                    print("Paid Amount",request.data['paid_amt'])
                    branch_id=employee.branches_id
                    if branch_id:
                        account_balance=BankAccountMaster.objects.get(branches=branch_id,is_default=True)
                        print("Rbank account",account_balance)
                        print("Rbank account",account_balance.balance)
                        bank_balance=float(account_balance.balance)
                        print("is default bank account",account_balance.is_default)
                        if account_balance.is_default:         
                            serializer = InvoiceCreateSerializer(data=request.data, context={"request": request,"data":request.data})
                            if serializer.is_valid():
                                serializer.save()
                                saved_paid_amt=float(serializer.data['paid_amt'])
                                saved_qty=float(serializer.data['qty'])
                                print("saved purchase quantity",saved_qty)
                                saved_fuel=float(serializer.data['fuel'])
                                try:
                                    print("fuel stock updation")
                                    fuel_master=FuelMaster.objects.get(id=saved_fuel)
                                    if fuel_master:
                                        new_current_stock=float(fuel_master.current_stock)-saved_qty
                                        FuelMaster.objects.filter(pk=saved_fuel).update(current_stock=new_current_stock)    
                                except FuelMaster.DoesNotExist:
                                    print("no matching Fuel found")
                                    return Response({'msg':'Fuel not found'},status.HTTP_422_UNPROCESSABLE_ENTITY)
                                sale_balance=bank_balance+saved_paid_amt
                                print("Account responsible",account_balance)
                                print("bank balance amout after Sale ",sale_balance,)
                                BankAccountMaster.objects.filter(branches=branch_id,is_default=True).update(balance=sale_balance,)    
                                return Response({'msg':'Success', 'data':serializer.data},status.HTTP_201_CREATED)
                            return Response({'errors':serializer.errors,'msg':'Invalid data'},status.HTTP_422_UNPROCESSABLE_ENTITY)
                        else:
                            serializer = InvoiceCreateSerializer(data=request.data, context={"request": request,"data":request.data})
                            if serializer.is_valid():
                                serializer.save()
                                saved_paid_amt=float(serializer.data['paid_amt'])
                                saved_qty=float(serializer.data['qty'])
                                print("saved purchase quantity",saved_qty)
                                saved_fuel=float(serializer.data['fuel'])
                                # branches=int(serializer.data['branches'])
                                try:
                                    print("fuel stock updation")
                                    fuel_master=FuelMaster.objects.get(id=saved_fuel)
                                    if fuel_master:
                                        new_current_stock=float(fuel_master.current_stock)-saved_qty
                                        FuelMaster.objects.filter(pk=saved_fuel).update(current_stock=new_current_stock)    
                                except FuelMaster.DoesNotExist:
                                    print("no matching Fuel found")
                                    return Response({'msg':'Fuel not found'},status.HTTP_422_UNPROCESSABLE_ENTITY)
                                sale_balance=bank_balance+saved_paid_amt
                                print("current debit balance=",account_balance.debit_balance)
                                print("bank balance amout after Sale ",sale_balance,)
                                BankAccountMaster.objects.filter(branches=branch_id,is_default=True).update(balance=sale_balance)    
                                return Response({'msg':'Success', 'data':serializer.data},status.HTTP_201_CREATED)
                            return Response({'errors':serializer.errors,'msg':'Invalid data'},status.HTTP_422_UNPROCESSABLE_ENTITY)
                elif int(request.data['payment_type'])==1:
                    print("payment type is cash")
                    print("request data",request.data)
                    print("Paid Amount",request.data['paid_amt'])
                    branch_id=employee.branches_id
                    if branch_id:
                        cash_account=CashMaster.objects.get(branches =branch_id)
                        print("Cash account",cash_account)
                        print("cash account balance",cash_account.balance)
                        cash_balance=float(cash_account.balance)
                        serializer = InvoiceCreateSerializer(data=request.data, context={"request": request,"data":request.data})
                        if serializer.is_valid():
                            serializer.save()
                            saved_paid_amt=float(serializer.data['paid_amt'])
                            saved_qty=float(serializer.data['qty'])
                            print("saved purchase quantity",saved_qty)
                            saved_fuel=float(serializer.data['fuel'])
                            try:
                                print("fuel stock updation")
                                fuel_master=FuelMaster.objects.get(id=saved_fuel)
                                if fuel_master:
                                    new_current_stock=float(fuel_master.current_stock)-saved_qty
                                    FuelMaster.objects.filter(pk=saved_fuel).update(current_stock=new_current_stock)    
                            except FuelMaster.DoesNotExist:
                                print("no matching Fuel found")
                                return Response({'msg':'Fuel not found'},status.HTTP_422_UNPROCESSABLE_ENTITY)
                            sale_cash_balance=cash_balance+saved_paid_amt
                            print("current cash debit balance=",cash_account.debit_balance)
                            print("cash balance amout after sale ",sale_cash_balance)
                            CashMaster.objects.filter(branches=branch_id).update(balance=sale_cash_balance)    
                            return Response({'msg':'Success', 'data':serializer.data},status.HTTP_201_CREATED)
                        return Response({'errors':serializer.errors,'msg':'Invalid data'},status.HTTP_422_UNPROCESSABLE_ENTITY)

            elif session==None:
                return Response({'msg':'There is no sesion currently ,Please mak sure there is an open session'},status.HTTP_403_FORBIDDEN)
            else:
                return Response({'msg':'There is no sesion currently ,Please mak sure there is an open session'},status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response({'msg':'Server error' },status.HTTP_500_INTERNAL_SERVER_ERROR)
  








# class GetAmount(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         try:
#             # vat = VatMaster.objects.values_list('vat').first()
#             # print("function working",request.query_params)
#             fuel = request.query_params.get('fuel')
#             print(fuel)
#             liter = request.query_params.get('liter')
#             print(liter)            
          
#             fuel_data = FuelMaster.objects.get(id=fuel)
#             # fuel_data = FuelMaster.objects.filter(id=fuel)
#             print("fuel=",fuel_data)            
#             # print("fuel=",FuelMaster.__dict__)            
#             serializer = FuelSerializer(fuel_data)
#             # amt = (vat + serializer.data.get('fuel_vat') + serializer.data.get('rate')) * liter
#             # 
#             amt = (serializer.data.get('vat') + serializer.data.get('fuel_vat') + serializer.data.get('rate'))* float(liter)
#             #  
#             return Response({'data': amt, 'data':amt},status=status.HTTP_200_OK)
#         except Exception as e:
#             print(e)
#             return Response({'msg':'Server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)






class MeterReadingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,IsEmployee]
    
    def create(self, request):
        try:
            serializer = MeterCreateSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Success', 'data':serializer.data},status.HTTP_201_CREATED)
            return Response({'errors':serializer.errors,'msg':'Invalid data'},status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(e)
            return Response({'msg':'Server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        try:
            emp=Employee.objects.get(user=request.user)
            print(emp)
            meter_reading = MeterReading.objects.filter(company=Company.objects.get(id=emp.company_id,branches=emp.branches_id))
            serializer = MeterSerializer(meter_reading, many=True, context={"request": request})
            return Response({'msg':'Success', 'data':serializer.data},status.HTTP_200_OK)
        except  Exception as e:
            print(e)
            return Response({'msg':'Server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            meter_reading = MeterReading.objects.filter(pk=pk)
            if not meter_reading:
                return  Response({'message':"Meter Reading not found"},status=status.HTTP_404_NOT_FOUND)
            serializer = MeterSerializer(meter_reading[0], context={"request": request})
            return Response({'msg':'Success', 'data':serializer.data},status.HTTP_200_OK)
        except:
            return Response({'msg':'Server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            meter_reading = MeterReading.objects.filter(pk=pk)
            if not meter_reading:
                return  Response({'message':"Meter Reading not found"},status=status.HTTP_404_NOT_FOUND)
            serializer = MeterSerializer(meter_reading[0], data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Success', 'data':serializer.data},status.HTTP_200_OK)
            return Response({'errors':serializer.errors,'msg':'Invalid data'},status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'msg':'Server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, pk=None):
        try:
            meter_reading = MeterReading.objects.filter(pk=pk)
            if not meter_reading:
                return  Response({'message':"Meter Reading not found"},status=status.HTTP_404_NOT_FOUND)
            meter_reading[0].delete()
            return Response({'msg':'Success'},status.HTTP_200_OK)
        except:
            return Response({'msg':'Server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)


class FuelMasterViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,IsEmployee]
    

    def list(self, request):
        try:
            emp=Employee.objects.get(user=request.user)
            fuel = FuelMaster.objects.filter(company=Company.objects.get(id=emp.company_id))
            serializer = FuelSerializer(fuel, many=True, context={"request": request})
            return Response({'msg':'Success', 'data':serializer.data},status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg':'Server error' },status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            emp=Employee.objects.get(user=request.user)
            fuel = FuelMaster.objects.filter(pk=pk,company=Company.objects.get(id=emp.company_id))
            if not fuel:
                return  Response({'message':"Fuel not found"},status=status.HTTP_404_NOT_FOUND)
            serializer = FuelSerializer(fuel[0], context={"request": request})
            return Response({'msg':'Success', 'data':serializer.data},status.HTTP_200_OK)
        except:
            return Response({'msg':'Server error' },status.HTTP_500_INTERNAL_SERVER_ERROR)



class VatMasterViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,IsEmployee]
    
    def list(self, request):
        try:
            emp=Employee.objects.get(user=request.user)
            # vat = VatMaster.objects.filter(company=Company.objects.get(id=emp.company_id), branches=emp.branches_id)
            vat = VatMaster.objects.filter(company=Company.objects.get(id=emp.company_id))
            serializer = VatSerializer(vat, many=True, context={"request": request})
            return Response({'msg':'Success', 'data':serializer.data},status.HTTP_200_OK)
        except:
            return Response({'msg':'Server error' },status.HTTP_500_INTERNAL_SERVER_ERROR)
    # def retrieve(self, request, pk=None):
    #     try:
    #         emp=Employee.objects.get(user=request.user)
    #         supplier = VatMaster.objects.filter(pk=pk,company=Company.objects.get(id=emp.company_id), branches=emp.branches_id)
    #         if not supplier:
    #             return  Response({'message':"Vat not found"},status=status.HTTP_404_NOT_FOUND)
    #         serializer = VatSerializer(supplier[0], context={"request": request})
    #         return Response({'msg':'Success', 'data':serializer.data},status.HTTP_200_OK)
    #     except:
    #         return Response({'msg':'Server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)
class BranchDetailsViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,IsEmployee]
    
    def list(self, request, pk=None):
        try:
            emp=Employee.objects.get(user=request.user)
            company=Branches.objects.get(id=emp.branches_id)
            if not company:
                return  Response({'message':"Fuel not found"},status=status.HTTP_404_NOT_FOUND)
            serializer = BranchSerializer(company, context={"request": request})
            return Response({'msg':'Success', 'data':serializer.data},status.HTTP_200_OK)
        except Exception as e:
            print(e)
            
            return Response({'msg':'Server error' },status.HTTP_500_INTERNAL_SERVER_ERROR)


    
class BankViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,IsEmployee]
    
    
    def list(self, request):
        try:
            emp=Employee.objects.get(user=request.user)
            bank = BankAccountMaster.objects.filter(company=Company.objects.get(id=emp.company_id), branches=emp.branches_id,is_default=True)
            serializer = BankSerializer(bank, many=True, context={"request": request})
            return Response({'msg':'Success', 'data':serializer.data},status.HTTP_200_OK)
        except:
            return Response({'msg':'Server error' },status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def retrieve(self, request, pk=None):
    #     try:
    #         manager=BranchManager.objects.get(user=request.user)

    #         bank = BankAccountMaster.objects.filter(pk=pk,company=Company.objects.get(id=manager.company_id), branches=Branches.objects.get(id=manager.branches_id))
    #         if not bank:
    #             return  Response({'message':"Bank not found"},status=status.HTTP_404_NOT_FOUND)
    #         serializer = BankSerializer(bank[0], context={"request": request})
    #         return Response({'msg':'Success', 'data':serializer.data},status.HTTP_200_OK)
    #     except:
    #         return Response({'msg':'Server error' },status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DispenceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,IsEmployee]
  
  
    def list(self, request):
        try:
            emp=Employee.objects.get(user=request.user)
            dispence = Dispence.objects.filter(company=Company.objects.get(id=emp.company_id), branches=emp.branches_id)
            dispencer_count = Dispence.objects.filter(company=Company.objects.get(id=emp.company_id), branches=emp.branches_id).count()
            # print("count of dispencers",dispencer_count)
            serializer = DispenceSerializer(dispence, many=True, context={"request": request,"data":dispencer_count})
            # print(serializer.data[0].append(dispencer_count))
            # serializer.data.append=dispencer_count
            return Response({'msg':'Success', 'data':serializer.data},status.HTTP_200_OK)
        except  Exception as e:
            print(e)
            return Response({'msg':'Server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def retrieve(self, request, pk=None):
        try:
            emp=Employee.objects.get(user=request.user)


            dispence = Dispence.objects.filter(pk=pk,company=Company.objects.get(id=emp.company_id), branches=emp.branches_id)
            if not dispence:
                return  Response({'message':"Dispence not found"},status=status.HTTP_404_NOT_FOUND)
            serializer = DispenceSerializer(dispence[0], context={"request": request})
            print("serializer.data after sereilizatin-================>",serializer.data)
            return Response({'msg':'Success', 'data':serializer.data},status.HTTP_200_OK)
        except:
            return Response({'msg':'Server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)


class PreviousMeterReading(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,IsEmployee]
    
    def retrieve(self, request, pk=None):
        try:
            emp=Employee.objects.get(user=request.user)
            meter_rading = MeterReading.objects.filter(dispence=pk,company=Company.objects.get(id=emp.company_id), branches=emp.branches_id).order_by('date').last()
            if not meter_rading:
                return  Response({'message':"Dispence not found"},status=status.HTTP_404_NOT_FOUND)
            print(meter_rading.start_reading)
            print(meter_rading.id)
            print(meter_rading.end_reading)
            data={}
            data["previous_meter_reading"]=meter_rading.end_reading
            return Response({'msg':'Success', 'data':data},status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg':'Server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PreviousMeterReading(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,IsEmployee]
    
    def retrieve(self, request, pk=None):
        try:
            emp=Employee.objects.get(user=request.user)
            meter_rading = MeterReading.objects.filter(dispence=pk,company=Company.objects.get(id=emp.company_id), branches=emp.branches_id).order_by('date').last()
            if not meter_rading:
                return  Response({'message':"Dispence not found"},status=status.HTTP_404_NOT_FOUND)
            print(meter_rading.start_reading)
            print(meter_rading.id)
            print(meter_rading.end_reading)
            data={}
            data["previous_meter_reading"]=meter_rading.end_reading
            return Response({'msg':'Success', 'data':data},status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'msg':'Server error'},status.HTTP_500_INTERNAL_SERVER_ERROR)


class AppPasswordChange(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,IsEmployee]
    
    def create(self, request, format=None):
        try:
            serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Success'},status.HTTP_201_CREATED)
            return Response({'msg':'Invalid data','error':serializer.errors},status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(e)
            return Response({'message':"Invalid Email"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)