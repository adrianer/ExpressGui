import subprocess
import Expressvpn
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class LocationPicker(Gtk.Window):

    def __init__(self, parent):
        Gtk.Window.__init__(self, title="Choose a server")
        self.parent = parent
        self.express = parent.express
        box = Gtk.VBox(False, 0)
        # Add container to dialog
        self.add(box)
        # Create widgets
        self.refresh_button = Gtk.Button("Refresh")
        self.countries_combobox = Gtk.ComboBoxText()
        self.locations_combobox = Gtk.ComboBoxText()
        self.connect_button = Gtk.Button("Change Server")

        self.connect("delete_event", self.delete_event)
        # Connect signals
        self.countries_combobox.connect("changed", self.country_change)
        self.connect_button.connect("clicked", self.dialog_change_server) 
        self.refresh_button.connect("clicked", self.refresh)  
        # Add widgets to box container
        box.add(self.countries_combobox)
        box.add(self.locations_combobox)
        box.add(self.connect_button)
        box.add(self.refresh_button)
        self.update_servers()

    def delete_event(self, widget, event, data=None):
        self.hide()

    def destroy(self, widget, data=None):
        self.hide()

    def dialog_change_server(self, widget):
        """Changes vpn server"""
        location = self.locations_combobox.get_active_text()
        status = self.express.connection_status
        if status is False:
            self.express.connect(location)
        elif status is True and self.express.current_server.location != location:
            self.express.disconnect()
            self.express.connect(location)

        self.parent.update()

    def update_country_box(self):
        """Updates the combobox containging the server countries"""
        for item, country in enumerate(self.express.servers['countries']):
            self.countries_combobox.append_text(country)
            if self.express.current_server != None:
                if country in self.express.current_server.country:
                    self.countries_combobox.set_active(item)
            else:
                self.countries_combobox.set_active(0)

    def update_location_box(self):
        """Updates the combobox containing the server locations"""
        self.locations_combobox.get_model().clear()
        country = self.countries_combobox.get_active_text()
        for item, location in enumerate(self.express.servers[country]):
            location = location.location
            self.locations_combobox.append_text(location)
            if self.express.current_server != None:
                if location in self.express.current_server.location:
                    self.locations_combobox.set_active(item)
                else:
                    self.locations_combobox.set_active(0)


    def update_servers(self):
        """Gets the servers from express then updates the comboboxs"""
        self.get_servers()
        self.update_country_box()
        self.update_location_box()

    def country_change(self, widget):
        """Updates the location combobox when country is changed"""
        self.update_location_box()

    def get_servers(self):
        """Gets a list of servers from express"""
        self.express.ls()

    def refresh(self, widget, data=None):
        """Refreshes the list of servers"""
        self.express.refresh()
        self.update_servers()