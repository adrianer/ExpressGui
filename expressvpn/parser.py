from expressvpn.server import Server

def parse_preferences(stream):
    send_diagnostics = False
    stream = stream.split()
    if stream[1] is "false":
        stream[1] = False
    else:
        stream[1] = True
    auto_connect = stream[1]
    prefered_protocol = stream[3]
    if stream[5] is 'true':
        send_diagnostics = True
    return auto_connect, prefered_protocol, send_diagnostics


def parse_status(stream):
    stream = stream.split(None, 2)
    stream = stream[2].strip('\n')
    country, location = parse_location_item(stream)
    return Server(None, country, location, None)


def parse_ls_recent(output):
    servers = []
    output = output.split('\n')
    output = output[2:-1]
    for server in output:
        server = server.split('\t')
        server = list(filter(None, server))[:3]
        country, location = parse_location_item(server[2])
        alias = server[0]
        server = Server(alias, country, location, None)
        servers.append(server)
    return servers


def parse_ls(output):
    """Returns a dictionary containing a list of countries and a list of locations
    ["countries"] for a list of countries """
    server_dict = {}
    server_dict['countries'] = []
    for country, location_list in parse_server_list(output):
        server_dict['countries'].append(country)
        server_dict[country] = location_list
    return server_dict


def parse_server_list(output):
    """Returns the country and a list of locations of that country"""
    location_list = []
    country = None
    output = output.split('\n')
    output = output[2:]

    for server in output:
        server = server.split('\t')
        server = list(filter(None, server))
        if server:
            server = parse_server_item(server)
            if len(location_list) is not 0:
                if (server.country) != location_list[-1].country:
                    yield location_list[-1].country, location_list
                    location_list = []
                    location_list.append(server)
                    country = server.country
                else:
                    location_list.append(server)
            else:
                location_list.append(server)
                country = server.country


def parse_server_item(stream):
    """ Takes a list from the output of expressvpn.ls
        and parses it to create a Server object
    """
    alias = stream[0]
    stream = stream[1:]
    recommended = False

    if stream[-1] is "Y":
        recommended = True
        if len(stream) is 3:
            country, location = parse_location_item(stream[1])
        else:
            country, location = parse_location_item(stream[0])
    else:
        if len(stream) is 2:
            country, location = parse_location_item(stream[1])
        else:
            country, location = parse_location_item(stream[0])

    return Server(alias, country, location, recommended)


def parse_location_item(stream):
    stream = [x.strip(' ') for x in stream.split('-')]
    if len(stream) is 1:
        country = stream[0]
        location = stream[0]
    else:
        country = stream[0]
        location = stream[1]
    if len(stream) is 3:
        location = location + " - " + stream[2]

    return country, location
