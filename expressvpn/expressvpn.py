import subprocess
from expressvpn import parser
from expressvpn.preferencer import Preferencer

class Expressvpn:
    connection_status = False
    current_server = None
    servers = {}
    last_server = None

    def __init__(self):
        self.status()
        self.ls()
        self.last_server = self.ls_recent()[0]
        self.set_preferences()

    def get_preferences(self):
        output = subprocess.check_output(
            ["expressvpn", "preferences"]).decode("utf-8")
        autoconnect, prefered_protocol, send_diagnostics = parser.parse_preferences(output)
        return Preferencer(autoconnect, prefered_protocol, send_diagnostics)

    def set_preferences(self):
        self.preferences = self.get_preferences()

    def autoconnect(self, state):
        state = str(state)
        subprocess.call(["expressvpn", "autoconnect",state])
        if state == "False":
            self.preferences.auto_connect = False
        else:
            self.preferences.auto_connect = True

    def protocol(self, protocol="auto"):
        subprocess.call(["expressvpn", "protocol", protocol])
        self.preferences.prefered_protocol = protocol

    def status(self):
        stream = subprocess.check_output(
            ["expressvpn", "status"]).decode('utf-8')
        if "Not connected" in stream:
            self.connection_status = False
        else:
            self.current_server = parser.parse_status(stream)

            self.connection_status = True

    def connect(self, server=None):
        print("Attempting to Connect")

        if server is not None:
            stream = subprocess.call(["expressvpn", "connect", server.alias])
            self.current_server = server
        else:
            stream = subprocess.call(["expressvpn", "connect"])
        if stream == 0 or 1:
            self.connection_status = True
            print("Connection Success")

    def disconnect(self):
        stream = subprocess.call(["expressvpn", "disconnect"])
        if stream == 0 or 1:
            print("Disconnect Success")
            self.connection_status = False

    def ls(self):
        output = subprocess.check_output(["expressvpn", "ls"]).decode('utf-8')
        self.servers = parser.parse_ls(output)

    def ls_recent(self):
        output = subprocess.check_output(
            ["expressvpn", "ls", "recent"]).decode('utf-8')
        recent_servers = parser.parse_ls_recent(output)
        return recent_servers

    def refresh(self):
        output = subprocess.call(["expressvpn", "refresh"])
        if output == 0:
            return True
    def temp(self):
        print("bacon")


if __name__ == "__main__":
    # Example of usage
    express = Expressvpn()
    express.preferences()
