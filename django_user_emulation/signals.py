from django.dispatch import Signal

emulation_started = Signal(providing_args=['logged_in_user_id', 'emulated_user_id', 'request'])
emulation_ended = Signal(providing_args=['logged_in_user_id', 'emulated_user_id', 'request'])
