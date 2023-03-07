a simple utility to create a vpn server on any given machine in 1 minute

```
# python3 masavs.py --help
usage: masavs.py [-h] --ip IP [--port PORT] --ssh_user SSH_USER [--ssh_passwd SSH_PASSWD] [--ssh_key SSH_KEY] [--ssh_key_phrase SSH_KEY_PHRASE]

options:
  -h, --help            show this help message and exit
  --ip IP               the ip of the server
  --port PORT           the port of ssh (defaut=22)
  --ssh_user SSH_USER   ssh username to use
  --ssh_passwd SSH_PASSWD
                        ssh password to use
  --ssh_key SSH_KEY     ssh private key to use instead of password
  --ssh_key_phrase SSH_KEY_PHRASE
                        ssh private key passphrase to use with (--ssh_key)

(M)ake (A)ny (S)erver (A) (V)pn (S)erver
```

- Just in Case

	- *this script creates a vpn server from only linux servers*