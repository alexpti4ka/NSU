from typing import List, Tuple, Any
from abc import ABC, abstractmethod


class Channel:
    def __init__(self, data_type: type):
        self.data_type = data_type
        self.data = None

    def push(self, data: Any):
        if not isinstance(data, self.data_type):
            raise TypeError(f"Data type mismatch. Expected {self.data_type}, but got {type(data)}")
        self.data = data

    def pull(self):
        data = self.data
        self.data = None
        return data


class Node(ABC):
    def __init__(self, input_channels: List[Channel], output_channels: List[Channel]):
        self.input_channels = input_channels
        self.output_channels = output_channels

    @abstractmethod
    def run(self):
        pass
    
    def connect(self, other_node: "Node", output_index: int, input_index: int):
      if not (0 <= output_index < len(self.output_channels) and 0 <= input_index < len(other_node.input_channels)):
        raise ValueError("Invalid channel index")
      if self.output_channels[output_index].data_type != other_node.input_channels[input_index].data_type:
        raise TypeError("Channel type mismatch")
      self.output_channels[output_index].connect_to_channel = other_node.input_channels[input_index]



class HeaderExtractor(Node):
    def __init__(self):
        super().__init__(
            input_channels=[Channel(List[str])],
            output_channels=[Channel(List[Tuple[int, str]]), Channel(List[str])]
        )

    def run(self):
      input_data = self.input_channels[0].pull()

      if not isinstance(input_data, list):
        raise TypeError("Input data must be a list of strings")
      
      headers = []
      content_without_headers = []

      for line in input_data:
        if line.startswith("#"):
          level = 0
          for char in line:
            if char == "#":
              level+=1
            else:
              break
          header_text = line[level:].lstrip()
          headers.append((level, header_text))
        else:
          content_without_headers.append(line)
      
      self.output_channels[0].push(headers)
      self.output_channels[1].push(content_without_headers)