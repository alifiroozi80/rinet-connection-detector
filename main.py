import os
import time
import schedule
from rinet_detector import RinetDetector


RINET_LOG_FILE_ABSOLUTE_PATH = '/Users/ali/Desktop/rinet/1.log'
EMAIL_RECEIVER = 'alifiroozizamani@gmail.com'
MAX_CONNECTIONS = 2


def job() -> None:
    """
    This function is called every 1 Minute
    - Read the log file
    - Detect the IP addresses and their associated Port numbers
    - Delete the log file contents in order to prevent disk pressure
    """
    connected_users = detector.read_log_file()
    detector.detect(connected_users=connected_users)
    detector.delete_log_file()


if __name__ == '__main__':
    detector = RinetDetector(
        rinet_log_path=RINET_LOG_FILE_ABSOLUTE_PATH,
        email_receiver=EMAIL_RECEIVER,
        max_connections=MAX_CONNECTIONS,
        email=os.getenv('EMAIL'),
        password=os.getenv('PASSWORD')
    )

    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
