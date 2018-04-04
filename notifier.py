import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import notify2
import sys
from threading import Thread
# Ubuntu's notify-osd doesn't officially support actions. However, it does have
# a dialog fallback which we can use for this demonstration. In real use, please
# respect the capabilities the notification server reports!
OVERRIDE_NO_ACTIONS = True

EMPTY_FUNCTION = lambda *a: None


class Notifier:
    def __init__(self, timeout):
        # start gtk loop in new thread
        self.timeout = timeout
        print("Init Notifier")
        self.mainloop = Thread(target=Gtk.main)
        self.mainloop.start()
        if not notify2.init("Default Action Test", mainloop='glib'):
            sys.exit(1)

    def close(self):
        Gtk.main_quit()
        self.mainloop.join()

    def notify(self, title, summary, icon="", data=None, default_cb=EMPTY_FUNCTION, closed_cb=EMPTY_FUNCTION):
        server_capabilities = notify2.get_server_caps()

        n = notify2.Notification(title, summary, icon)
        if ('actions' in server_capabilities) or OVERRIDE_NO_ACTIONS:
            n.add_action("default", "Default Action", default_cb, data)
        n.connect('closed', closed_cb)
        n.set_timeout(self.timeout)
        if not n.show():
            print("Failed to send notification")
            sys.exit(1)
