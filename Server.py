class Server:
    alias = ""
    country = ""
    location = ""
    recommended = False
    number = None

    def __init__(self, alias, country, location, recommended):
        self.alias = alias
        self.country = country
        self.location = location
        self.recommended = recommended