import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class StatusCheckButton(Gtk.CheckButton):
    """Takes a status variable (string) and calls the function callback if status is not
        equal to the widgets status""" 

    def __init__(self, label, obj, status_var, function):
        self.obj = obj
        self.status_var = status_var
        self.obj_call = function
        self.obj_status = getattr(obj, self.status_var)
        Gtk.CheckButton.__init__(self)
        self.set_label(label)
        self.connect('toggled', self.toggled)
        self.update_widget()


    def toggled(self, widget):
        """ Calls the callback function and updates the objects status when the widget is toggled"""
        status = self.get_active()
        obj_status = getattr(self.obj, self.status_var)
        if status == True and obj_status == False:
            self.obj_call(True)
        elif status == False and obj_status == True:
            self.obj_call(False)

    def update_widget(self):
        """ Updates widgets status if it's not equal to status_var"""
        widget_status = self.get_active()
        if self.obj_status == True and widget_status != True:
            self.set_active(True)
        elif self.obj_status == False and widget_status != False:
            self.set_active(False)


class Protocol(Gtk.ComboBoxText):

    def __init__(self, express):
        self.express = express
        Gtk.ComboBoxText.__init__(self)

        self.preferences = express.preferences
        self.connect("changed", self.protocol_changed)
        self.update()

    def protocol_changed(self, widget):
        protocol = self.get_active_text()
        if protocol != self.express.preferences.prefered_protocol:
            self.express.protocol(protocol)
            print("Protocol changed to " + protocol)

    def update(self):
        for item, protocol in enumerate(self.preferences.protocols):
            self.append_text(protocol)
            if protocol == self.express.preferences.prefered_protocol:
                self.set_active(item)


class Preference(Gtk.Window):

    def __init__(self, express):
        self.express = express
        Gtk.Window.__init__(self, title="Preferences")
        self.create_widgets()
        self.create_container()
        self.show_all()


    def create_widgets(self):
        self.diagnostics_check_button = StatusCheckButton("Diagnostics", self.express.preferences, "send_diagnostics", self.express.temp)
        self.autoconnect_check_button = StatusCheckButton("Autoconnect", self.express.preferences, "auto_connect", self.express.autoconnect)
        self.protocol_combo_box = Protocol(self.express)


    def create_container(self):
        box = Gtk.Grid()
        box.set_orientation(1)
        box.add(self.diagnostics_check_button)
        box.add(self.autoconnect_check_button)
        box.add(self.protocol_combo_box)
        self.add(box)
