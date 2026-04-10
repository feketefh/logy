# tests/test_logger.py
from beautylog import Logger


def testInstantiation():
    logger = Logger()
    assert logger._indentLevel == 0


def testSetGroupLevel():
    logger = Logger()
    logger.setGroupLevel(2)
    assert logger._indentLevel == 2


def testSetGroupLevelNegative():
    import pytest

    logger = Logger()

    with pytest.raises(ValueError):
        logger.setGroupLevel(-1)
