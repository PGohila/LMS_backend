# Generated by Django 4.2.7 on 2024-09-29 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_loan_workflow_stats_loanapplication_workflow_stats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='workflow_stats',
            field=models.CharField(choices=[('Submitted', 'Submitted'), ('Approved', 'Approved'), ('Borrower_Approved', 'Borrower Approved'), ('Lender_Approved', 'Lender Approved'), ('Borrower_and_Lender_Approved', 'Borrower and Lender Approved'), ('Borrower_Rejected', 'Borrower Rejected'), ('Disbursment', 'Disbursment'), ('Processing', 'Processing'), ('Loan Closed', 'Loan Closed')], max_length=50),
        ),
        migrations.AlterField(
            model_name='loanapplication',
            name='workflow_stats',
            field=models.CharField(choices=[('Submitted', 'Submitted'), ('Approved', 'Approved'), ('Borrower_Approved', 'Borrower Approved'), ('Lender_Approved', 'Lender Approved'), ('Borrower_and_Lender_Approved', 'Borrower and Lender Approved'), ('Borrower_Rejected', 'Borrower Rejected'), ('Disbursment', 'Disbursment'), ('Processing', 'Processing'), ('Loan Closed', 'Loan Closed')], max_length=50),
        ),
    ]
