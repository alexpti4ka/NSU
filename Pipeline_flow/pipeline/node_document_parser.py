from abc import abstractmethod
from node import Node

class DocumentParser(Node):
    """
    Abstract base class for document parser nodes.

    """
    def __init__(self):
        """Initializes a new document parser node."""
        super().__init__()
        self.type = "parser"

    @abstractmethod
    def parse(self, path):
        """
        Abstract method to parse the document

        Args:
          path: Path to the document.

        Returns:
           The parsed data.
        """
        pass

    def process(self, path): # по сути вызывает парсинг
        """
        Processes the path with `parse()` method
        Args:
           path: path to the document
        Returns:
          The parsed data.
        """
        return self.parse(path)