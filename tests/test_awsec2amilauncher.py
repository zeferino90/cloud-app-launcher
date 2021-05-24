import pytest
from unittest.mock import patch, MagicMock, ANY

from cloud_handler.adapters import AwsEc2AMILauncher


def test_awsec2amilauncher_constructor():
    aws_ec2_ami_launcher = AwsEc2AMILauncher()


def test_launch_app__runs_ok():
    aws_ec2_ami_launcher = AwsEc2AMILauncher()
    aws_ec2_ami_launcher.ec2_client = MagicMock()
    app = {"app_name": "ghost"}
    response = MagicMock()
    aws_ec2_ami_launcher.ec2_client.run_instances.return_value = response
    assert response["Instances"][0]["InstanceId"] == aws_ec2_ami_launcher.launch_app(app)
    image_id = aws_ec2_ami_launcher.REGISTERED_AMIS.get('ghost')
    aws_ec2_ami_launcher.ec2_client.run_instances.assert_called_with(ImageId=image_id,
                                                                  MinCount=ANY,
                                                                  MaxCount=ANY,
                                                                  InstanceType=ANY,
                                                                  KeyName=ANY)


def test_launch_app__exception_run_instances():
    aws_ec2_ami_launcher = AwsEc2AMILauncher()
    aws_ec2_ami_launcher.ec2_client = MagicMock()
    app = {"app_name": "ghost"}
    response = MagicMock()
    aws_ec2_ami_launcher.ec2_client.run_instances.side_effect = Exception
    with pytest.raises(Exception):
        aws_ec2_ami_launcher.launch_app(app)


def test_launch_app__no_image_id():
    aws_ec2_ami_launcher = AwsEc2AMILauncher()
    aws_ec2_ami_launcher.ec2_client = MagicMock()
    app = {"app_name": "app_not_known"}
    assert aws_ec2_ami_launcher.launch_app(app) is None
    aws_ec2_ami_launcher.ec2_client.run_instances.assert_not_called()


def test_get_launch_returns_pending():
    aws_ec2_ami_launcher = AwsEc2AMILauncher()
    aws_ec2_ami_launcher.ec2_client = MagicMock()
    instance = {"State": {"Name": "pending"}}
    reservation = [{"Instances": [instance]}]
    response = MagicMock()
    response.get.return_value = reservation
    aws_ec2_ami_launcher.ec2_client.describe_instances.return_value = response
    assert aws_ec2_ami_launcher.get_launch_status(MagicMock()) == {"status": "pending"}


def test_get_launch_returns_running():
    aws_ec2_ami_launcher = AwsEc2AMILauncher()
    aws_ec2_ami_launcher.ec2_client = MagicMock()
    instance = {"State": {"Name": "running"},
                "PublicDnsName" : '1.2.3.4'}
    reservation = [{"Instances": [instance]}]
    response = MagicMock()
    response.get.return_value = reservation
    aws_ec2_ami_launcher.ec2_client.describe_instances.return_value = response
    assert aws_ec2_ami_launcher.get_launch_status(MagicMock()) == {"status": "running", "url": "http://1.2.3.4"}


def test_get_launch_exception():
    aws_ec2_ami_launcher = AwsEc2AMILauncher()
    aws_ec2_ami_launcher.ec2_client = MagicMock()
    aws_ec2_ami_launcher.ec2_client.describe_instaces.side_effect = Exception
    with pytest.raises(Exception):
        assert aws_ec2_ami_launcher.get_launch_status(MagicMock())
