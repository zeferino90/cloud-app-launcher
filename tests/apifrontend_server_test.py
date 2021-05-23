import random

from frontend_handlers.adapters import ApiFrontendAdapter


def stub_launch_app_cb(app_name, app_properties):
    return {"launch_id": random.randint(0, 100)}


def stub_get_launch_status_cb(launch_id):
    option = random.randint(0, 2)
    if option == 0:
        return {"launch-id": launch_id, "state": "in-progress"}
    elif option == 1:
        return {"launch-id": launch_id, "state": "finished"}
    else:
        return {"launch-id": launch_id, "state": "failed"}


if __name__ == '__main__':
    api = ApiFrontendAdapter()
    api.add_launch_app_callback(stub_launch_app_cb)
    api.add_get_launch_status_callback(stub_get_launch_status_cb)
    api.run()
