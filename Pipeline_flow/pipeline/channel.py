from typing import Any, Type
from typing import Literal

CHANNEL_TYPE_STRING = "str"
CHANNEL_TYPE_BYTES = "bytes"
CHANNEL_TYPE_LIST_STR = "list[str]"
CHANNEL_TYPE_DICT_STR_STR = "dict[str, str]"
CHANNEL_TYPE_DICT_STR_ANY = "dict[str, any]"

ChannelTypes = Literal[ #только 1 тип данных
    "str",
    "bytes",
    "list[str]",
    "dict[str, str]",
    "dict[str, any]"
]

class Channel:
    """
    Represents a data channel for passing data between nodes in a pipeline.

    A channel is responsible for storing and validating the type of data
    that can be passed through it.
    """
    def __init__(self, data_type: ChannelTypes):
        """
        Initializes a new channel with the specified data type.

        Args:
            data_type (ChannelTypes): The type of data that can be passed through this channel.
             Must be one of ChannelTypes
        
        Raises:
           ValueError: If the data_type is not one of the allowed types in `ChannelTypes`
        """
        if data_type not in [CHANNEL_TYPE_STRING,
                             CHANNEL_TYPE_BYTES,
                             CHANNEL_TYPE_LIST_STR,
                             CHANNEL_TYPE_DICT_STR_STR,
                             CHANNEL_TYPE_DICT_STR_ANY]:
            raise ValueError(f"Invalid data type: {data_type}. Must be one of {ChannelTypes.__args__}")
        self.data_type = data_type
        self.data: Any = None  # Initialize with None

    def send_data(self, data: Any) -> None:
        """
        Sends data through the channel, performing type validation.

        Args:
            data (Any): The data to be sent through the channel.
        
        Raises:
           TypeError: If the data is not an instance of the channel's `data_type`.
        """
        if not self._is_valid_type(data):
            raise TypeError(
                f"Invalid data type. Expected: {self.data_type}, Got: {type(data)}"
            )
        self.data = data

    def receive_data(self) -> Any:
         """
        Receives data from the channel.

        Returns:
           Any: The data received from the channel.
        """
         return self.data
    
    def _is_valid_type(self, data: Any) -> bool:
      """
       Checks if a given data object is of a valid type for this channel.

       Args:
        data (Any): The data to validate.

       Returns:
        bool: True if the data is a valid type for this channel, False otherwise.
        """
      if self.data_type == CHANNEL_TYPE_STRING:
        return isinstance(data, str)
      elif self.data_type == CHANNEL_TYPE_BYTES:
        return isinstance(data, bytes)
      elif self.data_type == CHANNEL_TYPE_LIST_STR:
        return isinstance(data, list) and all(isinstance(item, str) for item in data)
      elif self.data_type == CHANNEL_TYPE_DICT_STR_STR:
         return isinstance(data, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in data.items())
      elif self.data_type == CHANNEL_TYPE_DICT_STR_ANY:
           return isinstance(data, dict) and all(isinstance(k, str) for k in data.keys())
      else:
            return False