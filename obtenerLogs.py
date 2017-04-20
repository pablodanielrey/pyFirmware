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
dbname = sys.argv[2]
dbuser = sys.argv[3]
dbpass = sys.argv[4]

print('Obteniendo los logs de  {}'.format(device))

zk = ZkSoftware(device, 80)
logs = zk.getAttLog('ALL')


if len(logs) <= 0:
    sys.exit(0)

users = {}

con = psycopg2.connect(host='127.0.0.1', dbname=dbname, user=dbuser, password=dbpass)
try:
    cur = con.cursor()
    try:
        cur.execute('select id, dni from users')
        if cur.rowcount > 0:
            for u in cur:
                users[u[1]] = u[0]

        inserted = 0

        for l in logs:
            dni = l['PIN']
            log = l['DateTime']
            if dni not in users:
                print('No existe {} lo creo'.format(dni))
                users[dni] = str(uuid.uuid4())
                cur.execute('insert into users (id, dni, name) values (%s,%s,%s)', (users[dni], dni, 'generado'))

            r = users[dni]
            if r:
                cur.execute('select id from attlog where person_id = %s and date = %s', (r,log))
                if cur.rowcount <= 0:
                    cur.execute('insert into attlog (id, device_id, person_id, verifymode, inoutmode, date) values (%s,%s,%s,%s,%s,%s)',
                        (str(uuid.uuid4()),'1c5c90a3-2873-4b8f-9931-faca5808e932', r, 0, 0, log))
                    inserted = inserted + 1

        con.commit()

        if inserted <= 0:
            """ si no se inserto a nadie nuevo entonces si el reloj no tiene mas logs los elimino """
            logs2 = zk.getAttLog('ALL')
            if (len(logs2) == len(logs)):
                zk.clearAttLogs()

    finally:
        cur.close()

finally:
    con.close()
