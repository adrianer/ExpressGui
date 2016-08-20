from Server import Server


def parse_ls_output(output):
    """Returns a dictionary containing a list of countries and a list of locations
    ["countries"] for a list of countries """
    server_dict = {}
    server_dict['countries'] = []
    for country, location_list in get_countries_locations(output):
        # Add the country to country dictionary key
        #print(repr(country))
        server_dict['countries'].append(country)
        # Add the list of locations to the couontry key  
        server_dict[country] = location_list

    return server_dict

def get_countries_locations(output):
    """Returns the country and a list of locations of that country"""
    location_list = []
    country = None
    output = output.split('\n')             # Remove new line
    output = output[2:]                     # Remove decoration

    for server in output:
        server = server.split('\t')
        server = list(filter(None, server))       # Remove blank items
        if server:
            server = parse_ls_server_item(server)
        # Check for new country
        #if len(server) == 4 or len(server) == 3 and server[2] != "Y":
            if len(location_list) is not 0:
                if (server.country) != location_list[-1].country:
                    # New country
                    # return the country and its list of locations
                    #country = country.split('(')[0]
                    yield location_list[-1].country, location_list
                    # Start a new list
                    location_list = []
                    # Add the location to the list
                    location_list.append(server)
                    # Set new current country
                    country = server.country
                else:
                    # FIX - Why is this needed?
                    location_list.append(server)      # Add location

            else:
                # The first location from output
                location_list.append(server)
                # Set current country
                country = server.country

def parse_ls_server_item(stream):
    """ Takes a list from the output of expressvpn.ls
        and parses it to create a Server object
    """
    alias = stream[0]
    stream = stream[1:]
    recommended = False

    if stream[-1] is "Y":
        recommended = True
        if len(stream) is 3:
            country, location = parse_location(stream[1])
        else:
            country, location = parse_location(stream[0])
    else:
        if len(stream) is 2:
            country, location = parse_location(stream[1])
        else:
            country, location = parse_location(stream[0])

    return Server(alias, country, location, recommended)

def parse_status(stream):
    stream = stream.split(None, 2)
    stream = stream[2].strip('\n')
    country, location = parse_location(stream)
    return Server(None, country, location, None)

def parse_location(stream):
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