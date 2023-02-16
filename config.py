import sys

DATABASE_PATH = 'clientes.csv'  # Define a constant for the database path

if 'pytest' in sys.argv[0]:
    DATABASE_PATH = 'tests/clientes_tests.csv'  # If running tests, use the tests database