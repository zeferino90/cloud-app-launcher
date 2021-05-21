from abc import ABC


class FrontendPort(ABC):
    def __init__(self):
        """
        Constructor of the frontend port
        """
        pass

    def add_launch_app_callback(self, callback):
        """
        Add the callback callled for launching an app
        :param callback: method
        :return: None
        """
        raise NotImplementedError

    def call_launch_app_callback(self, app_name, **kwargs):
        """
        Call the launch app callback
        :type app_name: str
        :returns response: dict
        """
        raise NotImplementedError

    def add_get_launch_statu_callback(self, callback):
        """
        Add the callback called for getting the launch status
        :param callback: method
        :return: None
        """
        raise NotImplementedError

    def call_get_launch_status_callback(self, launch_id):
        """
        call the get launch status callback
        :type launch_id: int
        :returns response: dict
        """
        raise NotImplementedError
