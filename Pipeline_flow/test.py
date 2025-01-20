import unittest
from pipeline.node import Node
from pipeline.channel import Channel, CHANNEL_TYPE_STRING, CHANNEL_TYPE_BYTES
from pipeline.data_file_reader import FileReader
from typing import Dict
import os

#python Pipeline_flow/test.py для запуска

class TestNode(Node):
    def __init__(self, input_channels: Dict[str, Channel], output_channels: Dict[str, Channel]):
        super().__init__(input_channels, output_channels)

    def process(self):
        pass


# class TestNodeTest(unittest.TestCase):
#     def test_valid_channels(self):
#         input_channels = {"input1": Channel(CHANNEL_TYPE_STRING)}
#         output_channels = {"output1": Channel(CHANNEL_TYPE_STRING)}
#         node = TestNode(input_channels, output_channels)
#         self.assertIsInstance(node, Node)

#     def test_invalid_input_channels(self):
#         input_channels = {"input1": "not a channel"}
#         output_channels = {"output1": Channel(CHANNEL_TYPE_STRING)}
#         with self.assertRaises(ValueError):
#             TestNode(input_channels, output_channels)

#     def test_invalid_output_channels(self):
#         input_channels = {"input1": Channel(CHANNEL_TYPE_STRING)}
#         output_channels = {"output1": "not a channel"}
#         with self.assertRaises(ValueError):
#             TestNode(input_channels, output_channels)
    
#     def test_get_input_data(self):
#         input_channels = {"input1": Channel(CHANNEL_TYPE_STRING)}
#         output_channels = {"output1": Channel(CHANNEL_TYPE_STRING)}
#         node = TestNode(input_channels, output_channels)
#         test_data = 'test input'
#         input_channels['input1'].send_data(test_data)
#         received_data = node.get_input_data('input1')
#         self.assertEqual(received_data, test_data)
    
#     def test_get_input_data_not_found(self):
#          input_channels = {"input1": Channel(CHANNEL_TYPE_STRING)}
#          output_channels = {"output1": Channel(CHANNEL_TYPE_STRING)}
#          node = TestNode(input_channels, output_channels)
#          with self.assertRaises(ValueError):
#             node.get_input_data('wrong_input')
    
#     def test_send_output_data(self):
#          input_channels = {"input1": Channel(CHANNEL_TYPE_STRING)}
#          output_channels = {"output1": Channel(CHANNEL_TYPE_STRING)}
#          node = TestNode(input_channels, output_channels)
#          test_data = 'test output'
#          node.send_output_data('output1', test_data)
#          received_data = output_channels['output1'].receive_data()
#          self.assertEqual(received_data, test_data)
    
#     def test_send_output_data_not_found(self):
#          input_channels = {"input1": Channel(CHANNEL_TYPE_STRING)}
#          output_channels = {"output1": Channel(CHANNEL_TYPE_STRING)}
#          node = TestNode(input_channels, output_channels)
#          with self.assertRaises(ValueError):
#             node.send_output_data('wrong_output', 'test')


# if __name__ == '__main__':
#     unittest.main()



class TestFileReader(unittest.TestCase):
    def setUp(self):
        # Создаем тестовый файл
        self.test_file_path = "test_file.txt"
        with open(self.test_file_path, "w") as f:
            f.write("This is a test file.")

    def tearDown(self):
         # Удаляем тестовый файл
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_read_existing_file(self):
        output_channel = {"file_content": Channel(CHANNEL_TYPE_BYTES)}
        file_reader = FileReader(output_channel)
        input_channel = file_reader.input_channels["file_path"]
        input_channel.send_data(self.test_file_path)
        file_reader.process()
        content = file_reader.output_channels["file_content"].receive_data()
        self.assertEqual(content, b"This is a test file.")

    def test_read_non_existing_file(self):
        output_channel = {"file_content": Channel(CHANNEL_TYPE_BYTES)}
        file_reader = FileReader(output_channel)
        input_channel = file_reader.input_channels["file_path"]
        input_channel.send_data("non_existing_file.txt")
        with self.assertRaises(FileNotFoundError):
            file_reader.process()
    
    def test_invalid_output_channel_type(self):
        with self.assertRaises(ValueError):
            FileReader({"output": Channel(CHANNEL_TYPE_STRING)})

    def test_invalid_output_channels_count(self):
        with self.assertRaises(ValueError):
            FileReader({"output1": Channel(CHANNEL_TYPE_BYTES), "output2": Channel(CHANNEL_TYPE_BYTES)})
    
    def test_invalid_input_channel(self):
         output_channel = {"file_content": Channel(CHANNEL_TYPE_BYTES)}
         file_reader = FileReader(output_channel)
         with self.assertRaises(ValueError):
            file_reader.get_input_data('wrong_channel')


if __name__ == '__main__':
    unittest.main()