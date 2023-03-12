import os
import sys
import time
import sqlite3


def disable_account(user_port):
    conn = sqlite3.connect('/root/x-ui/db/x-ui.db') 
    conn.execute(f'update inbounds set enable = 0 where port={user_port}')
    conn.commit()
    conn.close()
    time.sleep(2)
    os.popen('docker container restart x-ui')
    time.sleep(3)


disable_account(sys.argv[1])
