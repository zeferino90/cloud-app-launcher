class App:
    def __init__(self, name, properties):
        """
        Object representing and app that could we launched and a dictionary with the properties needed for that launch
        :type name: str
        :type properties: dict
        """
        self.name = name
        self.properties = properties


class AppPropertiesError(Exception):
    """
    Exception raised when the app properties are not correct
    """
