from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from datetime import datetime, date, timedelta
from .models import advancepayment, paydowncreditcard, salesrecpts, timeact, timeactsale, Cheqs, suplrcredit, addac, \
    bills, invoice, expences, payment, credit, delayedcharge, estimate, service, noninventory, bundle, employee, \
    payslip, inventory, customer, supplier, company, accounts, ProductModel, ItemModel, accountype, \
    expenseaccount, incomeaccount, accounts1, recon1, recordpay, addtax1, bankstatement, customize
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
import json
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
import itertools


def index(request):
    return render(request, 'app1/index.html')


def go(request):
    return render(request, 'app1/login.html')


def create(request):
    try:
        if request.method == 'POST':
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            conformpassword = request.POST['conformpassword']
            if password == conformpassword:
                if User.objects.filter(username=username).exists():
                    messages.info(
                        request, 'This username already exists. Sign up again')
                    return render(request, 'app1/login.html')
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email,
                                                    username=username, password=password)
                    user.save()
                    return render(request, 'app1/company.html', {'member': user})
            else:
                return redirect('')
        else:
            return redirect('')
    except:
        return redirect('')


def regcomp(request):
    return render(request, 'app1/login.html')

def register(request, id):
    try:
        if request.method == 'POST':
            cname = request.POST.get('cname')
            caddress = request.POST.get('caddress')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pincode = request.POST.get('pincode')
            cemail = request.POST.get('cemail')
            phone = request.POST.get('phone')
            try:
                img1 = request.FILES['img1']
            except:
                img1 = 'default'
            bname = request.POST.get('bname')
            industry = request.POST.get('industry')
            ctype = request.POST.get('ctype')
            abt = request.POST.get('abt')
            paid = request.POST.get('paid')
            new_id = User.objects.get(id=id)
            companys = company(id=new_id, cname=cname, caddress=caddress, city=city, state=state, pincode=pincode,
                               cemail=cemail,
                               phone=phone, bname=bname, industry=industry, ctype=ctype, abt=abt, paid=paid)
            if img1 != 'default':
                companys.cimg = img1
            companys.save()
            toda = date.today()
            tod = toda.strftime("%Y-%m-%d")
            comp = company.objects.get(id=new_id)
            accountsecond = [
                ['Account Receivable(Debtors)', 'Account Receivable(Debtors)',
                 'Account Receivable(Debtors)'],
                ['Current Assets', 'Deferred Service Tax Input Credit', 'Deferred CGST'],
                ['Current Assets', 'Deferred Service Tax Input Credit',
                    'Deferred GST Input Credit'],
                ['Current Assets', 'Deferred Service Tax Input Credit', 'Deferred IGST'],
                ['Current Assets', 'Deferred Service Tax Input Credit',
                    'Deferred Krishi Kalyan Cess Input Credit'],
                ['Current Assets', 'Prepaid Expenses', 'Prepaid Expenses'],
                ['Current Assets', 'Deferred Service Tax Input Credit',
                    'Deferred Service Tax Input Credit'],
                ['Current Assets', 'Deferred Service Tax Input Credit', 'Deferred SGST'],
                ['Current Assets', 'Deferred Service Tax Input Credit',
                    'Deferred VAT Input Credit'],
                ['Current Assets', 'Service Tax Refund', 'GST Refund'],
                ['Current Assets', 'Inventory', 'Inventory Asset'],
                ['Current Assets', 'Service Tax Refund',
                    'Krishi Kalyan Cess Refund'],
                ['Current Assets', 'Prepaid Expenses', 'Prepaid Insurance'],
                ['Current Assets', 'Service Tax Refund', 'Service Tax Refund'],
                ['Current Assets', 'Other Current Assets', 'TDS Receivable'],
                ['Current Assets', 'Other Current Assets', 'Uncategorised Asset'],
                ['Current Assets', 'Undeposited Fund', 'Undeposited Fund'],
                ['Fixed Assets', 'Accumulated Depreciation',
                    'Accumulated Depreciation'],
                ['Fixed Assets', 'Buildings', 'Buildings and Improvements'],
                ['Fixed Assets', 'Furniture and fixtures', 'Furniture and Equipment'], [
                    'Fixed Assets', 'Land', 'Land'],
                ['Fixed Assets', 'Leasehold Improvements', 'Leasehold Improvements'],
                ['Fixed Assets', 'Vehicles', 'Vehicles'],
                ['Accounts Payable(Creditors)', 'Accounts Payable(Creditors)',
                 'Accounts Payable(Creditors)'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'CGST Payable'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'CST Payable'],
                ['Current Liabilities', 'Tax Suspense', 'CST Suspense'],
                ['Current Liabilities', 'Sales And Service Tax Payable', 'GST Payable'],
                ['Current Liabilities', 'Tax Suspense', 'GST Suspense'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'IGST Payable'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'Input CGST'],
                ['Current Liabilities', 'Sales and Service Tax Payable',
                    'Input CGST Tax RCM'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'Input IGST'],
                ['Current Liabilities', 'Sales and Service Tax Payable',
                    'Input IGST Tax RCM'],
                ['Current Liabilities', 'Sales and Service Tax Payable',
                    'Input Krishi Kalyan Cess'],
                ['Current Liabilities', 'Sales and Service Tax Payable',
                    'Input Krishi Kalyan Cess RCM'],
                ['Current Liabilities', 'Sales and Service Tax Payable',
                    'Input Service Tax'],
                ['Current Liabilities', 'Sales and Service Tax Payable',
                    'Input Service Tax RCM'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'Input SGST'],
                ['Current Liabilities', 'Sales asnd Service Tax Payable',
                    'Input SGST Tax RCM'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'Input VAT 14%'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'Input VAT 4%'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'Input VAT 5%'],
                ['Current Liabilities', 'Sales and Service Tax Payable',
                    'Krishi Kalyan Cess Payable'],
                ['Current Liabilities', 'Tax Suspense',
                    'Krishi Kalyan Cess Suspense'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'Output CGST'],
                ['Current Liabilities', 'Sales and Service Tax Payable',
                    'Output CGST Tax RCM'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'Output CST 2%'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'Output IGST'],
                ['Current Liabilities', 'Sales and Service Tax Payable',
                    'Output IGST Tax RCM'],
                ['Current Liabilties', 'Sales and Service Tax Payable',
                    'Output Krishi Kaylan Cess'],
                ['Current Liabilities', 'Sales and Service Tax Payable',
                    'Output Krishi Kalyan Cess RCM'],
                ['Current Liabilties', 'Sales and Service Tax Payable',
                    'Output Service Tax'],
                ['Current Liabilities', 'Sales and Service Tax Payable',
                    'Output Service Tax RCM'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'Output SGST'],
                ['Current Liabilities', 'Sales and Service Tax Payable',
                    'Output SGST Tax RCM'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'Output VAT 14%'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'Output VAT 4%'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'Output VAT 5%'],
                ['Current Liabilties', 'Sales and Service Tax Payable',
                    'Service Tax Payable'],
                ['Current Liabilities', 'Tax Suspense', 'Service Tax Suspense'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'SGST Payable'],
                ['Current Liabilities', 'Sales and Service Tax Payable',
                    'Swachh Barath Cess Payable'],
                ['Current Liabilities', 'Tax Suspense',
                    'Swachh Barath Cess Suspense'],
                ['Current Liabilities', 'Current Liabilities', 'TDS Payable'],
                ['Current Liabilities', 'Sales and Service Tax Payable', 'VAT Payable'],
                ['Current Liabilities', 'Tax Suspense', 'VAT Suspense'],
                ['Equity', 'Opening Balance Equity', 'Opening Balance Equity'],
                ['Equity', 'Retained Earnings', 'Retained Earnings'],
                ['Income', 'Service/Fee Income', 'Billable Expense Income'],
                ['Income', 'Service/Fee Income', 'Consulting Income'],
                ['Income', 'Sales of Product Income', 'Product Sales'], [
                    'Income', 'Sales of Product Income', 'Sales'],
                ['Income', 'Sales of Product Income', 'Sales-Hardware'],
                ['Income', 'Sales of Product Income', 'Sales-Software'],
                ['Income', 'Sales of Product Income',
                    'Sales-Support and Maintanance'],
                ['Income', 'Discount/Refund Given', 'Sales Discounts'],
                ['Income', 'Sales of Product Income', 'Sales of Product Income'],
                ['Income', 'Service/Fee Income', 'Services'],
                ['Income', 'Unapplied Cash Payment Income',
                    'Unapplied Cash Payment Income'],
                ['Income', 'Service/Fee Income', 'Uncategorised Income'],
                ['Cost of Goods Sold', 'Suppliers and Materials-COS', 'Cost of Sales'],
                ['Cost of Goods Sold', 'Cost of Goods Sold',
                    'Equipment Rental for Jobs'],
                ['Cost of Goods Sold', 'Cost of Goods Sold',
                    'Freight and Shipping Cost'],
                ['Cost of Goods Sold', 'Suppliers and Materials-COS',
                    'Inventory Shrinkage'],
                ['Cost of Goods Sold', 'Cost of Goods Sold', 'Merchant Account Fees'],
                ['Cost of Goods Sold', 'Cost of Goods Sold',
                    'Purchases-Hardware for Resale'],
                ['Cost of Goods Sold', 'Cost of Goods Sold',
                    'Purchases-Software for Resale'],
                ['Cost of Goods Sold', 'Cost of Goods Sold',
                    'Subcontracted Services'],
                ['Cost of Goods Sold', 'Cost of Goods Sold',
                    'Tools and Craft Suppliers'],
                ['Expenses', 'Advertising/Promotional', 'Advertising/Promotional'],
                ['Expenses', 'Bank Charges', 'Bank Charges'],
                ['Expenses', 'Office/General Administrative Expenses',
                    'Business Licenses and Permitts'],
                ['Expenses', 'Charitable Contributions', 'Charitable Contributions'],
                ['Expenses', 'Office/General Administrative Expenses',
                    'Computer and Internet Expense'],
                ['Expenses', 'Office/General Administrative Expenses',
                    'Continuing Education'],
                ['Expenses', 'Office/General Administrative Expenses',
                    'Depreciation Expense'],
                ['Expenses', 'Dues and Subscriptions', 'Dues and Subscriptions'],
                ['Expenses', 'Office/General Administrative Expenses',
                    'Housekeeping Charges'],
                ['Expenses', 'Office/General Administrative Expenses',
                    'Insurance Expenses'],
                ['Expenses', 'Office/General Administrative Expenses',
                 'Insurance Expenses-General Liability Insurance'],
                ['Expenses', 'Office/General Administrative Expenses',
                    'Insurance Expenses-Health Insurance'],
                ['Expenses', 'Office/General Administrative Expenses',
                 'Insurance Expenses-Life and Disability Insurance'],
                ['Expenses', 'Office/General Administrative Expenses',
                    'Insurance Expenses-Professional Liability'],
                ['Expenses', 'Interest Paid', 'Interest Expenses'],
                ['Expenses', 'Meals and Entertainment', 'Meals and Entertainment'],
                ['Expenses', 'Office/General Administrative Expenses', 'Office Supplies'],
                ['Expenses', 'Office/General Administrative Expenses',
                    'Postage and Delivery'],
                ['Expenses', 'Office/General Administrative Expenses',
                    'Printing and Reproduction'],
                ['Expenses', 'Office/General Administrative Expenses',
                    'Professional Fees'],
                ['Expenses', 'Suppliers and Materials', 'Purchases'],
                ['Expenses', 'Office/General Administrative Expenses', 'Rent Expense'],
                ['Expenses', 'Office/General Administrative Expenses',
                    'Repair and Maintanance'],
                ['Expenses', 'Office/General Administrative Expenses',
                    'Small Tools and Equipments'],
                ['Expenses', 'Tax Expense', 'Swachh Barath Cess Expense'],
                ['Expense', 'Office/General Administrative Expenses', 'Taxes-Property'],
                ['Expenses', 'Office/General Administrative Expenses',
                    'Telephone Expense'],
                ['Expenses', 'Office/General Administrative Expenses', 'Travel Expense'],
                ['Expenses', 'Other Miscellaneous Service Cost',
                    'Uncategorised Expense'],
                ['Expenses', 'Utilities', 'Utilities'],
                ['Other Income', 'Other Miscellaneous Income',
                    'Finance Charge Income'],
                ['Other Income', 'Other Miscellaneous Income',
                    'Insurance Proceeds Received'],
                ['Other Income', 'Interest Earned', 'Interest Income'],
                ['Other Income', 'Other Miscellaneous Income',
                    'Proceeds From Sale of Assets'],
                ['Other Income', 'Other Miscellaneous Income',
                    'Shipping and Delivery Income'],
                ['Other Expenses', 'Other Expenses', 'Ask My Accountant'],
                ['Other Expenses', 'Other Expenses', 'CGST Write-Off'],
                ['Other Expense', 'Other Expense', 'GST Write-Off'],
                ['Other Expenses', 'Other Expenses', 'IGST Write-Off'],
                ['Other Expenses', 'Other Expenses', 'Miscellaneous Expense'],
                ['Other Expenses', 'Other Expenses', 'Political Contributions'],
                ['Other Expenses', 'Other Expenses',
                    'Reconciliation Discrepancies'],
                ['Other Expenses', 'Other Expenses', 'SGST Write-Off'],
                ['Other Expenses', 'Other Expenses', 'Tax Write-Off'],
                ['Other Expenses', 'Other Expenses', 'Vehicle Expenses']]

            accounype = [['Deferred CGST'], ['Deferred GST Input Credit'], ['Deferred IGST'],
                         ['Deferred Krishi Kalyan Cess Input Credit'],
                         ['Deferred Service Tax Input Credit'], [
                             'Deferred SGST'], ['Deferred VAT Input Credit'],
                         ['GST Refund'],
                         ['Inventory Asset'], ['Paid Insurance'], [
                             'Service Tax Refund'], ['TDS Receivable'],
                         ['Uncategorised Asset'],
                         ['Accumulated Depreciation'], ['Buildings and Improvements'], [
                             'Furniture and Equipments'],
                         ['Land'],
                         ['Leasehold Improvements'], ['Vehicles'], [
                             'CGST Payable'], ['CST Payable'], ['CST Suspense'],
                         ['GST Payable'],
                         ['GST Suspense'], ['IGST Payable'], ['Input CGST'], [
                             'Input CGST Tax RCM'], ['Input IGST'],
                         ['Input IGST Tax RCM'],
                         ['Input Krishi Kalyan Cess'], [
                             'Input Krishi Kalyan Cess RCM'], ['Input Service Tax'],
                         ['Input Service Tax RCM'],
                         ['Input SGST'], ['Input SGST Tax RCM'], [
                             'Input VAT 14 %'], ['Input VAT 4%'], ['Input VAT 5%'],
                         ['Krishi Kalyan Cess Payable'], [
                             'Krishi Kalyan Cess Suspense'], ['Output CGST'],
                         ['Output CGST Tax RCM'],
                         ['Output CST 2%'], ['Output IGST'], [
                             'Output IGST Tax RCM'], ['Output Krishi Kalyan Cess'],
                         ['Output Krishi Kalyan Cess RCM'], [
                             'Output Service Tax'], ['Output Service Tax RCM'],
                         ['Output SGST'],
                         ['Output SGST Tax RCM'], ['Output VAT 14%'], [
                             'Output VAT 4%'], ['Output VAT 5%'],
                         ['Service Tax Payable'],
                         ['Service Tax Suspense'], ['SGST Payable'], [
                             'SGST Suspense'], ['Swachh Barath Cess Payable'],
                         ['Swachh Barath Cess Suspense'], ['TDS Payable'], ['VAT Payable'], ['VAT Suspense']]
            for i in range(len(accountsecond)):
                for j in range(1):
                    accounts1model = accounts1(cid=comp, acctype=accountsecond[i][0],
                                               detype=accountsecond[i][1], name=accountsecond[i][2], description='',
                                               gst='', deftaxcode='', balance=0.0,
                                               asof=tod)
                    accounts1model.save()
            for i in range(len(accounype)):
                for j in range(1):
                    accoutype = accountype(
                        cid=comp, accountname=accounype[i][0])
                    accoutype.save()
            return redirect('regcomp')
        else:
            return redirect('regcomp')
    except:
        return redirect('regcomp')


