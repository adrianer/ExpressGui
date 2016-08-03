"""module to interact with expressvpn"""
import subprocess


def status():
    stream = subprocess.check_output(["expressvpn", "status"])
    if "Not connected" in stream:
        return False
    else:
        return True
        
def connect():
    stream = subprocess.call(["expressvpn", "connect"])
    if stream == 0 or 1:
        #connected
        return True

def disconnect():
    stream = subprocess.call(["expressvpn", "disconnect"])
    if stream == 0 or 1:
        #disconnected
        return True

def print_servers(server_dict):
    print('--------------------------')
    for country in server_dict['countries']:
        print("Country = " + country)
        for location in server_dict[country]:
            print(location)

def parse_ls_output(output):
    """returns a dictionary containing a list of countries and a list of locations
        ["countries"] for a list of countries """
    location_list = []
    server_dict = {}
    country = None
    server_dict['countries'] = []
    output = output.split('\n')            
    output = output[2:]                     #Remove decoration
    for server in output:
        server = server.split('\t')
        server = filter(None, server)       #Remove blank items
        if len(server) == 4 or len(server) == 3 and server[2] != "Y":  #check for new country
            #New country
            if country != None:                      
                server_dict['countries'].append(country)        #Add the current country to the server list
                server_dict[country] = location_list            #Add the list of server locations to the country key
                location_list = []                              #Start a new list
                location_list.append(server[2:])                #Add the location to the list
                country = server[1]                             #Set new current country
            else:
                location_list.append(server[2:])                #The first location from output
                country = server[1]                             #Set current country
        else:
            location_list.append(server[1:])                    #Add location

    return server_dict

def ls():
    output = subprocess.check_output(["expressvpn", "ls"])
    location_list = parse_ls_output(output)
    return location_list


if __name__ == "__main__":
    #example of usage
    if status() == False:
        connect()
    server_dict = ls()
    print_servers(server_dict)
