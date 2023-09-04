from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from base.models import Product, Variant, Category

@shared_task
def send_email_all(subject, message, from_email):
    try:
        recipient_emails = User.objects.all().values_list('email', flat = True)
        send_mail(subject, message, from_email, recipient_emails)
        return True  # Email sent successfully
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        print(f"Email sending failed: {str(e)}")
        return False  # Email sending failed
    
# Send mails daily to staff users with statuses
    # Count of products
    # Count of variants
    # Count of products belonging to each category
    # Number of customers
@shared_task
def send_email_updates_to_staff(subject,  from_email):
    try:
        prod_count= Product.objects.all().count()
        variant_count = Variant.objects.all().count()
        cust_count = User.objects.filter(is_staff = False).count()

        categories = Category.objects.all().prefetch_related('product_set')
        cat_wise_prod_count = "Category Name: \n"
        for cat in categories:
            cat_wise_prod_count += f"{cat.title}: {cat.product_set.all().count()}\n"
        
        message = f'''
        Count of products: {prod_count}\n
        Count of variants: {variant_count}\n
        Count of products belonging to each category: {cat_wise_prod_count}\n
        Number of customers: {cust_count}\n
        '''
        recipient_emails = User.objects.filter(is_staff = True).values_list('email', flat = True)
        send_mail(subject, message, from_email, recipient_emails)
        return True  # Email sent successfully
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        print(f"Email sending failed: {str(e)}")
        return False  # Email sending failed