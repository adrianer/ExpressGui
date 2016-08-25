import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from express_gui.preferences import Preference
from expressvpn.expressvpn import Expressvpn


def Preferences(test, express):
    Preference(express)


def About(test):
    # TODO
    pass


class Menu(Gtk.Menu):

    def __init__(self, express):
        menu_names = ["Preferences", "About"]
        Gtk.Menu.__init__(self)
        self.set_title("bacon")
        for name in menu_names:
            menuitem = Gtk.MenuItem(label=name)
            self.append(menuitem)
            menuitem.show()
            menuitem.connect("activate", globals()[name], express)


class MenuButton(Gtk.MenuButton):

    def __init__(self, express):
        Gtk.MenuButton.__init__(self)
        menu = Menu(express)
        menu.show()
        self.set_popup(menu)
        self.set_halign(2)
