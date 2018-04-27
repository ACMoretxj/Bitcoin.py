# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from urllib.parse import urlparse as parse

import time

from utils import singleton


class Peer:

    def __init__(self, peer_url):
        """
        initialize a network node, extract
        netloc or path from appointed url
        :param peer_url: appointed url
        """
        self.node_url = peer_url
        parsed_url = parse(peer_url)
        if parsed_url.netloc:
            self.url = parsed_url.netloc
        elif parsed_url.path:
            self.url = parsed_url.path
        else:
            raise ValueError('Invalid URL')

    def send(self, data):
        pass


@singleton
class PeerManager:

    def __init__(self):
        self.peers = []

    def register(self, peer_url):
        self.nodes.append(Peer(peer_url))

    def notify_all_peers(self, data):
        for peer in self.peers:
            self.notify_peer(data, peer)

    def notify_peer(self, data, peer=None):
        peer = peer or random.choice(self.peers)
        tries_left = 3
        while tries_left:
            # noinspection PyBroadException
            try: peer.send(data)
            except Exception:
                tries_left -= 1
                time.sleep(2)
            else: return None
        # the peer chosen is dead
        self.peers.remove(peer)
