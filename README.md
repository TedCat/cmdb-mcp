# local test

- start the server
```
python main.py
```
- use cherry studio, config the mcp and enable it in chats

# unit test
- unit test is created by Kiro so far -- 20250815
- run unit test by command below
```
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_mcp_tools_instance.py -v

# Run with coverage (if you have pytest-cov installed)
python -m pytest tests/ --cov=ops --cov-report=html
```
