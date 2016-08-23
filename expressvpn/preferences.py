
class Preferences:
    auto_connect = False
    prefered_protocol = ""
    send_diagnostics = True

    def __init__(self, auto_connect, prefered_protocol, send_diagnostics):
        self.auto_connect = auto_connect
        self.prefered_protocol = prefered_protocol
        self.send_diagnostics = send_diagnostics
