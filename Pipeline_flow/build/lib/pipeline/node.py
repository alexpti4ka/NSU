from abc import ABC, abstractmethod
from typing import List, Any, Optional

class Node(ABC):
    """
    Abstract base class for all nodes in the pipeline.
    """
    _node_id_counter = 0

    def __init__(self):
      """Initializes a new node with a unique ID."""
      self.id = self._generate_node_id()
      self.type: str = "Abstract Node"
      self.input_channels: int = 1 # default = 1
      self.output_channels: int = 1 # default = 1
      self.input_dtype: List[type] = [Any] # default is any type
      self.output_dtype: List[type] = [Any] # default is any type

    def _generate_node_id(self) -> str:
      """Generates a unique node ID using a counter."""
      Node._node_id_counter += 1
      return f"node_{Node._node_id_counter}"

    @abstractmethod
    def process(self, data: Any, **kwargs) -> Any:
        """
        Processes the input data and returns the result.
        Args:
            data: The input data to process.
            kwargs: (optional) additional data parameters
        Returns:
            The processed data.
        """
        pass