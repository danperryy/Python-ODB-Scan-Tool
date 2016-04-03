
import pytest

def pytest_addoption(parser):
    parser.addoption("--obdsim", action="store", default=None,
                     help="pts file name for obdsim tests")
