# Fluent HTTP Python Logger Handler

A logger handler for [fluentd](fluent) logging collector.

## How to use it

```python
import logging
from fluent_http import FluentHttpHandler

logger = logging.getLogger(__name__)
fluent_http_handler = FluentHttpHandler(url='localhost', port=9880, tag='app.python')
logger.addHandler(fluent_http_handler)

# Test it!
logger.warning('Houston, we have a problem')
```

### JSON logging

Install `python-json-logger` before

```bash
pip install python-json-logger
```

```python
import logging
from pythonjsonlogger import jsonlogger
from fluent_http import FluentHttpHandler

logger = logging.getLogger(__name__)
fluent_http_handler = FluentHttpHandler(url='localhost', port=9880, tag='app.python')
fluent_http_handler.setFormatter(jsonlogger.JsonFormatter(timestamp=True))
logger.addHandler(fluent_http_handler)
logger.setLevel(logging.INFO)
# Test it!
logger.info('purchase done', extra={'item_id': 12345, 'quantity': 4, 'total_price': 32412})
```

## Protected under Auth Basic HTTP

```python
...
fluent_http_handler = FluentHttpHandler(url='https://fluent.example.com', port=443, tag='app.python', username='user', password='a_password')
...
```

## License

MIT License

