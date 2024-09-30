# Generated by Django 4.2.7 on 2024-09-29 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_disbursement_bank_disbursement_disbursement_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='workflow_stats',
            field=models.CharField(choices=[('Submitted', 'Submitted'), ('Approved', 'Approved'), ('Borrower Approved', 'Borrower Approved'), ('Borrower Rejected', 'Borrower Rejected'), ('Disbursment', 'Disbursment'), ('Processing', 'Processing'), ('Loan Closed', 'Loan Closed')], default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loanapplication',
            name='workflow_stats',
            field=models.CharField(choices=[('Submitted', 'Submitted'), ('Approved', 'Approved'), ('Borrower Approved', 'Borrower Approved'), ('Borrower Rejected', 'Borrower Rejected'), ('Disbursment', 'Disbursment'), ('Processing', 'Processing'), ('Loan Closed', 'Loan Closed')], default=1, max_length=50),
            preserve_default=False,
        ),
    ]
