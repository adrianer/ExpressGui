import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import Expressvpn
from threading import Thread



class Selector:
    server_selected = None


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
        print(index)
        self.selector.server_selected = self.express.servers[self.selector.server_selected.country][index]

    def update(self):
        self.get_model().clear()
        print("bacon")
        country = self.selector.server_selected.country
        for item, server in enumerate(self.express.servers[country]):
            self.append_text(server.location)
            if self.express.current_server != None:
                if server.location in self.express.current_server.location:
                    self.set_active(item)
                    self.location_change(self)
                else:
                    self.set_active(0)
                    self.location_change(self)

class ChangeServerButton(Gtk.Button):

    def __init__(self, express, selector, update_parent):
        Gtk.Button.__init__(self, label="Change Server")
        self.connect("clicked",self.change_server)
        self.selector = selector
        self.express = express
        self.update_parent = update_parent

    def disconnect_connect(self):
        self.express.disconnect()
        self.update_parent()
        connect_thread = Thread(target=self.connectionss)
        connect_thread.start()

    def connectionss(self):
        self.express.connect(self.server)
        self.update_parent()

    def change_server(self, widget):
        server = self.selector.server_selected
        self.server = server
        status = self.express.connection_status
        print(server.alias)
        if status is False:
            self.express.connect(server)
        elif status is True and self.express.current_server.location != server.location:
            print("Changing server..")
            disconnect_thread = Thread(target=self.disconnect_connect)
            disconnect_thread.start()
            
class RefreshButton(Gtk.Button):

    def __init__(self, express):
        self.express = express
        Gtk.Button.__init__(self, label="Refresh")
        self.connect("clicked", self.refresh)

    def refresh(self, widget):
        self.express.refresh()
        self.update_servers()


class LocationPicker(Gtk.Window):

    def __init__(self, express, selector, update_parent):
        Gtk.Window.__init__(self, title="Choose a server")
        self.update_parent = update_parent  #Updates the label and switch
        self.express = express
        self.selector = selector
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
        self.connect_button = ChangeServerButton(self.express, self.selector, self.update_parent)
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

