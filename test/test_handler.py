import unittest
from unittest import mock
import logging
from logging import LogRecord

import pytest
import requests
from fluent_http import FluentHttpException
from fluent_http import FluentHttpHandler

class TestFluentHttpHandler(unittest.TestCase):


    def test_serialize(self):

        # Given
        entries = [
            ('hi world', '{"message": "hi world"}'),
            ('', '{"message": ""}'),
            ('{"message": "hi"}', '{"message": "hi"}'),
            ('{"temperature": "32", "unit": "celcius"}', '{"temperature": "32", "unit": "celcius"}'),
            ('peace ✌️', '{"message": "peace \\u270c\\ufe0f"}'),
            ('   ', '{"message": "   "}'),
        ]
        # When - Then
        fluent_http_handler = FluentHttpHandler()
        for entry in entries:
            assert fluent_http_handler._serialize(entry[0]) == entry[1]

    def test_build_url_default(self):

        # Given
        test_default_url = 'http://localhost:9880/fluent.info'
        # When
        fluent_http_handler = FluentHttpHandler()
        remote_url = fluent_http_handler._build_url()
        # Then
        assert remote_url == test_default_url

    def test_build_url_public(self):

        # Given
        test_url = 'https://fluent.example.com'
        test_port = 443
        test_tag = 'app.info'

        # When
        fluent_http_handler = FluentHttpHandler(url=test_url, port=test_port, tag=test_tag)
        remote_url = fluent_http_handler._build_url()
        # Then
        assert remote_url == f'{test_url}:{test_port}/{test_tag}'

    def test_build_url_public(self):

        # Given
        test_url = 'https://fluent.example.com'
        test_port = 443
        test_tag = 'app.info'

        # When
        fluent_http_handler = FluentHttpHandler(url=test_url, port=test_port, tag=test_tag)
        remote_url = fluent_http_handler._build_url()
        # Then
        assert remote_url == f'{test_url}:{test_port}/{test_tag}'

    @mock.patch.object(requests, 'post')
    def test_emit_success(self, mock_post):

        # Given
        test_name = 'name'
        test_level = logging.INFO
        test_pathname = 'path'
        test_lineno = 1
        test_msg = 'hello'
        test_args = None
        test_exc_info = None
        test_log_record = LogRecord(test_name, test_level, test_pathname, test_lineno,
                                    test_msg, test_args, test_exc_info)
        test_default_url = 'http://localhost:9880/fluent.info'
        # Mock
        mock_post.return_value.status_code = 200
        # When
        fluent_http_handler = FluentHttpHandler()
        fluent_http_handler.emit(test_log_record)
        # Then
        mock_post.assert_called_once_with(test_default_url, f'{{"message": "{test_msg}"}}',
                                          headers={'Content-type': 'application/json'}, auth=None)

    @mock.patch.object(requests, 'post')
    def test_emit_success_with_basic_auth(self, mock_post):

        # Given
        test_name = 'name'
        test_level = logging.INFO
        test_pathname = 'path'
        test_lineno = 1
        test_msg = 'hello'
        test_args = None
        test_exc_info = None
        test_log_record = LogRecord(test_name, test_level, test_pathname, test_lineno,
                                    test_msg, test_args, test_exc_info)
        test_default_url = 'http://localhost:9880/fluent.info'
        test_username = 'username'
        test_password = 'password'
        test_auth = requests.auth.HTTPBasicAuth(test_username, test_password)
        # Mock
        mock_post.return_value.status_code = 200
        # When
        fluent_http_handler = FluentHttpHandler(username=test_username, password=test_password)
        fluent_http_handler.emit(test_log_record)
        # Then
        mock_post.assert_called_once_with(test_default_url, f'{{"message": "{test_msg}"}}',
                                          headers={'Content-type': 'application/json'}, auth=test_auth)

    @mock.patch.object(requests, 'post')
    def test_emit_http_no_url(self, mock_post):

        # Given
        test_name = 'name'
        test_level = logging.INFO
        test_pathname = 'path'
        test_lineno = 1
        test_msg = 'hello'
        test_args = None
        test_exc_info = None
        test_log_record = LogRecord(test_name, test_level, test_pathname, test_lineno,
                                    test_msg, test_args, test_exc_info)
        test_url = 'not an url'
        # Mock
        mock_post.side_effect = FluentHttpException()
        # When
        fluent_http_handler = FluentHttpHandler(url=test_url)
        with pytest.raises(FluentHttpException) as exc:
            fluent_http_handler.emit(test_log_record)
        assert str(exc.value) == 'HTTP Exception'
        # Then
        mock_post.assert_called_once_with(f'{test_url}:9880/fluent.info', f'{{"message": "{test_msg}"}}',
                                          headers={'Content-type': 'application/json'}, auth=None)

    @mock.patch.object(requests, 'post')
    def test_emit_http_404(self, mock_post):

        # Given
        test_name = 'name'
        test_level = logging.INFO
        test_pathname = 'path'
        test_lineno = 1
        test_msg = 'hello'
        test_args = None
        test_exc_info = None
        test_log_record = LogRecord(test_name, test_level, test_pathname, test_lineno,
                                    test_msg, test_args, test_exc_info)
        test_url = 'not an url'
        # Mock
        mock_post.return_value.status_code = 404
        # When
        fluent_http_handler = FluentHttpHandler(url=test_url)
        with pytest.raises(FluentHttpException) as exc:
            fluent_http_handler.emit(test_log_record)
        assert str(exc.value) == 'Unexpected http response status: 404'
        # Then
        mock_post.assert_called_once_with(f'{test_url}:9880/fluent.info', f'{{"message": "{test_msg}"}}',
                                          headers={'Content-type': 'application/json'}, auth=None)

    @mock.patch.object(requests, 'post')
    def test_emit_http_500(self, mock_post):

        # Given
        test_name = 'name'
        test_level = logging.INFO
        test_pathname = 'path'
        test_lineno = 1
        test_msg = 'hello'
        test_args = None
        test_exc_info = None
        test_log_record = LogRecord(test_name, test_level, test_pathname, test_lineno,
                                    test_msg, test_args, test_exc_info)
        test_url = 'not an url'
        # Mock
        mock_post.return_value.status_code = 500
        # When
        fluent_http_handler = FluentHttpHandler(url=test_url)
        with pytest.raises(FluentHttpException) as exc:
            fluent_http_handler.emit(test_log_record)
        assert str(exc.value) == 'Unexpected http response status: 500'
        # Then
        mock_post.assert_called_once_with(f'{test_url}:9880/fluent.info', f'{{"message": "{test_msg}"}}',
                                          headers={'Content-type': 'application/json'}, auth=None)