def login(request):
    try:
        if request.method == 'POST':
            try:
                username = request.POST['username']
                password = request.POST['password']
                user = auth.authenticate(username=username, password=password)
                cmp1 = company.objects.get(id=user.id)
                request.session["uid"] = user.id
                if user is not None:
                    auth.login(request, user)
                    return redirect('/app1/godash')
                else:
                    messages.info(request, 'Invalid username or password')
                    return redirect('regcomp')
            except:
                messages.info(request, 'Invalid username or password')
                return render(request, 'app1/login.html')
        else:
            messages.info(request, 'Invalid username or password')
            return render(request, 'app1/login.html')
    except:
        messages.info(request, 'Invalid username or password')
        return render(request, 'app1/login.html')


@login_required(login_url='regcomp')
def godash(request):
    try:
        cmp1 = company.objects.get(id=request.session["uid"])
        request.session["invcol"] = " "
        request.session["noninvcol"] = " "
        request.session["buncol"] = " "
        context = {'cmp1': cmp1}
        return render(request, 'app1/dashbord.html', context)
    except:
        cmp1 = company.objects.get(id=request.session["uid"])
        request.session["invcol"] = " "
        request.session["noninvcol"] = " "
        request.session["buncol"] = " "
        context = {'cmp1': cmp1}
        return render(request, 'app1/dashbord.html', context)
        return redirect('/')


