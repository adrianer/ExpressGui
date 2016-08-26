from expressvpn.server import Server


def parse_preferences(stream):
    """ Returns preferences variables """
    send_diagnostics = False
    stream = stream.split()
    print(stream[1])
    if stream[1] == "false":
        auto_connect = False
    else:
        auto_connect = True
    prefered_protocol = stream[3]
    if stream[5] == 'true':
        send_diagnostics = True
    else:
        send_diagnostics = False
    return auto_connect, prefered_protocol, send_diagnostics


def parse_status(stream):
    """ Returns the a server object from expressvpn status output"""
    stream = stream.split(None, 2)
    stream = stream[2].strip('\n')
    country, location = parse_location_item(stream)
    return Server(None, country, location, None)


def parse_ls_recent(output):
    """ Returns a list of recent server objects """
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
    """ Returns a dictionary containing list of objects seperated by country"""
    return  {key: value for key, value in parse_server_list(output)}


def parse_server_list(output):
    """ Returns the country and a list of locations of that country"""
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
    """ Parses location string in the format country - location """
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
