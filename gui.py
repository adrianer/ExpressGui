"""the gui of ExpressvpnGui"""
import pygtk
pygtk.require('2.0')
import gtk
import os
import subprocess
import sys, string
import expressvpn


class ExpressGui:
    connected = False

    def __init__(self):
        self.connected = expressvpn.connect()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        self.countries_combobox = gtk.combo_box_new_text()
        self.locations_combobox = gtk.combo_box_new_text()

        self.get_servers()
        self.update_country_box()
        self.update_location_box()

        self.status_label = gtk.Label()
        self.update_status()
        self.box = gtk.HBox(False, 0)
        self.button = gtk.Button("connect")
        self.button.connect("clicked", self.connect, None)
        self.countries_combobox.connect("changed", self.country_change)
        self.disconnect_button = gtk.Button("disconnect")
        self.disconnect_button.connect("clicked", self.disconnect, None)

        self.box.pack_start(self.button, False, False, 0)
        self.box.pack_start(self.disconnect_button, False, False, 0)
        self.box.pack_start(self.status_label, False, False, 0)
        self.box.pack_start(self.countries_combobox, False, False, 0)
        self.box.pack_start(self.locations_combobox, False, False, 0)

        self.window.add(self.box)
        self.button.show()
        self.countries_combobox.show()
        self.locations_combobox.show()
        self.disconnect_button.show()
        self.status_label.show()
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

    def get_servers(self):
        self.server_list = expressvpn.ls()


    def update_status(self):
        if self.connected == False:
            self.status_label.set_text("Not connected")
        else:
            self.status_label.set_text("Connected")
    
    def connect(self, widget, data=None):
        location = self.locations_combobox.get_active_text()
        self.connected = expressvpn.connect(location)
        self.update_status()

    def disconnect(self, widget, data=None):
        if expressvpn.disconnect() == True:
            self.connected = False
        else:
            self.connected = True
        self.update_status()

    def delete_event(self, widget, event, data=None):
        print("Exiting")
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    express = ExpressGui()
    express.main()


