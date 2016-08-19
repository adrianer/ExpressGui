"""module to interact with expressvpn"""
import subprocess

class Expressvpn:
    connection_status = False
    current_server = ""
    current_country = ""
    servers = {}
    auto_connect = False
    prefered_protocol = ""
    send_diagnostics = True
    protocols = ["udp", "auto", "tcp"]

    def __init__(self):
        self.status()
        self.ls()

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
        print(stream)

    def autoconnect(self):
        subprocess.call(["expressvpn", "autoconnect"])

    def protocol(self, protocol="auto"):
        subprocess.call(["expressvpn", "protocol", protocol])

    def status(self):
        stream = subprocess.check_output(["expressvpn", "status"]).decode('utf-8')
        if "Not connected" in stream:
            self.connection_status = False
        else:
            stream = stream.split(None, 2)
            stream = stream[2].strip('\n')
            self.current_server = stream
            self.connection_status = True

    def connect(self, location=None):
        if location is not None:
            stream = subprocess.call(["expressvpn", "connect", location])
            self.current_server = location
        else:
            stream = subprocess.call(["expressvpn", "connect"])
        if stream == 0 or 1:
            self.connection_status = True

    def disconnect(self):
        stream = subprocess.call(["expressvpn", "disconnect"])
        if stream == 0 or 1:
            self.connection_status = False

    def print_servers(server_dict):
        print('--------------------------')
        for country in server_dict['countries']:
            print(country)
        for location in server_dict[country]:
            print(location)

    def get_countries_locations(self, output):
        """Returns the country and a list of locations of that country"""
        location_list = []
        country = None
        output = output.split('\n')             # Remove new line
        output = output[2:]                     # Remove decoration

        for server in output:
            server = server.split('\t')
            server = list(filter(None, server))       # Remove blank items
            # Check for new country
            if len(server) == 4 or len(server) == 3 and server[2] != "Y":
                # New country
                if country is not None:
                    # return the country and its list of locations
                    yield country, location_list
                    # Start a new list
                    location_list = []
                    # Add the location to the list
                    location_list.append(server[2:])
                    # Set new current country
                    country = server[1]
                else:
                    # The first location from output
                    location_list.append(server[2:])
                    # Set current country
                    country = server[1]
            else:
                location_list.append(server[1:])      # Add location

    def parse_ls_output(self, output):
        """Returns a dictionary containing a list of countries and a list of locations
        ["countries"] for a list of countries """
        server_dict = {}
        server_dict['countries'] = []
        for country, location_list in self.get_countries_locations(output):
            # Add the country to country dictionary key
            server_dict['countries'].append(country)
            # Add the list of locations to the couontry key
            server_dict[country] = location_list

        return server_dict

    def ls(self):
        """Gets the list of locations"""
        output = subprocess.check_output(["expressvpn", "ls"]).decode('utf-8')
        location_list = self.parse_ls_output(output)
        self.servers = location_list

    def refresh(self):
        """Refreshes the list of locations"""
        output = subprocess.call(["expressvpn", "refresh"])
        if output == 0:
            return True


if __name__ == "__main__":
    # Example of usage
    express = Expressvpn()
    express.preferences()

