import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from expressvpn.expressvpn import Expressvpn
from express_gui.location_picker import LocationPicker
from express_gui.selector import Selector
from express_gui.menu import MenuButton


class ConnectSwitch(Gtk.Switch):

    def __init__(self, express, selector):
        Gtk.Switch.__init__(self)
        self.express = express
        self.selector = selector
        self.connect("notify::active", self.switch_toggle, None)

    def update(self):
        if self.express.connection_status is False:
            self.set_state(False)
        else:
            self.set_state(True)

    def switch_toggle(self, switch, gparam, test):
        """ Callback function for the active signal of the switch
            Connects if active disconnects if inactive
        """
        status = self.get_active()
        if status is True and self.express.connection_status is not True:
            self.express.connect(self.selector.server_selected)
        elif status is False and self.express.connection_status is not False:
            self.express.disconnect()


class LocationLabel(Gtk.Label):

    def __init__(self, express, selector):
        Gtk.Label.__init__(self)
        self.express = express
        self.selector = selector

    def update(self):
        self.set_text(self.selector.get_server_text())


class LocationButton(Gtk.Button):

    def __init__(self, dialog):
        Gtk.Button.__init__(self, "Choose Location")
        self.connect("clicked", self.dialog_show)
        self.dialog = dialog

    def dialog_show(self, widget):
        self.dialog.show_all()


class Window(Gtk.Window):

    def __init__(self):
        self.express = Expressvpn()
        self.selector = Selector(self.express)
        self.location_dialog = LocationPicker(self.express, self.selector,
                                              self.update)
        self.create_main_window()
        self.create_widgets()
        self.create_container()
        self.update()
        self.show_all()

    def create_main_window(self):
        Gtk.Window.__init__(self, title="Expressvpn")
        self.set_border_width(10)
        self.connect("delete_event", self.delete_event)
        self.connect("destroy", self.destroy)

    def create_widgets(self):
        self.switch = ConnectSwitch(self.express, self.selector)
        self.location_label = LocationLabel(self.express, self.selector)
        self.location_chooser_button = LocationButton(self.location_dialog)
        self.menu_button = MenuButton(self.express)

    def create_container(self):
        box = Gtk.Grid()
        box.set_orientation(1)
        box.add(self.menu_button)
        box.add(self.switch)
        box.add(self.location_label)
        box.add(self.location_chooser_button)
        self.add(box)

    def update(self):
        self.location_label.update()
        self.switch.update()

    def delete_event(self, widget, event, data=None):
        print("Exiting")
        return False

    def destroy(self, widget, data=None):
        Gtk.main_quit()

    def main(self):
        Gtk.main()
