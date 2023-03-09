import smtplib
import os
from user_names import users


class RinetDetecter:
    def __init__(self, rinet_log_path: str, email_receiver: str):
        self.USER = []
        self.ALL = []
        self.EMAIL = os.getenv("EMAIL")
        self.PASSWORD = os.getenv("PASSWORD")
        self.RINET_LOG_PATH = rinet_log_path
        self.EMAIL_RECEIVER = email_receiver

    def send_emil(self, name: str, port: str, custom_message:str="") -> None:
        """
        This function sends notifies the Admin with Email
        """
        if custom_message != "":
            email_message = custom_message
        else:
            email_message = f"Subject:VPN\n\nHello\n User: {name}: {port} has reached the limits!"

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.EMAIL, password=self.PASSWORD)
            connection.sendmail(
                from_addr=self.EMAIL,
                to_addrs=self.EMAIL_RECEIVER,
                msg=email_message
            )
        return None


    def read_log_file(self) -> list:
        """
        This function read and simplify the Log file to a list
        """
        try:
            with open(self.RINET_LOG_PATH, mode="r") as f:
                content = f.readlines()
                for x in content:
                    try:
                        ip = x.split(" ")[0]
                        port = x.split(" ")[7].split("/")[3]
                        # print(f'{x.split(" ")[0]}:{x.split(" ")[7].split("/")[3]}')
                    except IndexError as e:
                        print(f"Do something with {e}")
                    else:
                        self.USER.append(port)
                        self.USER.append(ip)
        except Exception as e:
            self.send_emil(name=" ", port=" ", custom_message=f"Subject:Script crash\n\nHello\n The Script ran into an error:\n {e}")
        finally:
            return self.USER
        
    def delete_log_file(self) -> None:
        """
        Delete the content of the log file to prevent it from being a disk pressure
        """
        try:
            with open(self.RINET_LOG_PATH, mode='r+') as f:
                    f.truncate(0)
        except Exception as e:
            self.send_emil(name=" ", port=" ", custom_message=f"Subject:Script crash\n\nHello\n The Script ran into an error:\n {e}")
        finally:
            return None

    def detecte(self) -> None:
        """
        This function detects if a user connected with more than two different IP addresses
        """
        for k, v in users.items():
            if str(v) in self.USER:
                self.ALL.clear()
                indexes = [i for i, x in enumerate(self.USER) if x == str(v)]
                for ind in indexes:
                    self.ALL.append(self.USER[ind + 1])
                if len(set(self.ALL)) > 2:
                    # print(set(self.ALL))
                    # print(k, v)
                    self.send_emil(name=k, port=v)
        return None
