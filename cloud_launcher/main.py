from cloud_handler.adapters import AwsEc2AMILauncher
from frontend_handlers.adapters import ApiFrontendAdapter
from launcher import Launcher

if __name__ == '__main__':
    aws_ec2_ami_adapter = AwsEc2AMILauncher()
    launcher = Launcher(aws_ec2_ami_adapter)
    api = ApiFrontendAdapter()
    api.add_launch_app_callback(launcher.launch_app)
    api.add_get_launch_status_callback(launcher.check_app_launch)
    api.run()


