import pytest


@pytest.mark.skip(reason="Not implemented")
async def test_correct():
    raise NotImplementedError


@pytest.mark.skip(reason="Not implemented")
async def test_incorrect():
    raise NotImplementedError
