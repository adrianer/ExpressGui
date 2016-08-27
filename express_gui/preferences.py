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
        status_var = getattr(self.status_obj, self.var_string)
        if status == True and status_var == False:
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


class StatusComboBox(Gtk.ComboBoxText):
    """ Populates combobox with list and calls obj_call when changed 
        if the active item is not equal to status 
    """

    def __init__(self, status_var, callback, item_list, status_obj):
        super().__init__()
        self.callback = callback
        self.status_obj = status_obj
        self.status = status_var
        self.item_list = item_list
        self.connect("changed", self.changed)
        self.update()

    def changed(self, widget):
        """ If widget status and obj are not equal call the callback """
        active_item = self.get_active_text()
        status_var = getattr(self.status_obj, self.status)
        if active_item != status_var:
            self.callback(active_item)
            print("Protocol changed to " + active_item)

    def update(self):
        """ Populate combobox with the list """
        status_var = getattr(self.status_obj, self.status)
        for count, item in enumerate(self.item_list):
            self.append_text(item)
            if item == status_var:
                self.set_active(count)


class Preference(Gtk.Window):

    def __init__(self, express):
        super().__init__(title="Preferences")
        self.express = express
        self.create_widgets()
        self.create_container()
        self.show_all()

    def create_widgets(self):
        self.diagnostics_check_button = StatusCheckButton(
            "Send Diagnostics", "send_diagnostics", self.express.preferences, self.express.temp)
        self.autoconnect_check_button = StatusCheckButton(
            "Autoconnect", "auto_connect", self.express.preferences, self.express.autoconnect)
        self.protocol_combo_box = StatusComboBox(
            "prefered_protocol", self.express.protocol, self.express.preferences.protocols, self.express.preferences)

    def create_container(self):
        box = Gtk.Grid()
        box.set_orientation(1)
        box.add(self.diagnostics_check_button)
        box.add(self.autoconnect_check_button)
        box.add(self.protocol_combo_box)
        self.add(box)
