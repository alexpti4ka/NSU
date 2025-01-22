from node import Node
from typing import List, Dict, Any, Optional


class Pipeline:
    """
    A class representing a data processing pipeline.
    """

    class Channel:
        """
        A class representing a communication channel between nodes.
        """
        def __init__(self, source: Optional[Node] = None, destination: Optional[Node] = None, dtype: Optional[Any] = None):
            """
            Initializes a new channel.
            Args:
              source: the source node of a channel (can be None).
              destination: the destination node of a channel (can be None).
              dtype: (optional) type of data being passed throught the channel
            """
            self.source = source       # Исходный узел (может быть None)
            self.destination = destination  # Целевой узел (может быть None)
            self.dtype = dtype          # Тип данных, передаваемых по каналу (может быть None)


        def get_status(self):
            """
            Returns the status of the channel.
            Returns:
                A dictionary containing information about the source node, destination node, and type of data being passed throught the channel
            """
            return {
                "source": self.source.type if self.source else None,
                "destination": self.destination.type if self.destination else None,
                "dtype": self.dtype
            }
        
        def edit_channel(self, new_source: Node, new_destination: Node):
            """
            Changes the direction of a channel.
            Args:
            new_source: new source node
            new_destination: new destination node
            """

            self.source = new_source
            self.destination = new_destination

    def __init__(self):
        """Initializes a new Pipeline."""
        self.nodes: Dict[int, Node] = {}  # nodes with their positional IDs
        self.channels: List[Pipeline.Channel] = []
        self.next_node_id = 1 # Initialize the next available ID
        self.nodes_data: List[Dict] = [] # To store nodes data

    def _generate_node_id(self) -> int:
      """
      Generates unique ID for the node
      Returns:
        Unique ID
      """
      node_id = self.next_node_id
      self.next_node_id += 1
      return node_id

    def create_pipeline(self, nodes_data: List[Dict], custom_channels: List[tuple] = None):
        """
        Creates a pipeline with given nodes.
        Args:
            nodes_data: A list of dictionaries, where each dict contains a 'node' key for node instance and optional 'params' and 'channels' keys.
            custom_channels: (optional) a list of tuples in format (source_node_index, destination_node_index).
            If not set, will be created a default chain of channels
        """
        if not nodes_data:
            raise ValueError("List of nodes cannot be empty")

        # Assign ID's to nodes and store them
        for node_data in nodes_data:
            node = node_data.get("node")
            if not isinstance(node, Node):
                raise ValueError("Each node should be an instance of class Node")
            node_id = self._generate_node_id()
            self.nodes[node_id] = node
        
        self.nodes_data = nodes_data # Save nodes data

        if custom_channels:
            self._create_custom_channels(custom_channels)
        else:
            self._create_default_channels(nodes_data)

    def _create_custom_channels(self, custom_channels: List[tuple]):
        """
        Creates channels between nodes based on custom mapping
            Args:
            custom_channels: List of tuples in format (source_node_index, destination_node_index)
        """

        for source_index, dest_index in custom_channels:
            if source_index not in self.nodes or dest_index not in self.nodes:
                raise ValueError(f"Invalid node id: {source_index} or {dest_index}")

            source_node = self.nodes[source_index]
            dest_node = self.nodes[dest_index]

            
            channel = self.Channel(source_node, dest_node)
            self.channels.append(channel)


    def _create_default_channels(self, nodes_data: List[Dict]):
      """
        Creates default channels between nodes
        Args:
          nodes_data: list of nodes data
      """
      nodes = [node_data["node"] for node_data in nodes_data]
      for i in range(len(nodes)-1):
        source_node = nodes[i]
        dest_node = nodes[i+1]

        channel = self.Channel(source_node, dest_node, source_node.output_dtype)
        self.channels.append(channel)


    def edit_channel(self, source_node_type: str, destination_node_type:str):
      """
      Edits channel between two nodes, switching them
      Args:
        source_node_type: type of source node
        destination_node_type: type of destination node
      """
      source_node = next((node for node_id, node in self.nodes.items() if node.type == source_node_type), None)
      dest_node = next((node for node_id, node in self.nodes.items() if node.type == destination_node_type), None)


      if source_node is None or dest_node is None:
        raise ValueError(f"Invalid node type: {source_node_type} or {destination_node_type}")
      
      for channel in self.channels:
            if channel.source == source_node and channel.destination == dest_node:
              if channel.source.output_dtype != channel.destination.input_dtype:
                 raise ValueError(f"Incompatible data types for channel edit: {channel.source.output_dtype} -> {channel.destination.input_dtype}")
              channel.edit_channel(dest_node, source_node)
              return
        
      raise ValueError(f"Cannot find channel from node type {source_node_type} to {destination_node_type}")


    def get_info(self) -> Dict[str, Any]:
        """
        Returns information about the pipeline.
        Returns:
            A dictionary containing information about the nodes and channels in the pipeline.
        """
        nodes_info = {node_id: node.type for node_id, node in self.nodes.items()}
        channels_info = [
            channel.get_status()
            for channel in self.channels
        ]
        return {"nodes": nodes_info, "channels": channels_info}

    def run(self, input_data: Any):
        """
        Runs the pipeline.
        Args:
            input_data: The initial data to pass to the first node of the pipeline.
        Returns:
            The output of the last node in the pipeline.
        """
        if not self.channels:
            raise ValueError("Pipeline has no channels. Please, check pipeline construction.")

        current_data = input_data

        for channel in self.channels:
            source_node = channel.source
            dest_node = channel.destination

            # Find the node ID by node
            source_node_id = next((k for k, v in self.nodes.items() if v == source_node), None)

            if source_node_id is None:
                raise ValueError(f"Cannot find source node in the node map: {source_node}")
            
            # Extract params, if exist
            params = next((item.get("params") for item in self.nodes_data if item.get("node") == source_node), None)

            current_data = self._process_node(source_node, current_data, params)
            
            if dest_node:
              params = next((item.get("params") for item in self.nodes_data if item.get("node") == dest_node), None)
              current_data = self._process_node(dest_node, current_data, params)

        return current_data

    def _process_node(self, node: Node, data: Any, params: dict = None) -> Any:
        """
        Processes the single node.
        Args:
            node: node to process
            data: incoming data
            params: (optional) parameters to pass into node's process method
        Returns:
            processed data
        """
        if isinstance(node, Node):
            # Handle different callables based on node types
            if hasattr(node, "process"):
                if params:
                    return node.process(data, **params)
                else:
                    return node.process(data)
            else:
                raise ValueError(f"Node type {type(node)} doesn't have process method.")
        else:
            raise TypeError(f"Object {type(node)} is not Node type")