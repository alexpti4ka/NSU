from node_document_parser import DocumentParser
# import pypdf2 / fitz / PyMuPDF – позднее для конкретной реализации

class PDFParser(DocumentParser):
    """
    Concrete class for parsing PDF documents.
    """
    def __init__(self):
        """Initializes a new PDF parser node."""
        super().__init__()
        self.type = "PDFParser"
        self.input_dtype = str
        self.output_dtype = list

    def parse(self, path):
        """
        Parses metadata from the file and returns it as a dictionary.
        Also checks if the file type is PDF.
        Args:
          path: Path to the metadata file.
        Returns:
          A dictionary with the metadata.
        """
        metadata = {}
        try:
            with open(path, "r") as file:
                data = file.readlines()
                for line in data:
                    try:
                        key, value = line.split(":")
                        metadata[key.strip()] = value.strip()
                    except ValueError:
                        raise ValueError(f"Incorrect data format in line: '{line.strip()}'")

            if metadata.get("file_type") != "pdf":
                raise ValueError("This parser is only for PDF files.")

            return metadata
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{path}' was not found.")
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")

    def process(self, path, header_extractor=False):
        """
        Processes the document by parsing metadata and optionally extracts headers.
        Args:
            path: Path to the metadata file.
            header_extractor: Boolean parameter defining whether headers extraction should be executed or not.
        Returns:
            The parsed data (new dictionary).
        """
        try:
            metadata = self.parse(path)

            # Update status to parsed
            if metadata.get("status") == "raw_data":
                metadata["status"] = "parsed"

            # Update header_extractor if requested
            if header_extractor:
                metadata["header_extractor"] = "true"

            return metadata

        except Exception as e:
            return f"Error processing file: {str(e)}"


if __name__ == '__main__':
    # Example usage:
    # Create a sample metadata file for testing
    with open("test_metadata.txt", "w") as f:
        f.write("file_type: pdf\n")
        f.write("page_count: 10\n")
        f.write("status: raw_data\n")
        f.write("header_extractor: false\n")
        f.write("table_extractor: false\n")

    parser = PDFParser()
    # First pass without header extraction
    result1 = parser.process("test_metadata.txt")
    print(f"Result 1: {result1}")

    # Second pass with header extraction
    result2 = parser.process("test_metadata.txt", header_extractor=True)
    print(f"Result 2: {result2}")

    # Third pass to see that status will not change
    result3 = parser.process("test_metadata.txt")
    print(f"Result 3: {result3}")

    # Print updated metadata (for verification)
    with open("test_metadata.txt", "r") as f:
      print("Original file content:")
      for line in f:
        print(line.strip())

    # Create an invalid test metadata
    with open("test_metadata_wrong_type.txt", "w") as f:
        f.write("file_type: docx\n")
        f.write("page_count: 10\n")
        f.write("status: raw_data\n")
        f.write("header_extractor: false\n")
        f.write("table_extractor: false\n")

    #Test on incorrect file format
    result4 = parser.process("test_metadata_wrong_type.txt")
    print(f"Result 4: {result4}")