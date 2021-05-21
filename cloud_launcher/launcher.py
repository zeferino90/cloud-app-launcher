import logging

from entities import App, AppPropertiesError


class Launcher:
    def __init__(self, cloud_adapter):
        self.cloud_adapter = cloud_adapter  # This could be a list of cloud adapters to support multiple cloud launch

    def launch_app(self, app_name, **kwargs):
        """
        This use case is for launching an app with all of its arguments to a cloud provider
        :param app_name: App
        :type kwargs: dict
        :returns dict
        """
        try:
            app = App(app_name, kwargs)
            # TODO: check parameters
        except AppPropertiesError:  # TODO: Future feature
            msg = "Bad applications properties"
            logging.error(msg)
            return {'error_msg': msg}
        try:
            launch_id = self.cloud_adapter.launch_app(app)
        except Exception as e:
            msg = f"Exception while launching the app {app.name}"
            logging.exception(msg)
            return {'error_msg': msg}
        return {"launch_id": launch_id}

    def check_app_launch(self, launch_id):
        """
        This use case get the status of a specific launch
        :type launch_id: int
        :returns: dict
        """
        try:
            return self.cloud_adapter.get_launch_status(launch_id)
        except Exception as e:
            msg = f"Exception getting launch status for {launch_id}"
            logging.exception(msg)
            return {'error_msg': msg}
