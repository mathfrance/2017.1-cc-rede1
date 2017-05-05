#!/usr/bin/python
# coding=utf-8

import sys

from peergui import PeerGui


def main():
    if len(sys.argv) < 4:
        print "Syntax: %s server-port max-peers peer-ip:port" % sys.argv[0]
        sys.exit(-1)

    server_port = int(sys.argv[1])
    max_peers = sys.argv[2]
    peer_id = sys.argv[3]
    app = PeerGui(tracker_peer=peer_id, max_peers=max_peers, server_port=server_port)
    app.mainloop()
    pass


# setup and run app
if __name__ == '__main__':
    main()
