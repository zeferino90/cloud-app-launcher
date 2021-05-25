# App launcher

For using this App launcher you require python3. I only tried version 3.7.

If you want to run the application and the test suite install requirements-dev.txt. If you only want to run the 
application install requirements.txt instead.
To execute the app run from the root of the project.
> python cloud_launcher/main.py

Tu run the test suite run from cloud_launcher directory the following command:
>python -m pytest ../test/

There are some environment variables needed to run it:

(Optional) LAUNCHER_SERVER_PORT: Specify a custom port for the API, default to 8080

(Required) AWS_ACCESS_KEY: Access key needed for launching the app to aws

(Required) AWS_SECRET_ACCESS_KEY: secret key needed for launching the app to aws

Inside the project there's a dockerfile. Can build and run the container with the following commands.

Building:
>docker build . -t cloud-app-launcher:1.0

Running the app:
>docker run -e AWS_ACCESS_KEY="YOUR_ACCES_KEY" -e AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY" -p 8080:8080 cloud-app-launcher:1.0
