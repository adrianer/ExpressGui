"""the gui of ExpressvpnGui"""
import os
import subprocess
import sys
import string
import expressvpn
from gi.repository import Gtk
import gi
gi.require_version('Gtk', '3.0')


class ExpressGui:
    connected = False
    server_list = {}
    current_server = ""

    def __init__(self):
        # Create containers
        self.window = Gtk.Window()
        self.window.set_border_width(10)
        self.box = Gtk.VBox(False, 0)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        # Create comboboxs
        self.countries_combobox = Gtk.ComboBoxText()
        self.locations_combobox = Gtk.ComboBoxText()
        self.statusbar = Gtk.Statusbar()
        # Create the buttons
        self.switch = Gtk.Switch()
        self.refresh_switch = Gtk.switch("Refresh")
        # Connect the signals
        self.switch.connect("notify::active", self.connect, None)
        self.refresh_switch.connect("clicked", self.refresh, None)
        self.countries_combobox.connect("changed", self.country_change)
        # Pack the widgets
        self.box.pack_start(self.switch, False, False, 0)
        self.box.pack_start(self.countries_combobox, False, False, 0)
        self.box.pack_start(self.locations_combobox, False, False, 0)
        self.box.pack_start(self.refresh_switch, False, False, 0)
        # Add them to the window
        self.window.add(self.box)
        # Show the widgets
        self.refresh_switch.show()
        self.switch.show()
        self.countries_combobox.show()
        self.locations_combobox.show()
        self.box.show()
        self.window.show()
        # Get vpn servers and update status
        self.update_servers()
        self.update_status()

    def country_change(self, widget):
        """Updates the location combobox when country is changed"""
        self.update_location_box()

    def update_country_box(self):
        """Updates the combobox containging the server countries"""
        for country in self.server_list['countries']:
            self.countries_combobox.append_text(country)
        self.countries_combobox.set_active(0)

    def update_location_box(self):
        """Updates the combobox containing the server locations"""
        self.locations_combobox.get_model().clear()
        country = self.countries_combobox.get_active_text()
        for location in self.server_list[country]:
            self.locations_combobox.append_text(location[0])
        self.locations_combobox.set_active(0)

    def update_servers(self):
        """Gets the servers from expressvpn then updates the comboboxs"""
        self.get_servers()
        self.update_country_box()
        self.update_location_box()

    def get_servers(self):
        """Gets a list of servers from expressvpn"""
        self.server_list = expressvpn.ls()

    def update_status(self):
        """Gets expressvpn connection status"""
        status = expressvpn.status()
        if status is None:
            self.current_server = status
            self.connected = True
        else:
            self.connected = False
        self.update_switch()

    def update_switch(self):
        """Updates the state of the switch"""
        if self.connected is False:
            self.switch.set_state(False)
        else:
            self.switch.set_state(True)

    def connect(self, switch, gparam, location=None):
        """ Callback function for the active signal of the switch
            Connects if active disconnects if inactive
        """
        location = self.locations_combobox.get_active_text()
        if switch.get_active():
            # switch active so connect if not already connected
            if location != self.current_server:
                expressvpn.disconnect()
                expressvpn.connect(location)
        else:
            # switch set to inactive so disconnect
            expressvpn.disconnect()

    def disconnect(self, widget, data=None):
        if expressvpn.disconnect() is True:
            self.connected = False
        else:
            self.connected = True
        self.update_status()

    def refresh(self, widget, data=None):
        """Refreshes the list of servers"""
        expressvpn.refresh()
        self.update_servers()

    def delete_event(self, widget, event, data=None):
        print("Exiting")
        return False

    def destroy(self, widget, data=None):
        Gtk.main_quit()

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    express = ExpressGui()
    express.main()
