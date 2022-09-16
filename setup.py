import setuptools

setuptools.setup(
    name='fluent_http',
    version='0.1.0',
    author='JM Robles',
    author_email='chema@digitalilusion.com',
    description='Fluentd logger client for HTTP input',
    packages=['fluent_http'],
    license='Apache License, Version 2.0',
    test_suite='test',
    install_requires=[
        'requests'
    ]

)
