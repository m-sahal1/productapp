from django.db.models.signals import post_save
from django.dispatch import receiver
from base.tasks import send_emails_everyone
from base.models import Product

@receiver(post_save, sender=Product)
def run_task1_when_product_added(sender, instance, created, **kwargs):
    if created:
        subject= "New Product Added"
        message= f"{instance.title}\n{instance.description}"
        # This code will run when a new product is created
        send_emails_everyone.delay(subject,message,None)