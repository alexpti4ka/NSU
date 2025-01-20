from abc import ABC, abstractmethod
from typing import Dict
from pipeline.channel import Channel

class Node(ABC): #создаем абстрактный класс
    """
    Abstract base class for all nodes in a data processing pipeline.
    
    A node represents a single unit of work in a pipeline, it processes data
    received from input channels and sends processed data to output channels.
    """
    def __init__(self, input_channels: Dict[str, Channel], output_channels: Dict[str, Channel]):
        """
        Initializes a new node with the specified input and output channels.

        Args:
            input_channels (Dict[str, Channel]): A dictionary containing input channels.
            output_channels (Dict[str, Channel]): A dictionary containing output channels.
        
        Raises:
           ValueError: If the channels are not a valid channel object.
        """
        self.input_channels = input_channels
        self.output_channels = output_channels
        self.validate_channels()

    @abstractmethod
    def process(self):
        """
        Abstract method that defines the logic for processing data.

        This method should be implemented by concrete subclasses
        to perform specific data transformations.
        """
        pass
    
    def validate_channels(self):
        """
        Validates input and output channels to ensure they are valid Channel objects.

        Raises:
            ValueError: If any input or output channel is not a valid Channel object.
        """
        for channel_name, channel in self.input_channels.items():
            if not isinstance(channel, Channel):
                raise ValueError(f"Input channel '{channel_name}' is not a valid channel object")
        for channel_name, channel in self.output_channels.items():
             if not isinstance(channel, Channel):
                 raise ValueError(f"Output channel '{channel_name}' is not a valid channel object")
    
    def get_input_data(self, channel_name: str):
         """
        Receives data from a specific input channel.

        Args:
            channel_name (str): The name of the input channel to receive data from.
        Returns:
            Any: The data received from the channel.

        Raises:
            ValueError: If the channel with name is not found.
        """
         if channel_name not in self.input_channels:
             raise ValueError(f"Input channel with name '{channel_name}' not found")
         channel = self.input_channels[channel_name]
         return channel.receive_data()

    def send_output_data(self, channel_name: str, data: any):
        """
        Sends data to a specific output channel.
        
        Args:
           channel_name (str): The name of the output channel to send data to.
           data (Any): Data to be sent.
        
        Raises:
            ValueError: If the channel with name is not found.
        """
        if channel_name not in self.output_channels:
            raise ValueError(f"Output channel with name '{channel_name}' not found")
        channel = self.output_channels[channel_name]
        channel.send_data(data)