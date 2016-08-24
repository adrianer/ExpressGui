import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Diagnostics(Gtk.CheckButton):

	def __init__(self, express):
		self.express = express
		Gtk.CheckButton.__init__(self)
		self.set_label("Send Diagnostics")
		self.connect('toggled', self.toggled)
		self.update()

	def toggled(self, widget):
		pass

	def update(self):
		if self.express.preferences.send_diagnostics is True:
			self.set_active(True)
		else:
			self.set_active(False)

class AutoConnect(Gtk.CheckButton):

	def __init__(self, express):
		Gtk.CheckButton.__init__(self)
		self.express = express
		self.set_label("Autoconnect")
		self.update()
		self.connect('toggled', self.toggled)

	def toggled(self, widget):
		status = self.get_active()
		print(status)
		if status == True and self.express.preferences.auto_connect == False:
			self.express.autoconnect(True)
		elif status == False and self.express.preferences.auto_connect == True:
			self.express.autoconnect(False)
		self.update()

	def update(self):
		status = self.get_active()
		pref_status = self.express.preferences.auto_connect
		if status == False and pref_status == False:
			self.set_active(False)
		elif status == True and pref_status == True:
			self.set_active(True)



class Protocol(Gtk.ComboBoxText):

	def __init__(self, express):
		Gtk.ComboBoxText.__init__(self)
		self.express = express
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

	def __init__(self, preferences):
		Gtk.Window.__init__(self, title="Preferences")
		self.preferences = preferences
		self.create_widgets()
		self.create_container()
		self.show_all()


	def create_widgets(self):
		self.diagnostics_check_button = Diagnostics(self.preferences)
		self.autoconnect_check_button = AutoConnect(self.preferences)
		self.protocol_combo_box = Protocol(self.preferences)


	def create_container(self):
		box = Gtk.Grid()
		box.set_orientation(1)
		box.add(self.diagnostics_check_button)
		box.add(self.autoconnect_check_button)
		box.add(self.protocol_combo_box)
		self.add(box)
