from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def main():
        # Instantiate a dummy authorizer for managing 'virtual' users
        authorizer = DummyAuthorizer()

        # Add a user with username, password, home directory, and permissions
        # 'elradfmw' grants full read/write access (list, enable, read, delete, ftp, modify, write)
        authorizer.add_user("rumi", "accordingtoallknownlawsofaviationthereisnowayabeeshouldbeabletofly", "./ftp", perm="lr")

        # Optionally, add an anonymous user with limited access
        # authorizer.add_anonymous("/home/myuser/ftp_public")

        # Instantiate FTP handler and set the authorizer
        handler = FTPHandler
        handler.authorizer = authorizer
        handler.passive_ports = range(42300, 42500)

        # Define the server address and port
        address = ("0.0.0.0", 21)  # Listen on all available interfaces, port 2121

        # Instantiate the FTP server
        server = FTPServer(address, handler)

        # Set a maximum number of concurrent connections
        server.max_cons = 256
        server.max_cons_per_ip = 5

        # Start the FTP server
        print(f"Starting FTP server on {address[0]}:{address[1]}...")
        server.serve_forever()

if __name__ == "__main__":
        main()
