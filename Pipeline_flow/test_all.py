import os
import sys
from pipeline.node import Node
from pipeline.channel import Channel
from pipeline.data_pdf_parser import PdfParser
from pipeline.data_header_extractor import HeaderExtractor

def test_pipeline(pdf_file_path):
    """
    A test that runs a pipeline with a specified PDF file path.
    """
    try:
        # 1. Check if the file exists
        if not os.path.exists(pdf_file_path):
            raise FileNotFoundError(f"File not found: {pdf_file_path}")

        # 2. Create instances of nodes
        pdf_parser = PdfParser()
        header_extractor = HeaderExtractor()

        # 3. Create channels and connect them
        pdf_output_channel = pdf_parser.output_channels[0]
        header_extractor.input_channels[0].connect_to_channel = pdf_output_channel

        # 4. Load PDF file as bytes
        with open(pdf_file_path, "rb") as f:
            pdf_content = f.read()

        # 5. Run the pipeline step by step
        print("--- PdfParser ---")
        print(f"Input data (bytes): {pdf_content[:100]}... (truncated)")
        pdf_parser.input_channels[0].push(pdf_content)

        pdf_parser.run()
        pdf_parser_output = pdf_parser.output_channels[0].pull()
        print(f"Output data (lines):\n {pdf_parser_output[:5]}... (truncated)")

        print("\n--- HeaderExtractor ---")
        print(f"Input data (lines):\n {pdf_parser_output[:5]}... (truncated)")
        header_extractor.run()
        header_output_headers = header_extractor.output_channels[0].pull()
        header_output_content = header_extractor.output_channels[1].pull()
        print(f"Output headers:\n {header_output_headers}")
        print(f"Output content:\n {header_output_content[:5]}... (truncated)")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a PDF file path as an argument.")
        sys.exit(1)

    pdf_file_path = sys.argv[1]
    test_pipeline(pdf_file_path)


# python Pipeline_flow/test_all.py Pipeline_flow/example_doc.pdf