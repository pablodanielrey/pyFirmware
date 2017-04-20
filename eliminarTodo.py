# -*- coding: utf-8 -*-
import logging
import sys
from zksoftware.zkSoftware import ZkSoftware

logging.getLogger().setLevel(logging.INFO)

if len(sys.argv) <= 3:
    print('no se ejecuta')
    sys.exit(1)

device = sys.argv[1]
y = sys.argv[2]

if y != 'y':
    print('no se ejecuta')
    sys.exit(1)

zk = ZkSoftware(device, 80)
zk.clearAttLogs()
zk.clearUsers()
