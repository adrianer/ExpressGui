"""module to interact with expressvpn"""
import subprocess
import Parser
from Server import Server


class Expressvpn:
    connection_status = False
    current_server = None
    servers = {}
    auto_connect = False
    prefered_protocol = ""
    send_diagnostics = True
    protocols = ["udp", "auto", "tcp"]

    def __init__(self):
        self.status()
        self.ls()
        self.preferences()

    def preferences(self):
        stream = subprocess.check_output(["expressvpn","preferences"]).decode("utf-8")
        stream = stream.split()
        if stream[1] is "false":
            stream[1] = False
        else:
            stream[1] = True
        self.prefered_protocol = stream[3]
        if stream[5] is 'true':
            self.send_diagnostics = True

    def autoconnect(self):
        subprocess.call(["expressvpn", "autoconnect"])

    def protocol(self, protocol="auto"):
        subprocess.call(["expressvpn", "protocol", protocol])

    def status(self):
        stream = subprocess.check_output(["expressvpn", "status"]).decode('utf-8')
        if "Not connected" in stream:
            self.connection_status = False
        else:
            self.current_server = Parser.parse_status(stream)

            self.connection_status = True

    def connect(self, server=None):
        if server is not None:
            stream = subprocess.call(["expressvpn", "connect", server.alias])
            self.current_server = server
        else:
            stream = subprocess.call(["expressvpn", "connect"])
        if stream == 0 or 1:
            self.connection_status = True

    def disconnect(self):
        stream = subprocess.call(["expressvpn", "disconnect"])
        if stream == 0 or 1:
            print("test")
            self.connection_status = False

    def ls(self):
        """Gets the list of locations"""
        output = subprocess.check_output(["expressvpn", "ls"]).decode('utf-8')
        self.servers = Parser.parse_ls_output(output)

    def refresh(self):
        """Refreshes the list of locations"""
        output = subprocess.call(["expressvpn", "refresh"])
        if output == 0:
            return True




if __name__ == "__main__":
    # Example of usage
    express = Expressvpn()
    express.preferences()

