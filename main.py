import logging

from fluent_http.handler import FluentHttpHandler
from pythonjsonlogger import jsonlogger


if __name__ == '__main__':

    logger = logging.getLogger('main.test')
    fluent_http_handler = FluentHttpHandler(url='https://fluentd.digitalilusion.com', port=443, tag='app.python', username='reporter', password='as05ro12')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fluent_http_handler.setFormatter(formatter)
    logger.addHandler(fluent_http_handler)
    
    logger.warning('jander sander monder')
    logger.error('Main Error 2', extra={'os': 'Darwin', 'arch': 'arm64'})
    fluent_http_handler.setFormatter(jsonlogger.JsonFormatter(timestamp=True))
    logger.warning('testing', extra={'mode': 'dev'})