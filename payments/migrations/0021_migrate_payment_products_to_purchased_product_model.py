# Generated by Django 5.1.2 on 2024-10-23 03:07

from django.db import migrations, transaction, connection
from datetime import datetime

def forwards(apps, schema_editor):
  Payment = apps.get_model('payments', 'Payment')
  PurchasedProduct = apps.get_model('payments', 'PurchasedProduct')
  
  now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

  payment_table_backup_table_name = f"payments_payment_backup_{now}"
  print(f"creating backup table {payment_table_backup_table_name} as copy of payments_payment")
  
  cur = connection.cursor()
  cur.execute(f"CREATE TABLE {payment_table_backup_table_name} AS TABLE payments_payment")
  
  payments = Payment.objects.filter(product__isnull=False)
  for payment in payments:
    print(f"migrating payment {payment.id}")
    with transaction.atomic():
      pp = PurchasedProduct.objects.create(payment=payment, product=payment.product, quantity=1)
      print(f"created PurchasedProduct {pp.id} for Payment {payment.id} with product {payment.product.id}")
      payment.product = None
      print (f"setting payment {payment.id} product to null")
      payment.save()
      print(f"saved payment {payment.id}")
      
  
  # raises an AssertionError if there are any payments with a product (meaning the migration didn't fully work). 
  # if weird things happen, this migration should be safe to run multiple times until it works. 
  # worst case, you should always have the backup table to rollback to. (but we should really have a full
  # db backup in case things go severely wrong)
  assert Payment.objects.filter(product__isnull=False).count() == 0


def backwards(apps, schema_editor, connection):
    # shouldn't be that bad, just need to manually revert payments_payment table to state of the backup table. but this is funny to see so I'm leaving it
    raise Exception("lol gl homie")

class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0020_alter_purchasedproduct_product'),
    ]

    operations = [
      migrations.RunPython(forwards),
    ]
