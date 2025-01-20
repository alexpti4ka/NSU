from typing import Dict
from pipeline.node import Node
from pipeline.channel import Channel, CHANNEL_TYPE_STRING, CHANNEL_TYPE_BYTES

class FileReader(Node):
    """
    A node that reads the content of a file and sends it through an output channel.
    """
    def __init__(self, output_channels: Dict[str, Channel]):
        """
        Initializes a FileReader node with an output channel for the file content.

        Args:
            output_channels (Dict[str, Channel]): A dictionary containing output channels.
             It should have exactly one output channel with `CHANNEL_TYPE_BYTES`.

        Raises:
            ValueError: If the output channel is not of the correct type.
        """
        if len(output_channels) != 1:
             raise ValueError("FileReader should have exactly one output channel")
        
        if not all(channel.data_type == CHANNEL_TYPE_BYTES for channel in output_channels.values()):
            raise ValueError("Output channel must have a type 'bytes'")

        input_channels = {
            "file_path": Channel(CHANNEL_TYPE_STRING)
        }
        super().__init__(input_channels, output_channels)

    def process(self):
        """
        Reads the file from the input channel and sends the content to the output channel.

        Raises:
            FileNotFoundError: If the file path is invalid.
            IOError: If there is an error during file reading.
        """
        file_path = self.get_input_data("file_path")
        try:
            with open(file_path, 'rb') as f: #чтение файла в двоичном коде
                file_content = f.read()
            self.send_output_data(list(self.output_channels.keys())[0], file_content)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except IOError as e:
            raise IOError(f"Error reading file: {file_path}: {e}")