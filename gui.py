"""the gui of expressGui"""
import os
import subprocess
import sys
import string
import expressvpn
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ExpressGui:

    def __init__(self):
        self.express = expressvpn.Expressvpn()
        # Create containers
        self.create_main_window()
        self.create_dialog()
        # Update the widgets
        self.update()
        self.update_servers()
        # Show the widgets
        self.window.show_all()

    def create_main_window(self):
        self.window = Gtk.Window()
        self.window.set_border_width(10)
        self.box = Gtk.VBox(False, 0)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        # Create the widgets
        self.switch = Gtk.Switch()
        self.location_chooser_button = Gtk.Button('Choose location')
        self.location_label = Gtk.Label()
        # Connect the signals
        self.switch.connect("notify::active", self.switch_toggle, None)
        self.location_chooser_button.connect("clicked",self.locations_dialog)
        # Pack the widgets
        self.box.pack_start(self.switch, False, False, 0)
        self.box.pack_start(self.location_label, False, False, 0)
        self.box.pack_start(self.location_chooser_button, False, False, 0)
        # Add them to the window
        self.window.add(self.box)

    def create_dialog(self):
        # Dialog
        self.dialog = Gtk.Window()
        # The container
        box = Gtk.VBox(False, 0)
        # Add container to dialog
        self.dialog.add(box)
        # Create widgets
        self.refresh_button = Gtk.Button("Refresh")
        self.countries_combobox = Gtk.ComboBoxText()
        self.locations_combobox = Gtk.ComboBoxText()
        self.connect_button = Gtk.Button("Change Server")
        # Connect signals
        self.countries_combobox.connect("changed", self.country_change)
        self.connect_button.connect("clicked", self.dialog_connect) 
        self.refresh_button.connect("clicked", self.refresh)  
        # Add widgets to box container
        box.add(self.countries_combobox)
        box.add(self.locations_combobox)
        box.add(self.connect_button)
        box.add(self.refresh_button)

    
    def locations_dialog(self, widget):
        """Open dialog to switch server"""
        self.dialog.show_all()

    def dialog_connect(self, widget):
        location = self.locations_combobox.get_active_text()
        status = self.express.connection_status
        if status is False:
            self.express.connect(location)
        elif status is True and self.express.current_server != location:
            self.express.disconnect()
            self.express.connect(location)

        self.update()

    def update_location_label(self):
        """Updates the server location label"""
        self.location_label.set_text(self.express.current_server)

    def update_switch(self):
        """Updates the state of the switch"""
        if self.express.connection_status is False:
            self.switch.set_state(False)
        else:
            self.switch.set_state(True)

    def update(self):
        self.update_location_label()
        self.update_switch()


    def switch_toggle(self, switch, gparam, test):
        """ Callback function for the active signal of the switch
            Connects if active disconnects if inactive
        """
        location = self.locations_combobox.get_active_text()
        if self.switch.get_active():
            # switch active so connect if not already connection_status
            if location is not None and self.express.connection_status is not True:
                self.express.disconnect()
                self.express.connect(location)
            else:
                self.express.connect()
        else:
            # switch set to inactive so disconnect
            self.express.disconnect()

        self.update()


    def disconnect(self, widget, data=None):
        if self.express.disconnect() is True:
            self.connection_status = False
        else:
            self.connection_status = True

    def delete_event(self, widget, event, data=None):
        print("Exiting")
        return False

    def destroy(self, widget, data=None):
        Gtk.main_quit()

    def main(self):
        Gtk.main()

    def refresh(self, widget, data=None):
        """Refreshes the list of servers"""
        self.express.refresh()
        self.update_servers()

    def update_country_box(self):
        """Updates the combobox containging the server countries"""
        for country in self.express.servers['countries']:
            self.countries_combobox.append_text(country)
        self.countries_combobox.set_active(0)

    def update_location_box(self):
        """Updates the combobox containing the server locations"""
        self.locations_combobox.get_model().clear()
        country = self.countries_combobox.get_active_text()
        for location in self.express.servers[country]:
            self.locations_combobox.append_text(location[0])
        self.locations_combobox.set_active(0)

    def country_change(self, widget):
        """Updates the location combobox when country is changed"""
        self.update_location_box()

    def get_servers(self):
        """Gets a list of servers from express"""
        self.express.ls()

    def update_servers(self):
        """Gets the servers from express then updates the comboboxs"""
        self.get_servers()
        self.update_country_box()
        self.update_location_box()



if __name__ == "__main__":
    express = ExpressGui()
    express.main()