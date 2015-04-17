"""
Tools for creating and editing networks, and algorithms for computing their properties.

Classes:
Network  -- a network of nodes
RSTree  -- rooted spanning tree, created from a Network objects
NetworkFactory -- generate classic networks (star, clique, erdos-renyi, etc.)
"""
import random

__all__ = ['Network']

class Network:
    """
    A network of nodes.

    Methods:
    add_node -- add node to the network
    add_link -- add link between two nodes

    Properties:
    nodes -- list of nodes in the network
    node_count -- number of nodes in the network
    link_count -- number of links in the network
    """
    def __init__(self, fromDict=None):
        """Create a network, optionally from a dictionary, else empty.

        Keyword arguments:
        fromDict -- dictionary from which to create the network

        Dictionary format: {node1:{node2:1, node3:1}}
        """
        if fromDict is None:
            self._net = {}
        else:
            self._net = fromDict

    def __len__(self):
        return self.node_count

    def add_node(self, node):
        """Create a new (unconnected) node in the graph."""
        if node not in self._net:
            self._net[node] = {}

    def add_link(self, node1, node2):
        """Make a link between nodes.

        n1 and n2 are created if they did not already exist."""
        if not self.add_node(node1):
            return -1
        if not self.add_node(node2):
            return -1
        self._net[node1][node2] = 1
        self._net[node2][node1] = 1

    def del_link(self, node1, node2):
        """Delete link between nodes"""
        del self._net[node1][node2]
        del self._net[node2][node1]

    def find_neighbors(self, node):
        """Return list of neighbors of node."""
        return [neighbor for neighbor in self._net[node]]

    @property
    def link_count(self):
        """Number of links in the network."""
        return int(sum([sum(self._net[n].values()) for n in self._net]) / 2)

    @property
    def node_count(self):
        """Number of nodes in the network."""
        return len(self._net)

    @property
    def nodes(self):
        """Nodes in the network."""
        return [node for node in self._net]

    # def compute_distances_to_node(self, node):
    #     pass

    # def compute_node_centrality(self, node):
    #     pass

    # def map_ac_naive(self, nodes='all'):
    #     pass

    # def map_ac_split(self, nodes='all'):
    #     pass

    # def compute_node_cc(self, node):
    #     pass

    # def find_shortest_paths_to_node(self, node, algo="floyd-warshall"):
    #     pass

    # def estimate_node_cc(self, node):
    #     pass

    # def estimate_cc(self):
    #     pass


class RSTree:
    """ A rooted spanning tree, created from a Network object.

    Properties
    root
    network
    po_map
    desc_map
    max_po_map
    min_po_map
    bridge_links
    """
    def __init__(self, network, root):
        """ Create a rooted spanning tree from a Network object."""
        self.root = root
        self.network = network
        self._po_map = None
        self._max_po_map = None
        self._desc_map = None
        self._min_po_map = None

        tree = {root:{}}
        marked = [root]
        open_list = [root]

        def add_link(node1, node2, color):
            """Add link to tree."""
            if not node1 in tree:
                tree[node1] = {}
            if not node2 in tree:
                tree[node2] = {}
            tree[node1][node2] = color
            if color == 'red':
                tree[node2][node1] = 'red'

        while open_list != []:
            current = open_list.pop(0)
            neighbors = network.find_neighbors(current)

            for neighbor in neighbors:
                if neighbor not in marked:
                    marked.append(neighbor)
                    open_list.append(neighbor)
                    add_link(current, neighbor, 'green')
                elif neighbor not in tree[current] and current not in tree[neighbor]:
                    add_link(current, neighbor, 'red')
        self._tree = tree

        # @property
        # def po_map(self):
        #     pass

        # @property
        # def desc_map(self):
        #     pass

        # @property
        # def max_po_map(self):
        #     pass

        # @property
        # def min_po_map(self):
        #     pass

        # @property
        # def bridge_links(self):
        #     pass


class NetworkFactory:
    """
    Generates several types of classic networks.

    Methods:
    build_network

    Properties:
    defaults
    """
    def __init__(self, **kwargs):
        """
        Create a network factory with defaults specified by keyword args.

        Optional keyword arguments:
        size -- number of nodes in the graph
        shape -- network type, see below for list of supported types
        p -- probability for random network type
        size_x -- x dimension for grid network type
        size_y -- y dimension for grid network type

        Types of networks:
        star -- one central node, connected to all other nodes
        clique -- all nodes interconnected
        chain --
        ring --
        hypercube --
        grid -- x by y grid of nodes
        random -- each node has probability p of being connected to each other node (Erdos-Renyi)
        """
        self.defaults = {
            'shape': kwargs.get('shape', None),
            'size': kwargs.get('size', None),
            'p': kwargs.get('p', None),
            'size_x': kwargs.get('size_x', None),
            'size_y': kwargs.get('size_y', None)
            }

    def build_network(self, **kwargs):
        """
        Build a network based on defaults. Return a Network object.

        All defaults can be overriden with keyword arguments.
        """
        return Network()

    @staticmethod
    def build_star_network(size):
        """Build a star network. Returns Network object."""
        network = Network()
        for i in range(1, size):
            network.add_link(0, i)
        return network

    @staticmethod
    def build_chain_network(size):
        """Build a chain network. Returns Network object."""
        network = Network()
        for i in range(size-1):
            network.add_link(i, i+1)
        return network

    @staticmethod
    def build_ring_network(size):
        """Build a ring network. Returns Network object."""
        network = Network()
        for i in range(size-1):
            network.add_link(i, i+1)
        network.add_link(0, size-1)
        return network

    @staticmethod
    def build_random_network(size, p):
        """Build a random (Erdos-Renyi) network. Returns Network object."""
        network = Network()
        for i in range(size):
            network.add_node(i)
        for i in range(size-1):
            for j in range(i+1, size):
                if random.random() < p:
                    network.add_link(i, j)
        return network

    @staticmethod
    def build_clique_network(size):
        """Build a clique network. Returns Network object."""
        network = Network()
        for i in range(size-1):
            for j in range(i+1, size):
                network.add_link(i, j)
        return network

    @staticmethod
    def build_hypercube_network(size):
        """Build a hypercube network. Returns Network object."""
        def _rec_build_hc_net(n):
            if n == 1:
                return {0:{}}

            m = int(n/2)
            network = {}
            network1 = _rec_build_hc_net(m)

            for node1 in network1:
                network[node1] = network1[node1]
                network[node1 + m] = {}
                for node2 in network1[node1]:
                    network[node1 + m][node2 + m] = 1

                network[node1][node1 + m] = 1
                network[node1 + m][node1] = 1
            return network

        # Find largest power of 2 < size
        nn = 1
        while nn <= size:
            nn = nn*2
        nn = nn/2

        network = _rec_build_hc_net(nn)
        return Network(fromDict=network)

    @staticmethod
    def build_grid_network(size_x, size_y):
        """Build a grid network. Returns Network object."""
        network = Network()
        for n in range(size_x * size_y):
            if (n+1) % size_x != 0:
                network.add_link(n, n+1)
            if n < (size_y - 1)*size_x:
                network.add_link(n, n+size_x)
        return network