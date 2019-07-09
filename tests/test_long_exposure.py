from src.long_exposure import LongExposure


class TestLongExposure:
    def test_averager(self):
        avg = LongExposure.averager()
        assert avg(10) == 10
        assert avg(15) == 12.5
        assert avg(35) == 20