def logout(request):
    request.session["uid"] = ""
    auth.logout(request)
    return redirect('/')


@login_required(login_url='regcomp')
def userprofile(request, id):
    try:
        user1 = User.objects.get(id=id)
        cmp1 = company.objects.get(id=request.session["uid"])
        return render(request, 'app1/userprofile.html', {'users': user1, 'cmp1': cmp1})
    except:
        return redirect('godash')


@login_required(login_url='regcomp')
def edituserprofile(request):
    try:
        user1 = User.objects.get(id=request.session["uid"])
        cmp1 = company.objects.get(id=request.session["uid"])
        context = {'users': user1, 'cmp1': cmp1}
        return render(request, 'app1/edituserprofile.html', context)
    except:
        return redirect('godash')


@login_required(login_url='regcomp')
def updateuserprofile(request):
    try:
        user = User.objects.get(id=request.session["uid"])
        comp = company.objects.get(id=user.id)

        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]
        p1 = request.POST["newpassword"]
        p2 = request.POST["newpassword1"]

        comp.cname = request.POST["cname"]
        comp.caddress = request.POST["caddress"]
        comp.city = request.POST["city"]
        comp.state = request.POST["state"]
        comp.pincode = request.POST["pincode"]
        comp.cemail = request.POST["cemail"]
        comp.phone = request.POST["phone"]
        comp.bname = request.POST["bname"]
        comp.industry = request.POST["industry"]
        comp.ctype = request.POST["ctype"]
        try:
            img1 = request.FILES["img1"]
            comp.cimg = img1
        except:
            img2 = request.POST["img2"]
            comp.cimg = img2

        comp.save()
        user.save()

        if p1 == p2:
            if p1 != "":
                user.set_password(p1)
                user.save()
                logout(request)
                return redirect('/app1/go')
        elif p1 == "":
            return redirect('/app1/godash')

        return redirect('/app1/godash')
    except:
        return redirect('godash')


