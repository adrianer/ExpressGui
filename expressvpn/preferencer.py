
class Preferencer:
    auto_connect = False
    prefered_protocol = ""
    send_diagnostics = True
    protocols = ["udp", "auto", "tcp"]

    def __init__(self, auto_connect, prefered_protocol, send_diagnostics):
        self.auto_connect = auto_connect
        self.prefered_protocol = prefered_protocol
        self.send_diagnostics = send_diagnostics
