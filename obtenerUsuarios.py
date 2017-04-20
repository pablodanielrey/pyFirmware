# -*- coding: utf-8 -*-

import uuid
import pprint
import logging
import csv
import sys
import psycopg2
from zksoftware.zkSoftware import ZkSoftware

logging.getLogger().setLevel(logging.INFO)

device = sys.argv[1]

zk = ZkSoftware(device, 80)
users = zk.getUserInfo()

for u in users:
    print(u)

templates = zk.getUserTemplate()
for t in templates:
    print(t)
