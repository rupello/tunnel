#!/usr/bin/env python
"""
    sets up a bi-directional ssh tunnel forwarded to local
    ports at both ends

    ssh key based login needs to be setup already

    to run every minute, add using 'crontab -e'
    */1 * * * * tunnel-out.py >> ~/.logs/tunnel.log
"""
import subprocess

REMOTE_USER = 'woozle'           # account on the remote (public) server
REMOTE_IP   = '100.100.100.100'  # IP of the server (public ip)
REMOTE_PORT = '10024'            # port we will forward on the server back to me, "ssh -p 10022 rupello@localhost'
LOCAL_PORT  = '19924'            # port we will forward here as our 'canary' tunnel

def create_tunnel():
    try:
        subprocess.check_call(['/usr/bin/ssh','-f','-N',
                               '-R','{}:localhost:22'.format(REMOTE_PORT),     # reverse tunnel from server back to me
                               '-L','{}:{}:22'.format(LOCAL_PORT, REMOTE_IP),  # local port forward 'canary' tunnel
                               '{}@{}'.format(REMOTE_USER,REMOTE_IP)])         # the user@server we are connecting to
        print('tunnel created OK')
    except:
        print('error creating tunnel')

def check_extant_tunnel():
    try:
        # try executing a task over the tunnel
        out = subprocess.check_output(['/usr/bin/ssh','-p',LOCAL_PORT,'{}@localhost'.format(REMOTE_USER),'ls > /dev/null'])
        print(out)
        return True
    except:
        return False

if __name__ == '__main__':
    print('checking for existing tunnel...')
    if not check_extant_tunnel():
        print('creating new tunnels...')
        create_tunnel()
    else:
        print('tunnel exists already')


