import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--run-integration', action='store_true', default=False,
        help='run integration tests which require a GitHub user and token'
    )


def pytest_configure(config):
    config.addinivalue_line('markers', 'integration: mark test as part of integration test suite')


def pytest_collection_modifyitems(config, items):
    if config.getoption('--run-integration'):
        # --run-integration given in cli: do not skip integration tests
        return
    skip_integration = pytest.mark.skip(reason='need --run-integration option to run')
    for item in items:
        if 'integration' in item.keywords:
            item.add_marker(skip_integration)
