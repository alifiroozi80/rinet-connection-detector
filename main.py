import schedule
import time
from rinet_detecter import RinetDetecter

RINET_LOG_FILE_FULL_PATH = "/Users/ali/Desktop/rinet/1.log"
EMAIL_RECEIVER = "alifiroozizamani@gmail.com"

def job(path: str) -> None:
    """This function is called every 1 Minute"""
    x = RinetDetecter(rinet_log_path=path, email_receiver=EMAIL_RECEIVER)
    x.read_log_file() # Read the log file
    x.detecte() # Detect the IP addresses and their associated Port numbers
    x.delete_log_file() # Delete the log file contents in order to prevent Disk pressure
    return None

schedule.every(1).minutes.do(job, path=RINET_LOG_FILE_FULL_PATH)

while True:
    schedule.run_pending()
    time.sleep(1)