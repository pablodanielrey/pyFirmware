# -*- coding: utf-8 -*-
import logging
import sys
from zksoftware.zkSoftware import ZkSoftware

logging.getLogger().setLevel(logging.INFO)

if len(sys.argv) <= 3:
    print('no se ejecuta')
    sys.exit(1)

deviceFrom = sys.argv[1]
deviceTo = sys.argv[2]

zkFrom = ZkSoftware(deviceFrom, 80)
zkTo = ZkSoftware(deviceTo, 80)

users = zkFrom.getUserInfo()
for u in users:
    try:
        print('Copiando : {}'.format(u['PIN2']))
        r = zkTo.setUserInfo(
            u['PIN2'],
            u['Password'],
            u['Group'],
            u['Privilege'],
            u['Card']
        )
        print(r)

        try:
            ts = zkFrom.getUserTemplate(u['PIN2'])
            if 'PIN' in ts:
                t = ts
                print(zkTo.setUserTemplate(t['PIN'], t['FingerID'], t['Size'], t['Valid'], t['Template']))
            else:
                for t in ts:
                    print(zkTo.setUserTemplate(t['PIN'], t['FingerID'], t['Size'], t['Valid'], t['Template']))
                    
        except Exception as e2:
            print(e2)

    except Exception as e:
        print(e)

zkTo.refreshDb()
