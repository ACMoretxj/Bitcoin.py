# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib.parse import urlparse as parse


class Node:

    def __init__(self, node_url):
        """
        initialize a network node, extract
        netloc or path from appointed url
        :param node_url: appointed url
        """
        self.node_url = node_url
        parsed_url = parse(node_url)
        if parsed_url.netloc:
            self.url = parsed_url.netloc
        elif parsed_url.path:
            self.url = parsed_url.path
        else:
            raise ValueError('Invalid URL')


class NodeManager:

    def __init__(self):
        """
        initialize the node manager
        """
        self.nodes = []

    def register(self, node):
        self.nodes.append(node)
