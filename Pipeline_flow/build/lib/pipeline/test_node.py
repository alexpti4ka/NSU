from node_pdf_parser import PDFParser
from node_data_operator import DataOperator
from pipeline import Pipeline

# Тестирование парсера
pdf_parser = PDFParser()

metadata_path = "/Users/alexpti4ka/Documents/Cursor_projects/Pipeline_flow/pdf_metadata.txt"
simulated_data = pdf_parser.process(metadata_path, header_extractor=True)

#print(simulated_data)

# Тестирование селектора
operator = DataOperator()

keys_to_select = ["file_type", "status"]

selected_data = operator.process(simulated_data, keys_to_select)

# print(selected_data)

# Тестирование пайплайна
pipeline = Pipeline()

nodes_data = [
    {"node": pdf_parser},
    {"node": operator, "params": {"keys": keys_to_select}}
]
pipeline.create_pipeline(nodes_data)

print(pipeline.get_info())
result = pipeline.run(metadata_path)
print(f"Result: {result}")


# Тестирование измененного пайплайна
pipeline2 = Pipeline()

nodes_data2 = [
    {"node": operator, "params": {"keys": keys_to_select}},
    {"node": pdf_parser},
]
pipeline2.create_pipeline(nodes_data2)

print(f"Initial pipeline info 2: {pipeline2.get_info()}")

try:
  pipeline2.edit_channel(source_node_type="DataOperator", destination_node_type="PDFParser")
  print(f"Changed pipeline info 2: {pipeline2.get_info()}")

  result2 = pipeline2.run(metadata_path)
  print(f"Result: {result2}")
except ValueError as e:
    print(f"Error: {e}")