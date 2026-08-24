from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import requests

from .models import Book, WebHook

@receiver(post_save, sender=Book)
def notify_book_created(sender,instance,created, **kwargs):
    if not created:
        return  # only fire on creation, not every save/update

    # --- Listener 1: Email ---
    send_mail(
        subject=f'New Book was added: { instance.title}',
        message=f'"{instance.title}" by {instance.author.name} was just added to the library.',
        from_email='noreply@readingroom.local',
        recipient_list=['admin@readingroom.local'],  # placeholder for now
        fail_silently=False,
    )

    # --- Listener 2: Webhooks ---
    webhooks = WebHook.objects.filter(event='book.created', is_active=True)
    payload = {
        'event': 'book.created',
        'book' : {
            'id' : instance.id,
            'title' : instance.title,
            'author' : instance.author.name,
        }
    }

    for webhook in webhooks:
        try:
            requests.post(webhook.url, json=payload, timeout=5)
        except requests.RequestException:
            pass

