

class Selector:
    server_selected = None

    def __init__(self, express):
        self.express = express
        if self.express.current_server != None:
            self.server_selected = self.express.current_server
        elif self.express.last_server != None:
            self.server_selected = self.express.last_server

    def get_server_text(self):
        return self.server_selected.country + " - " + self.server_selected.location
