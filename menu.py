import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

def Preferences(test):
    #TODO
    pass

def About(test):
    #TODO
    pass


class MenuButton(Gtk.MenuButton):

    def __init__(self):
        Gtk.MenuButton.__init__(self)
        menu = Menu()
        menu.show()
        self.set_popup(menu)
        self.set_halign(2)

class Menu(Gtk.Menu):

    def __init__(self):
        menu_names = ["Preferences","About"]
        Gtk.Menu.__init__(self)
        self.set_title("bacon")
        for name in menu_names:
            menuitem = Gtk.MenuItem(label=name)
            self.append(menuitem)
            menuitem.show()
            menuitem.connect("activate", globals()[name])