# -*- coding: utf-8 -*-
import logging
import sys
from zksoftware.zkSoftware import ZkSoftware

logging.getLogger().setLevel(logging.INFO)
device = sys.argv[1]

zk = ZkSoftware(device, 80)
print(zk.refreshDb())
