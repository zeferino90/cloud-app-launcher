from abc import ABC


class CloudLauncherPort(ABC):
    def __init__(self):
        """
        Initialization of the cloud launcher
        """
        pass

    def launch_app(self, app):
        """
        Launch the app on the cloud and return a launch_id to monitor the launch
        :type app: App
        :returns response: dict
        """
        raise NotImplementedError

    def get_launch_status(self, launch_id):
        """
        Get the status information about the launch_id
        :type launch_id: int
        """
        raise NotImplementedError