@login_required(login_url='regcomp')
def editsettings(request):
    return render(request, 'app1/editsettings.html')



@login_required(login_url='regcomp')
def cashposition(request):
    try:
        label_1 = []
        data_1 = []
        cmp1 = company.objects.get(id=request.session['uid'])
        cashpo = accounts.objects.filter(
            detype='Cash and Cash Equivalents', cid=cmp1)
        balance = accounts.objects.order_by('balance')[:10]
        for bala in balance:
            if bala.cid == cmp1:
                label_1.append(bala.name)
                data_1.append(bala.balance)
        context = {'cmp1': cmp1,
                   'cashpo': cashpo,
                   'label_1': label_1,
                   'data_1': data_1}
        return render(request, 'app1/cashposition.html', context)
    except:
        return redirect('godash')


@login_required(login_url='regcomp')
def editaccounts(request):
    try:
        user1 = User.objects.get(id=request.session["uid"])
        cmp1 = company.objects.get(id=request.session["uid"])
        context = {'users': user1, 'cmp1': cmp1}
        return render(request, 'app1/accountssettings.html', context)
    except:
        return redirect('godash')


@login_required(login_url='regcomp')
def updateaccounts(request):
    try:
        user = User.objects.get(id=request.session["uid"])
        comp = company.objects.get(id=user.id)

        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]
        p1 = request.POST["newpassword"]
        p2 = request.POST["newpassword1"]

        comp.cname = request.POST["cname"]
        comp.caddress = request.POST["caddress"]
        comp.city = request.POST["city"]
        comp.state = request.POST["state"]
        comp.pincode = request.POST["pincode"]
        comp.cemail = request.POST["cemail"]
        comp.phone = request.POST["phone"]
        comp.bname = request.POST["bname"]
        comp.industry = request.POST["industry"]
        comp.ctype = request.POST["ctype"]
        try:
            img1 = request.FILES["img1"]
            comp.cimg = img1
        except:
            img2 = request.POST["img2"]
            comp.cimg = img2

        comp.save()
        user.save()

        if p1 == p2:
            if p1 != "":
                user.set_password(p1)
                user.save()
                logout(request)
                return redirect('/app1/go')
        elif p1 == "":
            return redirect('/app1/godash')

        return redirect('/app1/godash')
    except:
        return redirect('godash')
