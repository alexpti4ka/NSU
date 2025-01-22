from node import Node

class DataOperator(Node):
    """
    Concrete class for operating with data.
    """
    def __init__(self):
        """Initializes a new DataOperator node."""
        super().__init__()
        self.type = "DataOperator"
        self.input_dtype = dict
        self.output_dtype = dict

    def selectHeaderData(self, data, keys):
        """
        Selects data based on provided keys.
        Args:
            data: Input data (dictionary).
            keys: A list of keys to select.
        Returns:
            A dictionary with selected key-value pairs.
        Raises:
            ValueError: If any of the keys are not found in the data.
        """
        selected_data = {}
        for key in keys:
            if key not in data:
                raise ValueError(f"Incorrect key: '{key}' not found in data.")
            selected_data[key] = data[key]
        return selected_data

    def process(self, data, keys=None):
        """
        Processes the data with `selectHeaderData()` method
        Args:
           data: Data to operate
           keys: keys to select
        Returns:
          selected data
        Raises:
          ValueError: if status not parsed
        """
        if not isinstance(data, dict):
            raise TypeError("Input data must be a dictionary.")
        if "status" not in data or data["status"] != "parsed":
          raise ValueError("Input data must have status 'parsed'")
        return self.selectHeaderData(data, keys)