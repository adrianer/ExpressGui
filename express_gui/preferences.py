import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class StatusCheckButton(Gtk.CheckButton):
    """Takes a status variable (string) and calls the function callback if status is not
        equal to the widgets status
    """

    def __init__(self, label, var_string, status_obj, callback):
        super().__init__()
        self.status_obj = status_obj
        self.var_string = var_string
        self.set_label(label)
        self.callback = callback
        self.connect('toggled', self.toggled)
        self.update_widget()

    def toggled(self, widget):
        """ Calls the callback function and updates the objects status when the widget is toggled"""
        status = self.get_active()
        status_var = getattr(self.status_obj ,self.var_string)
        if status == True and  status_var == False:
            self.callback(True)
        elif status == False and status_var == True:
            self.callback(False)

    def update_widget(self):
        """ Updates widgets status if it's not equal to status_var"""
        widget_status = self.get_active()
        status_var = getattr(self.status_obj, self.var_string)
        if status_var == True and widget_status != True:
            self.set_active(True)
        elif status_var == False and widget_status != False:
            self.set_active(False)


class ListComboBox(Gtk.ComboBoxText):
    """ Populates combobox with list and calls obj_call when changed """

    def __init__(self):
        super().__init__()
        self.connect("changed", self.changed)
        self.update()

    def changed(self, widget):
        active_item = self.get_active_text()
        if active_item != self.item:
            self.obj_call(self.item)
            print("Protocol changed to " + self.item)

    def update(self):
        for count, item in enumerate(self.item_list):
            self.append_text(item)
            if item == self.item:
                self.set_active(count)


class Protocol(ListComboBox):

    def __init__(self, express):
        self.obj_call = express.protocol
        self.item_list = express.preferences.protocols
        self.item = express.preferences.prefered_protocol
        super().__init__()


class Preference(Gtk.Window):

    def __init__(self, express):
        super().__init__(title="Preferences")
        self.express = express
        self.create_widgets()
        self.create_container()
        self.show_all()

    def create_widgets(self):
        self.diagnostics_check_button = StatusCheckButton("Send Diagnostics", "send_diagnostics", self.express.preferences, self.express.temp)
        self.autoconnect_check_button = StatusCheckButton("Autoconnect", "auto_connect", self.express.preferences, self.express.autoconnect)
        self.protocol_combo_box = Protocol(self.express)

    def create_container(self):
        box = Gtk.Grid()
        box.set_orientation(1)
        box.add(self.diagnostics_check_button)
        box.add(self.autoconnect_check_button)
        box.add(self.protocol_combo_box)
        self.add(box)
