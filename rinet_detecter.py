import os
import smtplib
from user_names import users


class RinetDetector:
    def __init__(self, rinet_log_path: str, email_receiver: str, email: str, password: str, max_connections: int):
        self.email = email
        self.password = password
        self.rinet_log_path = rinet_log_path
        self.email_receiver = email_receiver
        self.max_connections = max_connections

    def read_log_file(self) -> list[tuple[str, str]]:
        """
        This function read and simplify the log file to a list
        """
        connected_users = list()
        try:
            with open(self.rinet_log_path) as f:
                for line in f.readlines():
                    try:
                        ip = line.split(' ')[0]
                        port = line.split(' ')[7].split('/')[3]
                    except IndexError as e:
                        self._send_error_mail(e)
                    else:
                        connected_users.append((ip, port))

        except Exception as e:
            self._send_error_mail(e)
        return connected_users

    def delete_log_file(self) -> None:
        """
        Delete the content of the log file to prevent it from being a disk pressure
        """
        try:
            with open(self.rinet_log_path, mode='r+') as f:
                f.truncate(0)
        except Exception as e:
            self._send_error_mail(e)

    def detect(self, connected_users: list[tuple[str, str]]) -> None:
        """
        This function detects if a user connected with more than "int(max_connections)" different IP addresses
        """

        for user, port in users.items():
            connected_ips = set()
            for connected_ip, connected_port in connected_users:
                if str(port) == connected_port:
                    connected_ips.add(connected_ip)

            if len(connected_ips) > self.max_connections:
                self._ban_user(user=user, port=port, connected_ips=connected_ips)

    def _ban_user(self, user: str, port: int, connected_ips: set) -> None:
        self._send_email(name=user, port=port, ips=connected_ips)
        try:
            os.system(f"ansible-playbook -i inventory.ini playbook.yaml --extra-vars 'xxx={user}'")
        except Exception as e:
            self._send_error_mail(e)

    def _send_mail(self, message: str) -> None:
        """
        This function sends notifies the Admin with Email
        """

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.password)
            connection.sendmail(
                from_addr=self.email,
                to_addrs=self.email_receiver,
                msg=message
            )

    def _send_email(self, *, name: str, port: int, ips: set) -> None:
        """
        This function create notification message and send it to the Admin
        """
        message = f"Subject:VPN\n\nHello\n User: {name}: {port} has reached the limits!\nSources: {ips}"
        self._send_mail(message)

    def _send_error_mail(self, error: str | Exception) -> None:
        """
        This function create error message and send it to the Admin
        """
        message = f"Subject:Script crash\n\nHello\n The Script ran into an error:\n {error}"
        self._send_mail(message)
