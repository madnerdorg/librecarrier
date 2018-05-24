import argparse
import _cffi_backend # Need for pyinstaller
from argon2 import PasswordHasher

# Source: https://pypi.python.org/pypi/argon2_cffi
parser = argparse.ArgumentParser(description="Generate an hash from a password")
parser.add_argument("--password", default=False, help="Password to hash")
args = vars(parser.parse_args())

if args["password"] is False:
    password = raw_input('Enter your password:')
else:
    password = args["password"]

ph = PasswordHasher()
pass_hash = ph.hash(password)
print("password_hash = " + pass_hash)


