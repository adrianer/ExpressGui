import subprocess
import Expressvpn
from LocationPicker import LocationPicker
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Window(Gtk.Window):

    def __init__(self, expressvpn):
        self.express = expressvpn
        self.create_main_window()
        self.create_widgets()
        self.dialog = LocationPicker(self)
        self.update()
        self.show_all()

    def create_main_window(self):
        Gtk.Window.__init__(self, title="Expressvpn")
        self.set_border_width(10)
        self.connect("delete_event", self.delete_event)
        self.connect("destroy", self.destroy)
        self.box = Gtk.VBox(False, 0)
        self.add(self.box)

    def create_widgets(self):
        # Create the widgets
        self.switch = Gtk.Switch()
        self.location_chooser_button = Gtk.Button('Choose location')
        self.location_label = Gtk.Label()
        # Connect the signals
        self.switch.connect("notify::active", self.switch_toggle, None)
        self.location_chooser_button.connect("clicked",self.dialog_location_select)
        # Pack the widgets
        self.box.pack_start(self.switch, False, False, 0)
        self.box.pack_start(self.location_label, False, False, 0)
        self.box.pack_start(self.location_chooser_button, False, False, 0)

    def update(self):
        """Updates the location label and connection status switch"""
        self.update_location_label()
        self.update_switch()

    def update_location_label(self):
        """Updates the server location label"""
        if self.express.current_server != None:
            country = self.express.current_server.country
            location = self.express.current_server.location
            self.location_label.set_text(country + " - " + location)

    def update_switch(self):
        """Updates the state of the switch"""
        if self.express.connection_status is False:
            self.switch.set_state(False)
        else:
            self.switch.set_state(True)

    def switch_toggle(self, switch, gparam, test):
        """ Callback function for the active signal of the switch
            Connects if active disconnects if inactive
        """
        #server = self.dialog.locations_combobox.get_active_text()
        server = self.dialog.server_selected
        if self.switch.get_active():
            # switch active so connect if not already connection_status
            if server is not None and self.express.connection_status is not True:
                self.express.disconnect()
                self.express.connect(server)
            else:
                self.express.connect()
        else:
            # switch set to inactive so disconnect
            self.express.disconnect()

        self.update()

    def dialog_location_select(self, widget):
        """Open dialog to switch server"""
        self.dialog = LocationPicker(self)
        self.dialog.show_all()

    def delete_event(self, widget, event, data=None):
        print("Exiting")
        return False

    def destroy(self, widget, data=None):
        Gtk.main_quit()

    def main(self):
        Gtk.main()


if __name__ == "__main__":
    expresss = Expressvpn.Expressvpn()
    express = Window(expresss)
    express.main()