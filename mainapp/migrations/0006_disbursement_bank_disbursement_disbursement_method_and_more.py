# Generated by Django 4.2.7 on 2024-09-29 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_loanagreement_loan_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='disbursement',
            name='bank',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mainapp.bankaccount'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='disbursement',
            name='disbursement_method',
            field=models.CharField(choices=[('direct_deposit', 'Direct Deposit'), ('check', 'Check'), ('cash', 'Cash'), ('prepaid_card', 'Prepaid Card'), ('Third-Party', 'Third-Party')], default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='disbursement',
            name='loan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_loan', to='mainapp.loan'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='loanagreement',
            name='borrower_signature',
            field=models.FileField(blank=True, null=True, upload_to='signatures/borrowers/'),
        ),
        migrations.AlterField(
            model_name='loanagreement',
            name='lender_signature',
            field=models.FileField(blank=True, null=True, upload_to='signatures/lenders/'),
        ),
        migrations.DeleteModel(
            name='Disbursementmethod',
        ),
    ]
