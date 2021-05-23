import os

SERVER_PORT = os.getenv('LAUNCHER_SERVER_PORT') if os.getenv('LAUNCHER_SERVER_PORT') is not None else 8080
