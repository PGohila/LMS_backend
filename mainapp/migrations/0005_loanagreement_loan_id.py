# Generated by Django 4.2.7 on 2024-09-29 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_rename_loan_term_loan_tenure_remove_loan_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanagreement',
            name='loan_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_company', to='mainapp.loan'),
            preserve_default=False,
        ),
    ]
