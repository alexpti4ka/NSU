from typing import Dict, Any
from pipeline.node import Node
from pipeline.channel import Channel, CHANNEL_TYPE_STRING, CHANNEL_TYPE_DICT_STR_ANY, CHANNEL_TYPE_BYTES
from pipeline.data_pdf_parser import PdfParser
from pipeline.data_file_reader import FileReader


class DocumentParser(Node):
    """
    A node that determines the type of a document and dispatches it to the correct parser.
    """
    def __init__(self, output_channels: Dict[str, Channel]):
        """
        Initializes a DocumentParser with an output channel for structured data.

        Args:
            output_channels (Dict[str, Channel]): A dictionary containing output channels.
             It should have exactly one output channel with `CHANNEL_TYPE_DICT_STR_ANY`.

        Raises:
            ValueError: If the output channel is not of the correct type.
        """
        if len(output_channels) != 1:
             raise ValueError("DocumentParser should have exactly one output channel")

        if not all(channel.data_type == CHANNEL_TYPE_DICT_STR_ANY for channel in output_channels.values()):
            raise ValueError("Output channel must have a type 'dict[str, any]'")

        input_channels = {
            "file_path": Channel(CHANNEL_TYPE_STRING)
        }
        super().__init__(input_channels, output_channels)
        self.pdf_parser = PdfParser({})
        self.file_reader = FileReader({"file_content": Channel(CHANNEL_TYPE_BYTES)})


    def process(self):
        """
        Processes the document based on its file type.

        Raises:
            ValueError: If the file format is not supported.
        """
        file_path = self.get_input_data("file_path")
        
        self.file_reader.input_channels['file_path'].send_data(file_path)
        self.file_reader.process()
        file_content = self.file_reader.output_channels['file_content'].receive_data()

        if file_path.lower().endswith(".pdf"):
           self.pdf_parser.input_channels['file_content'].send_data(file_content)
           self.pdf_parser.process()
           structured_data = self.pdf_parser.output_channels['structured_data'].receive_data()
           self.send_output_data(list(self.output_channels.keys())[0], structured_data)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")