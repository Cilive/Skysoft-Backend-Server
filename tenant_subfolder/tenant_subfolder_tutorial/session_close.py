
# from company.models import DailySession


# def close_sessions():
#     print("this function runs every 10 seconds")
    
    # # print("session",self)s
    # session = DailySession.objects.filter(pk=pk,branches=request.data['branches'])
    
    # print("session",self.context['data'])
    # data=self.context['data']
    # session=data[0]
    # # invoice_data=Invoice.objects.filter(session=session,)
    # total_transactions = Invoice.objects.filter(session=session,).aggregate(Sum('total_amt'))
    # total_transactions=total_transactions['total_amt__sum']
    # total_sale_by_cash = Invoice.objects.filter(session=session,payment_type=1,type=2).aggregate(Sum('total_amt'))
    # total_sale_by_cash=total_sale_by_cash['total_amt__sum']
    # total_purchase_by_cash = Invoice.objects.filter(session=session,payment_type=1,type=1).aggregate(Sum('total_amt'))
    # total_purchase_by_cash=total_purchase_by_cash['total_amt__sum']
    # total_expense_by_cash = Invoice.objects.filter(session=session,payment_type=1,type=3).aggregate(Sum('total_amt'))
    # total_expense_by_cash=total_expense_by_cash['total_amt__sum']
    # total_sale_by_bank = Invoice.objects.filter(session=session,payment_type=2,type=2).aggregate(Sum('total_amt'))
    # total_sale_by_bank=total_sale_by_bank['total_amt__sum']
    # total_purchase_by_bank = Invoice.objects.filter(session=session,payment_type=2,type=1).aggregate(Sum('total_amt'))
    # total_purchase_by_bank=total_purchase_by_bank['total_amt__sum']
    # total_expense_by_bank = Invoice.objects.filter(session=session,payment_type=2,type=3).aggregate(Sum('total_amt'))
    # total_expense_by_bank=total_expense_by_bank['total_amt__sum']
    # total_sale = Invoice.objects.filter(session=session,type=2).aggregate(Sum('total_amt'))
    # total_sale=total_sale['total_amt__sum']
    # total_purchase = Invoice.objects.filter(session=session,type=1).aggregate(Sum('total_amt'))
    # total_purchase=total_purchase['total_amt__sum']
    # total_expense = Invoice.objects.filter(session=session,type=3).aggregate(Sum('total_amt'))
    # total_expense=total_expense['total_amt__sum']
    # print("total invoice sum",total_transactions)
    # print("total cash sales",total_sale_by_cash)
    # print("total cash Purchase",total_purchase_by_cash)
    # print("total cash expense",total_expense_by_cash)
    # print("total bank sales",total_sale_by_bank)
    # print("total bank Purchase",total_purchase_by_bank)
    # print("total bank expense",total_expense_by_bank)
    # cashmaster=CashMaster.objects.filter(branches=session.branches)
    # print("cashmaster",cashmaster[0])
    # cash_master=cashmaster[0].balance
    # print("current blance in cash for the branch",cash_master)
    # bankmaster=BankAccountMaster.objects.filter(branches=session.branches)
    # print("cashmaster",bankmaster[0])
    # bank_master_balance=bankmaster[0].balance
    # print("current blance in bank for the branch",bank_master_balance)
    # session_update=DailySession.objects.filter(pk=session.id).update(closing_balance_cash=cash_master,
    # closing_balance_bank=bank_master_balance,
    # total_transactions=total_transactions,
    # total_sales=total_sale,
    # total_purchase=total_purchase,
    # total_expense=total_expense,
    # total_cash_sales=total_sale_by_cash,
    # total_cash_purchase=total_purchase_by_cash,
    # total_bank_purchase=total_purchase_by_bank,
    # total_bank_sales=total_sale_by_bank,
    # ) 
    # print("session update",session_update) 
    # if session_update ==1:
    #     cash_accounts = Invoice.objects.values('cash_id').filter(session=session.id,cash__isnull=False).distinct()
    #     cash_ac_id=cash_accounts[0]['cash_id']            
    #     print('session updated suscessfully')    
    #     total_sale_cash = Invoice.objects.filter(session=session.id,payment_type=1,type=2,cash=cash_ac_id).aggregate(Sum('total_amt'))
    #     total_sale_by_cash=float(total_sale_cash['total_amt__sum'])
    #     total_purchase_cash= Invoice.objects.filter(session=session.id,payment_type=1,type=1,cash=cash_ac_id).aggregate(Sum('total_amt'))
    #     total_purchase_by_cash=total_purchase_cash['total_amt__sum']
    #     total_expense_cash = Invoice.objects.filter(session=session.id,payment_type=1,type=3,cash=cash_ac_id).aggregate(Sum('total_amt'))
    #     total_expense_by_cash=total_expense_cash['total_amt__sum']
    #     total_transactions_by_cash = Invoice.objects.filter(session=session.id,cash=cash_ac_id,payment_type=1,).aggregate(Sum('total_amt'))
    #     total_transactions=total_transactions_by_cash['total_amt__sum']
    #     total_credit = Invoice.objects.filter(session=session.id,cash=cash_ac_id,payment_type=1,type=1).aggregate(Sum('balance_amt'))
    #     total_credit_by_cash=total_credit['balance_amt__sum']
    #     total_debit = Invoice.objects.filter(session=session.id,cash=cash_ac_id,payment_type=1,type=2).aggregate(Sum('balance_amt'))
    #     total_debitt_by_cash=total_debit['balance_amt__sum']
    #     #cash ledger creation
    #     try:
    #         ledger = AccountLedger(
    #                 branches=cashmaster[0].branches,
    #                 session=DailySession.objects.get(id=session.id),
    #                 debit_balance=total_debitt_by_cash,
    #                 credit_balance=total_credit_by_cash,
    #                 balance=cashmaster[0].balance,
    #                 company=cashmaster[0].company,
    #                 cash=cashmaster[0],
    #                 total_transactions=total_transactions,                            
    #                 total_sales=total_sale_by_cash,
    #                 total_purchase=total_purchase_by_cash,
    #                 total_expense=total_expense_by_cash,
    #             )
    #         ledger.save()
    #         print("cash ledger created",ledger)
    #     except Exception as e:
    #         print(e)
    #     accounts = Invoice.objects.values('bank_id').filter(session=session.id,bank__isnull=False).distinct()
    #     print('affected bank accounts',accounts)
    #     for account in accounts:
    #         if account!=None:
    #             print("inner if condition working")
    #             print (account['bank_id'])
    #             bank_account_id=account['bank_id']
    #             bank=BankAccountMaster.objects.get(id=bank_account_id)
    #             total_sale_account = Invoice.objects.filter(session=session.id,payment_type=2,type=2,bank=bank_account_id).aggregate(Sum('total_amt'))
    #             total_sale_by_account=float(total_sale_account['total_amt__sum'])
    #             total_purchase_account= Invoice.objects.filter(session=session.id,payment_type=2,type=1,bank=bank_account_id).aggregate(Sum('total_amt'))
    #             total_purchase_by_account=total_purchase_account['total_amt__sum']
    #             total_expense_account = Invoice.objects.filter(session=session.id,payment_type=2,type=3,bank=bank_account_id).aggregate(Sum('total_amt'))
    #             total_expense_by_account=total_expense_account['total_amt__sum']
    #             total_transactions_by_account = Invoice.objects.filter(session=session.id,bank=bank_account_id,payment_type=2,).aggregate(Sum('total_amt'))
    #             total_transactions=total_transactions_by_account['total_amt__sum']
    #             total_credit = Invoice.objects.filter(session=session.id,bank=bank_account_id,payment_type=2,type=1).aggregate(Sum('balance_amt'))
    #             total_credit_by_bank=total_credit['balance_amt__sum']
    #             total_debit = Invoice.objects.filter(session=session.id,bank=bank_account_id,payment_type=2,type=2).aggregate(Sum('balance_amt'))
    #             total_debitt_by_bank=total_debit['balance_amt__sum']
    #             # print("bank",bank)
    #             try:
    #                 ledger = AccountLedger(
    #                     branches=bank.branches,
    #                     session=DailySession.objects.get(id=session.id),
    #                     debit_balance=total_debitt_by_bank,
    #                     credit_balance=total_credit_by_bank,
    #                     balance=bank.balance,                    
    #                     company=bank.company,
    #                     bank=bank,
    #                     total_transactions=total_transactions,                            
    #                     total_sales=total_sale_by_account,
    #                     total_purchase=total_purchase_by_account,
    #                     total_expense=total_expense_by_account,
    #                 )
    #                 ledger.save()      
    #                 print("bank ledger created",ledger)
    #             except Exception as e:
    #                 print(e)
    #         else:
    #             pass
    # # session_update=DailySession.objects.filter(pk=session.id).update(status=1)
    # self.instance = session_update
    # return self.instance
