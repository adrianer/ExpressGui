"""module to interact with expressvpn"""
import subprocess


def status():
    stream = subprocess.check_output(["expressvpn", "status"])
    if "Not connected" in stream:
        return None
    else:
        stream = stream.split(None, 2)
        stream = stream[2].strip('\n')
        return stream


def connect(location=None):
    if location != None:
        stream = subprocess.call(["expressvpn", "connect", location])
    else:
        stream = subprocess.call(["expressvpn", "connect"])
    if stream == 0 or 1:
        # Connected
        return True


def disconnect():
    stream = subprocess.call(["expressvpn", "disconnect"])
    if stream == 0 or 1:
        # Disconnected
        return True

def print_servers(server_dict):
    print('--------------------------')
    for country in server_dict['countries']:
        print(country)
        for location in server_dict[country]:
            print(location)

def get_countries_locations(output):
    location_list = []
    country = None
    output = output.split('\n')             # Remove new line
    output = output[2:]                     # Remove decoration

    for server in output:
        server = server.split('\t')         
        server = filter(None, server)       # Remove blank items
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

def parse_ls_output(output):
    """returns a dictionary containing a list of countries and a list of locations
        ["countries"] for a list of countries """
    server_dict = {}
    server_dict['countries'] = []

    for country, location_list in get_countries_locations(output):
        server_dict['countries'].append(country)
        server_dict[country] = location_list

    return server_dict


def ls():
    output = subprocess.check_output(["expressvpn", "ls"])
    location_list = parse_ls_output(output)
    return location_list

def refresh():
    output = subprocess.call(["expressvpn", "refresh"])
    if output == 0:
        return True


if __name__ == "__main__":
    # Example of usage
    if status() is False:
        connect()
    server_dict = ls()
    print_servers(server_dict)
