from django.dispatch import Signal

#post share creation signal
post_creation = Signal(providing_args=["ctext"])

