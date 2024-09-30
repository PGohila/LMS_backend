from django.db import models
from django.contrib.auth.models import User

# MS setup models
class MSRegistration(models.Model):
    mservice_id = models.CharField(max_length=20,primary_key=True)
    mservice_name = models.CharField(max_length=100)
    arguments = models.JSONField(null=True,blank=True)
    arguments_list = models.TextField(null=True,blank=True)
    required_parameter = models.TextField(null=True,blank=True)
    optional_parameter = models.TextField(null=True,blank=True)
    is_authenticate = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
	
    def formatted_mservice_name(self):
        # Replace underscores with spaces in mservice_name
        return self.mservice_name.replace('_', ' ')
    def __str__(self):
        return str(self.mservice_id)
    
class ModuleRegistration(models.Model):
    module_name = models.CharField(max_length=250,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return str(self.module_name)

class MsToModuleMapping(models.Model):
    mservice_id = models.OneToOneField(MSRegistration,on_delete=models.CASCADE,related_name='ms_id')
    module_id = models.ForeignKey(ModuleRegistration,on_delete=models.CASCADE,related_name='module_id')

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def str(self):
        return str(self.module_id)	
    
# ============= Masters =====================
class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class IdentificationType(models.Model):
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    type_name = models.CharField(max_length=100, unique=True) # passport, Adhar Card, License, Pan card
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BankAccount(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='%(class)s_company')
    account_number = models.CharField(max_length=50, unique=True)
    account_holder_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    nrfc_number = models.CharField(max_length=50, blank=True, null=True)  # Non-Resident Foreign Currency number
    swift_code = models.CharField(max_length=50, blank=True, null=True)
    ifsc_code = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_number}"

class Currency(models.Model):
	company = models.ForeignKey(Company,on_delete=models.CASCADE, related_name='%(class)s_company')
	code = models.CharField(max_length=3)
	name = models.CharField(max_length=50)
	symbol = models.CharField(max_length=5, blank=True, null=True)
	exchange_rate = models.DecimalField(max_digits=10, decimal_places=4,)
	is_active = models.BooleanField(default=False,)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class PaymentMethod(models.Model):
	company = models.ForeignKey(Company,on_delete=models.CASCADE, related_name='%(class)s_company')
	method_name = models.CharField(max_length=50) # Bank Transfer,Credit/Debit Card,Cash,Mobile Payment Solutions(mobile apps),Checks
	description = models.TextField( blank=True,null=True)
	is_active = models.BooleanField(default=False,)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)   

class   LoanType(models.Model):
	company = models.ForeignKey(Company,on_delete=models.CASCADE, related_name='%(class)s_company')
	loantype_id = models.CharField(max_length=50,unique = True)
	loantype = models.CharField(max_length=100) # personal loan, housing loan
	description = models.TextField(blank = True,null =True)
	interest_rate = models.FloatField(default = 0.0) # percentage
	loan_teams = models.IntegerField() # Standard loan term duration for this type, in months.
	min_loan_amt = models.FloatField(default = 0.0)
	max_loan_amt = models.FloatField(default = 0.0)
	eligibility = models.TextField() # Conditions a borrower must meet to qualify for this loan with customer income.
	collateral_required = models.BooleanField(default=False)
	charges = models.TextField() # Any associated fees like processing or administration fees.
	is_active = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True) 


# Collateral Type Master Table
class CollateralType(models.Model):
	company = models.ForeignKey(Company,on_delete=models.CASCADE, related_name='%(class)s_company')
	name = models.CharField(max_length=100) # Real Estate, vehicle, saving account
	description = models.TextField(blank=True, null=True)
	category = models.CharField(max_length=50,choices= [
		('Tangible','Tangible'), # tangible is physical asset like own property or own bike etc
		('Intangible','Intangible'), # intangible is non-physical assets like parents, trademarks
		('Financial','Financial'), # financial assets like stocks, bonds, and certificates
	])
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

#================== Processing =====================


class Customer(models.Model):
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=20,unique=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    dateofbirth = models.DateField()
    customer_income = models.FloatField(default = 0.0) # monthly income
    identification_type = models.ForeignKey(IdentificationType,on_delete=models.CASCADE)
    identification_number = models.CharField(max_length=50,blank=True,null=True)
    credit_score = models.IntegerField(default=0)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
     
    def __str__(self):
        return self.customer_id

