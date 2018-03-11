import os
import datetime

import subprocess

from netbios import byte_to_int

if __name__ == "__main__":
    label = subprocess.check_output(["git", "describe", "--always"])  # current git hash
    print(label)
    print(labe)