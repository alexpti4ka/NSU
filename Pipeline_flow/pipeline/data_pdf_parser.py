from typing import List
from pipeline.node import Node
from pipeline.channel import Channel, CHANNEL_TYPE_BYTES
import fitz # PyMuPDF

class PdfParser(Node):
    """
    A node that extracts text with header markup from a PDF file.
    """
    def __init__(self):
        """
        Initializes a PdfParser node with an output channel for text lines.
        """
        input_channels = [
            Channel(CHANNEL_TYPE_BYTES)
        ]
        output_channels = [Channel(List[str])]
        super().__init__(input_channels, output_channels)

    def run(self):
        """
        Extracts text with header markup from a PDF file and sends it to the output channel.

        Raises:
            ValueError: If the file content is not bytes or a file path is passed.
            fitz.fitz.FileDataError: If the file is not a valid PDF file.
            IOError: If there is an error during file reading.
        """
        file_content = self.input_channels[0].pull()
        if not isinstance(file_content, bytes):
           raise ValueError("PdfParser expects file content as bytes, not a file path.")

        try:
          doc = fitz.open(stream=file_content, filetype="pdf")
          all_lines = []
          for page in doc:
            blocks = page.get_text("blocks")
            
            for block in blocks:
              # Extract text, bounding box and font size
              x0, y0, x1, y1, text, block_type = block[:6]
              if block_type == 0: # ignore images
                lines = text.splitlines()
                if lines:
                    
                    first_line = lines[0]
                    font_size = None
                    for span in page.get_text("rawdict", clip=fitz.Rect(x0, y0, x1, y1))["blocks"][0]["lines"][0]["spans"]:
                      font_size = span["size"]
                      break
                    
                    # Check for header (simplistic check, should be improved)
                    if font_size > 12: # or if first_line.startswith(('<B>', '<I>', '<U>')):
                        header_level = 1
                        if len(all_lines) > 0 and all_lines[-1].startswith("#"):
                            if font_size > font_size_prev:
                                header_level = len(all_lines[-1].split(' ')[0]) + 1
                        all_lines.append("#"*header_level + " " + first_line)
                        font_size_prev = font_size
                        for i in range(1, len(lines)):
                          all_lines.append(lines[i])
                    else:
                        for line in lines:
                          all_lines.append(line)
                all_lines.append("") # add space between blocks of text

          doc.close()
          self.output_channels[0].push(all_lines)
        except fitz.fitz.FileDataError as e:
           raise ValueError(f"Error reading pdf: {e}")
        except Exception as e:
              raise IOError(f"Error during pdf parsing: {e}")

