# -*- coding: utf-8 -*-
import ldap
import ldap.modlist as modlist
import uuid
import sys
import psycopg2

user = sys.argv[1]
passw = sys.argv[2]
dbname = sys.argv[3]
dbuser = sys.argv[4]
dbpass = sys.argv[5]

l = ldap.initialize("ldap://127.0.0.1:389")
l.protocol_version = ldap.VERSION3
l.simple_bind_s(user,passw);

con = psycopg2.connect(host='127.0.0.1', dbname=dbname, user=dbuser, password=dbpass)
try:
        result = l.search_s("ou=people,dc=econo",ldap.SCOPE_SUBTREE,"(x-dcsys-dni=*)",["uid","mail","x-dcsys-dni","sn","givenName","userPassword","x-dcsys-uuid","objectClass","l","co","x-dcsys-gender","telephoneNumber"])
        if result == None:
                exit(1)

        cur = con.cursor()
        try:
            cur.execute("""create table if not exists users (
                 id varchar not null primary key,
                 name varchar,
                 lastname varchar,
                 telephone varchar,
                 dni varchar,
                 gender varchar,
                 country varchar,
                 city varchar,
                 notes varchar,
                 email varchar,
                 upassword varchar
            )""");

            for dn,g in result:
                    userid = g['x-dcsys-uuid'][0]
                    dni = g['x-dcsys-dni'][0]
                    name = None
                    lastname = None
                    city = None
                    country = None
                    email = None
                    upassword = None
                    gender = None

                    if 'givenName' in g:
                        name = g['givenName'][0]

                    if 'sn' in g:
                        #print g['sn']
                        lastname = g['sn'][0]

                    if 'mail' in g:
                        email = g['mail'][0]

                    if 'userPassword' in g:
                        upassword = g['userPassword'][0]

                    if 'gender' in g:
                        gender = g['gender'][0]

                    if 'telephoneNumber' in g:
                        telephone = g['telephoneNumber'][0]

                    cur.execute('insert into users (id,dni,name,lastname,city,country,gender,telephone,email,upassword) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (userid,dni,name,lastname,city,country,gender,telephone,email,upassword))
                    con.commit()
        finally:
            cur.close()

except ldap.LDAPError, e:
        print e

finally:
        con.close();
        l.unbind_s()
