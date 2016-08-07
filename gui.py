"""the gui of ExpressvpnGui"""
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import os
import subprocess
import sys, string
import expressvpn


class ExpressGui:
    connected = False
    server_list = {}
    current_server = ""

    def __init__(self):
        self.window = Gtk.Window()
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        self.countries_combobox = Gtk.ComboBoxText()
        self.locations_combobox = Gtk.ComboBoxText()

        self.statusbar = Gtk.Statusbar()

        self.get_servers()
        self.update_country_box()
        self.update_location_box()

        self.box = Gtk.VBox(False, 0)
        self.button = Gtk.Switch()
        self.update_status()

        self.button.connect("notify::active", self.connect, None)
        self.countries_combobox.connect("changed", self.country_change)

        self.refresh_button = Gtk.Button("Refresh")
        self.refresh_button.connect("clicked", self.refresh, None)


        self.box.pack_start(self.button, False, False, 0)
        self.box.pack_start(self.countries_combobox, False, False, 0)
        self.box.pack_start(self.locations_combobox, False, False, 0)
        self.box.pack_start(self.refresh_button, False, False, 0)


        self.window.add(self.box)
        self.refresh_button.show()
        self.button.show()
        self.countries_combobox.show()
        self.locations_combobox.show()
        self.box.show()
        self.window.show()



    def country_change(self, widget):
        self.update_location_box()


    def update_country_box(self):
        for country in self.server_list['countries']:
            self.countries_combobox.append_text(country)
        self.countries_combobox.set_active(0)


    def update_location_box(self):
        self.locations_combobox.get_model().clear()
        country = self.countries_combobox.get_active_text()
        for location in self.server_list[country]:
            self.locations_combobox.append_text(location[0])
        self.locations_combobox.set_active(0)

    def update_servers(self):
        self.get_servers()
        self.update_country_box()
        self.update_location_box()


    def get_servers(self):
        self.server_list = expressvpn.ls()

    def update_status(self):
        status = expressvpn.status()
        if status != None:
            self.current_server = status
            self.connected = True
        else:
            self.connected = False
        self.update_switch()

    def update_switch(self):
        if self.connected == False:
            self.button.set_state(False)
        else:
            self.button.set_state(True)
    
    def connect(self, switch, gparam, location=None):
        location = self.locations_combobox.get_active_text()
        if switch.get_active():
            if location != self.current_server:
                expressvpn.disconnect()
                expressvpn.connect(location)
        else:
            expressvpn.disconnect()

    def disconnect(self, widget, data=None):
        if expressvpn.disconnect() == True:
            self.connected = False
        else:
            self.connected = True
        self.update_status()

    def refresh(self, widget, data=None):
        expressvpn.refresh()
        self.get_servers()
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


