import os
import sqlite3
import time
import sys

def disableAccount(user_port):
    conn = sqlite3.connect('/root/x-ui/db/x-ui.db') 
    conn.execute(f"update inbounds set enable = 0 where port={user_port}")
    conn.commit()
    conn.close()
    time.sleep(2)
    os.popen("docker container restart x-ui")
    time.sleep(3)

disableAccount(sys.argv[1])

