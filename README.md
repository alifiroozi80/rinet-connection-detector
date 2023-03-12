<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">Rinetd Connection Detector</h3>

  <p align="center">
    Limit V2ray user while they are behind another Server (Rinetd)
    <br />
    <br />
    <a href="https://github.com/alifiroozi80/rinet-connection-detecter/issues">Report Bug</a>
    ·
    <a href="https://github.com/alifiroozi80/rinet-connection-detecter/issues">Request Feature</a>
  </p>
</div>

---

### What is Rinetd?
[Rinetd](https://github.com/samhocevar/rinetd) efficiently redirects connections from one IP address/port combination to another. It is useful when operating virtual servers, firewalls, and the like.

It is a fantastic tool, especially in this scenario:

You have two servers.

One is the leading VPN server (located in France, for instance), and the other is in another location (e.g., Iran).

You want to connect the users to the Iran Server and redirect them to your France VPN server.

To achieve this, on France Server, you can install whatever VPN you want (V2ray, ocServe, etc.), and on the Iran Server, install Rinetd, and you are good to go.

---

### UseCase
Let's say you successfully deployed this setup.

Now you want to Limit users to two users at the same time.

If you are using V2ray, there is already a [script](https://github.com/net-pioneer/v2ray-connection-limiter/blob/main/main.py) does this.

But this script doesn't work with this setup because we redirect all traffic from Iran Server, and the VPN server (France) now sees only our Iran server's IP address.

So, we should monitor the users from the Iran Server, not the VPN Server (France).

This simple Python Script do this!

---

### How is this script working?

It reads your log file and sees if one particular port is used by more than X Ip addresses. (The X is the number that you'll define).

Just be aware of the following:

First) The log file should be in web-server style format.
For this, your rinetd config file should be like this:

```shell
# logging information
logfile /var/log/rinetd.log

# uncomment the following line if you want web-server style logfile format
logcommon
```

Sample log file format:

```shell
8.8.8.8 - - [09/Mar/2023:07:27:50  +0000] "GET /rinetd-services/0.0.0.0/3000/1.1.1.1/3000/done-remote-closed HTTP/1.0" 200 203 - - - 131
8.8.4.4 - - [09/Mar/2023:07:27:51  +0000] "GET /rinetd-services/0.0.0.0/3001/1.1.1.1/3001/opened HTTP/1.0" 200 0 - - - 0
```

Second) You should enter your Usernames with their specified ports in the `user_names.py` file with the dictionary type.

---

### Install Guide:
1) install python.
2) `pip3 install -r requirements.txt`
3) put it on background => `nohup python3 main.py &` (without background process : `python3 main.py`)

---

### Prevention

You can disable the user with the `prevent` folder.

In there, you see three files: 
1) `main.py`: Keep this file on the VPN server that hosts V2ray (France).
2) `inventory.ini`: edit this file. Keep this file with other parent files.
3) `playbook.yaml`: edit this file to replace the `db` path and the `main.py` script on the  VPN server. Keep this file with other parent files.

---

<!-- ROADMAP -->

## Roadmap

- [x] Add real-world examples
- [x] Add exam tips
- [ ] Add Dockerfile and Docker Compose examples
- [x] Automatically disabled user (With Ansible)

See the [open issues](https://github.com/alifiroozi80/rinet-connection-detecter/issues) for a complete list of proposed features (and known
issues).

---

<!-- CONTRIBUTING -->

## Contributing

Any contributions you make are **greatly appreciated**.

If you have a suggestion to improve this, please fork the repo and create a pull request. You can also open an issue
with the tag "enhancement."

1) Fork the Project
2) Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3) Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4) Push to the Branch (`git push origin feature/AmazingFeature`)
5) Open a Pull Request

---

<!-- LICENSE -->

## License

The license is under the MIT License. See [LICENSE](https://github.com/alifiroozi80/rinet-connection-detecter/blob/main/LICENSE) for more
information.

---

## ❤ Show your support

Give a ⭐️ if this project helped you!
