from abc import ABC, abstractmethod

_node_id_counter = 0

def generate_node_id():
    """Generates a unique node ID using a counter."""
    global _node_id_counter
    _node_id_counter += 1
    return f"node_{_node_id_counter}"


class Node(ABC):
    """
    Abstract base class for all nodes in the pipeline.
    
    """

    def __init__(self):
        """Initializes a new node with a unique ID."""
        self.id = generate_node_id()
        self.input_channels = []
        self.output_channels = []
        self.position = None
        self.input_dtype = None
        self.output_dtype = None

    @abstractmethod
    def process(self, data):
        """
        Abstract method for processing data in the node.

        Args:
          data: The data to be processed.

        Returns:
          The processed data.
        """
        pass