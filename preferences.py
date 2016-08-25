import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PrefCheckButton(Gtk.CheckButton):

	def __init__(self, label, express, status_var, function):
		self.express = express
		self.status_var = status_var
		self.express_call = getattr(express, function)
		self.express_status = getattr(express.preferences, self.status_var)
		Gtk.CheckButton.__init__(self)
		self.set_label(label)
		self.connect('toggled', self.toggled)
		self.update_widget()


	def toggled(self, widget):
		status = self.get_active()
		express_status = getattr(self.express.preferences, self.status_var)
		if status == True and express_status == False:
			self.express_call(True)
		elif status == False and express_status == True:
			self.express_call(False)

	def update_widget(self):
		""" Updates widgets status if it's not equal to status_var"""
		widget_status = self.get_active()
		if self.express_status == True and widget_status != True:
			self.set_active(True)
		elif self.express_status == False and widget_status != False:
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
		self.diagnostics_check_button = PrefCheckButton("Diagnostics", self.express, "send_diagnostics", "temp")
		self.autoconnect_check_button = PrefCheckButton("Autoconnect", self.express, "auto_connect", "autoconnect")
		self.protocol_combo_box = Protocol(self.express)


	def create_container(self):
		box = Gtk.Grid()
		box.set_orientation(1)
		box.add(self.diagnostics_check_button)
		box.add(self.autoconnect_check_button)
		box.add(self.protocol_combo_box)
		self.add(box)
