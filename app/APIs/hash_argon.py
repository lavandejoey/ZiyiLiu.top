#!/usr/bin/env python
# hash_argon.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"

# standard library
# 3rd party packages
import argon2
from argon2 import PasswordHasher, Type

# local source
ph = PasswordHasher(
    time_cost=100,  # number of iterations
    memory_cost=1024 * 64,  # Kb, 128Mb
    parallelism=20,  # Defines the number of parallel threads (*changes* the resulting hash value).
    hash_len=120,  # Length of the hash in bytes
    salt_len=8,  # Length of random salt to be generated for each password.
    type=Type.ID  # Argon2_id
)


# Hash the password
def str_hash(raw_passwd: str) -> str:
    return ph.hash(raw_passwd)


# Verify the password
def str_verify(raw_passwd: str, hashed_passwd: str) -> bool:
    try:
        ph.verify(hashed_passwd, raw_passwd)
        return True
    except argon2.exceptions.VerifyMismatchError or argon2.exceptions.VerificationError:
        return False
