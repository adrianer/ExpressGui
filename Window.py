import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from Expressvpn import Expressvpn
from LocationPicker import LocationPicker
from LocationPicker import Selector

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
        server = self.selector.server_selected
        status = self.get_active()
        if status is True and self.express.connection_status != True:
            self.express.connect(server)
        elif status is False and self.express.connection_status != False:
            self.express.disconnect()

class LocationLabel(Gtk.Label):
    def __init__(self, express, selector):
        Gtk.Label.__init__(self)
        self.express = express
        self.selector = selector

    def update(self):
        if self.express.current_server != None:
            country = self.selector.server_selected.country
            location = self.selector.server_selected.location
            self.set_text(country + " - " + location)
        elif self.express.last_server != None:
            country = self.selector.server_selected.country
            location = self.selector.server_selected.location
            self.set_text(country + " - " + location)
        else:
            self.set_text("Error")



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
        self.location_dialog = LocationPicker(self.express, self.selector, self.update)
        self.create_main_window()
        self.create_widgets()
        self.update()
        self.show_all()

    def create_main_window(self):
        Gtk.Window.__init__(self, title="Expressvpn")
        self.set_border_width(10)
        self.connect("delete_event", self.delete_event)
        self.connect("destroy", self.destroy)
        
    def create_widgets(self):
        box = Gtk.VBox(False, 0)
        self.switch = ConnectSwitch(self.express, self.selector)
        self.location_label = LocationLabel(self.express, self.selector)
        self.location_chooser_button = LocationButton(self.location_dialog)
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


if __name__ == "__main__":

    expressgui = Window()
    expressgui.main()