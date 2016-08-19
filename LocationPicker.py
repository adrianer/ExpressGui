import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import Expressvpn


class CountryComboBox(Gtk.ComboBoxText):

    def __init__(self, express, selector, locations):
        Gtk.ComboBoxText.__init__(self)
        self.connect("changed", self.country_change)
        self.express = express
        self.selector = selector
        self.locations = locations

    def update(self):
        for item, country in enumerate(self.express.servers['countries']):
            self.append_text(country)
            if self.express.current_server != None:
                if country in self.express.current_server.country:
                    self.set_active(item)
            else:
                self.set_active(0)

    def country_change(self, widget):
        self.selector.server_selected.country = self.get_active_text()
        self.locations.update()

class LocationComboBox(Gtk.ComboBoxText):

    def __init__(self, express, selector):
        Gtk.ComboBoxText.__init__(self)
        self.connect("changed", self.location_change)
        self.express = express
        self.selector = selector

    def location_change(self, test):
        index = test.get_active()
        self.selector.server_selected = self.express.servers[self.selector.server_selected.country][index]

    def update(self):
        self.get_model().clear()
        country = self.selector.server_selected.country
        for item, server in enumerate(self.express.servers[country]):
            self.append_text(server.location)
            if self.express.current_server != None:
                if server.location in self.express.current_server.location:
                    self.set_active(item)
                    self.selector.server_selected = server
                else:
                    self.set_active(0)
                    self.selector.server_selected = server

class ChangeServerButton(Gtk.Button):

    def __init__(self, express, selector):
        Gtk.Button.__init__(self, label="Change Server")
        self.selector = selector
        self.connect("clicked", self.change_server) 
        self.express = express

    def change_server(self, widget):
        server = self.selector.server_selected
        status = self.express.connection_status
        if status is False:
            self.express.connect(server)
        elif status is True and self.express.current_server.location != server.location:
            self.express.disconnect()
            self.express.connect(server)

class RefreshButton(Gtk.Button):

    def __init__(self, express):
        self.express = express
        Gtk.Button.__init__(self, label="Refresh")
        self.connect("clicked", self.refresh)

    def refresh(self, widget):
        self.express.refresh()
        self.update_servers()

class Selector:
    server_selected = None

class LocationPicker(Gtk.Window):

    def __init__(self, parent):
        Gtk.Window.__init__(self, title="Choose a server")
        self.parent = parent
        self.express = parent.express
        self.selector = Selector()
        if self.express.current_server != None:
            self.selector.server_selected = self.express.current_server
        else:
            self.selector.server_selected = self.express.servers[self.express.servers['countries'][0]][0]

        self.create_widgets()
        self.add(self.add_widgets())
        self.update_servers()

    def create_widgets(self): 
        self.locations_combobox = LocationComboBox(self.express, self.selector)
        self.countries_combobox = CountryComboBox(self.express, self.selector, self.locations_combobox)
        self.connect_button = ChangeServerButton(self.express, self.selector)
        self.refresh_button = RefreshButton(self.express)

    def add_widgets(self):
        box = Gtk.VBox(False, 0)
        box.add(self.countries_combobox)
        box.add(self.locations_combobox)
        box.add(self.connect_button)
        box.add(self.refresh_button)
        return box

    def update_servers(self):
        self.get_servers()
        self.countries_combobox.update()
        self.locations_combobox.update()

    def get_servers(self):
        self.express.ls()

