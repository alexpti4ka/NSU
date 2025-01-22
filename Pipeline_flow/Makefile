PYTHON = python3
TEST_FILE = pipeline/test_node.py

test:
	$(PYTHON) $(TEST_FILE)

docs:
	cd docs && make html

clean:
	rm -rf docs/_build

.PHONY: test docs clean