class CustomerDocuments(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE, related_name='%(class)s_company')
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE, related_name='%(class)s_customers')
    documentid = models.CharField(max_length=20,unique=True)
    document_type = models.ForeignKey(IdentificationType,on_delete=models.CASCADE, related_name='%(class)s_document_type')
    documentfile = models.FileField(upload_to='documents/' ,blank=True,null=True )
    uploaded_at = models.DateField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    verified_by = models.CharField(max_length=50,blank=True,null=True)
    verified_at = models.DateField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class LoanCalculators(models.Model):
	loan_amount = 	models.FloatField(default = 0.0) # principal amount
	interest_rate = models.FloatField(default = 0.0) # 
	tenure = models.IntegerField(help_text="Tenure in days/weeks/months/years depending on the schedule.") # number of month
	tenure_type = models.CharField(max_length=100,choices=[
		('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
        ('years', 'Years')])
	repayment_schedule = models.CharField(max_length=100,choices=[('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('halfyearly', 'Half Yearly'),
        ('annually', 'Annually'),
        ('one_time', 'One Time'),]) # 
	repayment_mode = models.CharField(max_length=100,choices=[
        ('principal_only', 'Principal Only'),
        ('interest_only', 'Interest Only'),
        ('both', 'Principal and Interest'),
        ('interest_first', 'Interest First, Principal Later'),
        ('principal_end', 'Principal at End, Interest Periodically'),
    ])
	interest_basics = models.CharField(max_length=100,choices=[
        ('365', '365 Days Basis'),
        ('other', 'Other Basis'),
    ])
	loan_calculation_method = models.CharField(max_length=150,choices=[
        ('reducing_balance', 'Reducing Balance Method'),
        ('flat_rate', 'Flat Rate Method'),
        ('constant_repayment', 'Constant Repayment (Amortization)'),
        ('simple_interest', 'Simple Interest'),
        ('compound_interest', 'Compound Interest'),
        ('graduated_repayment', 'Graduated Repayment'),
        ('balloon_payment', 'Balloon Payment'),
        ('bullet_repayment', 'Bullet Repayment'),
        ('interest_first', 'Interest-Only Loans'),
    ])
	repayment_start_date = models.DateField()
	created_at = models.DateField(auto_now=True)
	updated_at = models.DateField(auto_now=True)

class LoanApplication(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE, related_name='%(class)s_company')
    application_id = models.CharField(max_length=20,unique=True)
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    loantype = models.ForeignKey(LoanType,on_delete=models.CASCADE, related_name='%(class)s_loantype')
    loan_amount = models.FloatField(default=0.0) # requested amount
    loan_purpose = models.TextField()
    application_status = models.CharField(max_length=20,choices=[
        ('Submitted', 'Submitted'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
        ]) 
    interest_rate = models.FloatField(default=0.0)
    tenure_type = models.CharField(max_length=100,choices=[
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
        ('years', 'Years')])
    tenure = models.IntegerField(help_text="Duration of the loan in months") # Duration of the loan in months
    repayment_schedule = models.CharField(max_length=100,choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('halfyearly', 'Half Yearly'),
        ('annually', 'Annually'),
        ('one_time', 'One Time')])
    repayment_mode = models.CharField(max_length=100,choices=[
        ('principal_only', 'Principal Only'),
        ('interest_only', 'Interest Only'),
        ('both', 'Principal and Interest'),
        ('interest_first', 'Interest First, Principal Later'),
        ('principal_end', 'Principal at End, Interest Periodically'),
    ])
    interest_basics = models.CharField(max_length=100,choices=[
        ('365', '365 Days Basis'),
        ('other', 'Other Basis'),
    ])
    loan_calculation_method = models.CharField(max_length=150,choices=[
        ('reducing_balance', 'Reducing Balance Method'),
        ('flat_rate', 'Flat Rate Method'),
        ('constant_repayment', 'Constant Repayment (Amortization)'),
        ('simple_interest', 'Simple Interest'),
        ('compound_interest', 'Compound Interest'),
        ('graduated_repayment', 'Graduated Repayment'),
        ('balloon_payment', 'Balloon Payment'),
        ('bullet_repayment', 'Bullet Repayment'),
        ('interest_first', 'Interest-Only Loans'),
    ])
    repayment_start_date = models.DateField()
    applied_at = models.DateField(auto_now=True) # application date
    approved_at = models.DateField(blank=True,null=True)
    rejected_reason = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True, null=True)
    workflow_stats = models.CharField(max_length=50,choices=[
        ('Submitted', 'Submitted'),
        ('Approved', 'Approved'),
        ('Borrower_Approved','Borrower Approved'), # loan agreement screen
        ('Lender_Approved','Lender Approved'),
        ('Borrower_and_Lender_Approved', 'Borrower and Lender Approved'),
        ('Borrower_Rejected', 'Borrower Rejected'),
        ('Disbursment', 'Disbursment'),
        ('Processing', 'Processing'),
        ('Loan Closed', 'Loan Closed'),
        ])
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Loan(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE, related_name='%(class)s_company')
    loanapp_id = models.ForeignKey(LoanApplication,on_delete=models.CASCADE, related_name='%(class)s_loanapp')
    loan_id = models.CharField(max_length=20, unique=True)
    loan_amount = models.FloatField(default = 0.0)
    interest_rate = models.FloatField(default = 0.0)
    disbursement_amount = models.FloatField(default = 0.0) # toatal disbursement amount
    tenure = models.IntegerField()  # In months
    loan_purpose = models.TextField()
    paid_amount = models.FloatField(default = 0.0)
    borrower = models.ForeignKey(Customer,on_delete=models.CASCADE)
    lender = models.ForeignKey(User, related_name='lender', on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')], default='pending') # loan agreement status
    workflow_stats = models.CharField(max_length=50,choices=[
        ('Submitted', 'Submitted'),
        ('Approved', 'Approved'),
        ('Borrower_Approved','Borrower Approved'), # loan agreement screen
        ('Lender_Approved','Lender Approved'),
        ('Borrower_and_Lender_Approved', 'Borrower and Lender Approved'),
        ('Borrower_Rejected', 'Borrower Rejected'),
        ('Disbursment', 'Disbursment'),
        ('Processing', 'Processing'),
        ('Loan Closed', 'Loan Closed'),
        ])

    def __str__(self):
        return f"Loan {self.loan_id}"

class LoanAgreement(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='%(class)s_company')
    agreement_id = models.CharField(max_length=20)
    loan_id = models.ForeignKey(Loan,on_delete=models.CASCADE, related_name='%(class)s_company')
    loanapp_id = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='%(class)s_loan_id')
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='%(class)s_customer_id')
    agreement_terms = models.TextField( blank=True,null=True)
    agreement_date = models.DateTimeField(auto_now_add=True)
    borrower_signature = models.FileField(upload_to='signatures/borrowers/',blank=True,null=True)
    lender_signature = models.FileField(upload_to='signatures/lenders/',blank=True,null=True)
    signed_at = models.DateTimeField(blank=True,null=True)
    agreement_status = models.CharField(max_length=70,choices = [
        ('Active', 'Active'),
        ('Terminated', 'Terminated'),
        ('Completed', 'Completed'),
    ]) 
    maturity_date = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Disbursement(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='%(class)s_company')
    disbursement_id = models.CharField(max_length=50,unique=True)
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE, related_name='%(class)s_customer_id')
    loan = models.ForeignKey(Loan,on_delete=models.CASCADE, related_name='%(class)s_loan')
    loan_application = models.ForeignKey(LoanApplication,on_delete=models.CASCADE, related_name='%(class)s_loan_application')
    disbursement_date = models.DateField(auto_now=True)
    amount = models.FloatField(default=0.0)
    disbursement_type = models.CharField(max_length=50,choices=[
        ('Initial', 'Initial'),
        ('Partial', 'Partial'),
        ('Final', 'Final'),
    ])
    disbursement_status = models.CharField(max_length=50,choices=[
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
    ])
    disbursement_method = models.CharField(max_length=50, choices=[
        ('direct_deposit', 'Direct Deposit'),
        ('check', 'Check'),
        ('cash', 'Cash'),
        ('prepaid_card','Prepaid Card'),
        ('Third-Party','Third-Party')
    ])
    bank = models.ForeignKey(BankAccount,on_delete=models.CASCADE,blank=True,null=True)
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE)
    notes = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RepaymentSchedule(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE, related_name='%(class)s_company')
    loan_application = models.ForeignKey(LoanApplication,on_delete=models.CASCADE,related_name='%(class)s_loan_application')
    period = models.IntegerField(default=0)
    schedule_id = models.CharField(max_length=50,unique=True)
    repayment_date = models.DateField()
    instalment_amount = models.FloatField(default = 0.0)
    paid_amount = models.FloatField(default = 0.0)
    principal_amount = models.FloatField(default = 0.0)
    interest_amount = models.FloatField(default = 0.0)
    remaining_balance = models.FloatField(default = 0.0)
    repayment_status = models.CharField(max_length = 50,choices = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    ],default="Pending")
    payment_method = models.ForeignKey(PaymentMethod,on_delete=models.CASCADE,related_name='%(class)s_payment_method',blank=True,null=True)
    transaction_id = models.CharField(max_length=50,blank=True,null=True)
    notes = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Payments(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=50,unique=True)
    loan_id = models.ForeignKey(Loan,on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    payment_date = models.DateField(auto_now=True)
    payment_method = models.ForeignKey(PaymentMethod,on_delete=models.CASCADE)
    transaction_refference = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Penalties(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='%(class)s_company')
    penalty_id = models.CharField(max_length=50,unique=True)
    loan_application = models.ForeignKey(LoanApplication,on_delete=models.CASCADE,related_name='%(class)s_loan_application')
    repaymentschedule_id = models.ForeignKey(RepaymentSchedule,on_delete=models.CASCADE,related_name='%(class)s_repaymentschedule_id')
    panalty_date = models.DateField(auto_now=True)
    penalty_amount = models.FloatField(default=0.0)
    penalty_reason = models.CharField(max_length=50,choices = [
        ('Late Payment', 'Late Payment'),
        ('Missed Payment', 'Missed Payment'),
    ])
    payment_status = models.CharField(max_length=50,choices = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    ])
    transaction_refference = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LoanClosure(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    closure_id = models.CharField(max_length=50,unique=True)
    loanapp_id = models.ForeignKey(LoanApplication,on_delete=models.CASCADE)
    closure_date = models.DateField()
    closure_amount = models.FloatField(default=0.0)
    remaining_balance = models.FloatField(default=0.0)
    closure_method = models.CharField(max_length=50,choices = [
        ('lump sum Payment', 'lump sum Payment'),
        ('Refinancing', 'Refinancing'),
    ])
    closure_reason = models.TextField()
    transaction_refference = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    
class Collaterals(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    collateral_id = models.CharField(max_length=20,unique=True)
    loanapp_id = models.ForeignKey(LoanApplication,on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    collateral_type = models.ForeignKey(CollateralType,on_delete=models.CASCADE)
    collateral_value = models.FloatField(default = 0.0,help_text="Monetary value of the collateral") 
    valuation_date = models.DateField()
    valuation_report = models.FileField(upload_to='valuation_reports/', blank=True, null=True, help_text="Upload the valuation report document.")
    collateral_status = models.CharField(max_length=50,choices=[
        ('Held', 'Held'),
        ('Released', 'Released'),
        ('Sold', 'Sold'),
    ])
    insurance_status = models.CharField(max_length=50,choices=[
        ('Insured', 'Insured'),
        ('Not insured', 'Not insured'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#===========================================

class Creditscores(models.Model):
	company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='%(class)s_company')
	scores_id = models.CharField(max_length=20)
	customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='%(class)s_customer_id')
	credit_score = models.IntegerField(blank=True,null=True) # A credit score is a three-digit number that typically ranges from 300 to 850.
	retrieved_at = models.DateField(blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class LoanOffer(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    offer_id = models.CharField(max_length=20,unique=True)
    application_id = models.ForeignKey(LoanApplication,on_delete=models.CASCADE)
    loanamount = models.FloatField(default=0.0)
    interest_rate = models.FloatField(default = 0.0)
    tenure = models.IntegerField(help_text="Duration of the loan in months")
    monthly_instalment = models.FloatField(default = 0.0)
    terms_condition = models.TextField(null=True, blank=True)
    offer_status = models.CharField(max_length=50,choices=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class SupportTickets(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    ticket_id = models.CharField(max_length=50,unique=True)
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    subject = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=50,choices= [
        ('Open', 'Open'),
        ('In-progress', 'In-progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ])
    priority = models.CharField(max_length=50,choices= [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ])
    assigned_to = models.CharField(max_length=50,blank=True,null=True)
    resolution = models.CharField(max_length=50)
    resolution_date = models.DateField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CustomerFeedBack(models.Model):
    feedback_id = models.CharField(max_length=50,unique=True)
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    feedback_date = models.DateField(blank=True,null=True)
    feedback_type = models.CharField(max_length=50,choices=  [
        ('Complaint', 'Complaint'),
        ('Suggestion', 'Suggestion'),
        ('Compliment', 'Compliment'),
    ])
    subject = models.CharField(max_length=50)
    description = models.TextField(blank=True,null=True)
    feedback_status = models.CharField(max_length=50)


class Notifications(models.Model):
	company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='%(class)s_company')
	notification_id = models.CharField(max_length=20)
	customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='%(class)s_customer_id')
	message = models.TextField()
	status = models.CharField(max_length=20)
	priority = models.CharField(max_length=20)





