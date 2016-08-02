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

def print_servers(server_list):
    print('--------------------------')
    for server in server_list:
        print(server['alias'])
        print(server['country'])
        print(server['location'])
        print(server['recommended'])

def parse_server_list(output):
    #TODO

    return server_list

def ls():
    output = subprocess.check_output(["expressvpn", "list"]).split()
    server_list = parse_server_list(output)
    return server_list


if __name__ == "__main__":
    #example of usage
    if status() == False:
        connect()
    server_list = ls()
    print_servers(server_list)
