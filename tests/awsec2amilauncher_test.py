from time import sleep

from cloud_handler.adapters import AwsEc2AMILauncher
from entities import App

if __name__ == '__main__':
    ec2_ami_launcher = AwsEc2AMILauncher()
    app = App('ghost', None)
    launch_id = ec2_ami_launcher.launch_app(app.as_dict())
    print(launch_id)
    sleep(5)
    while True:
        response = ec2_ami_launcher.get_launch_status(launch_id)
        print(response)
        if response['status'] == 'running':
            break
        sleep(4)

