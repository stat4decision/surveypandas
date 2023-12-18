import unittest
import numpy as np
import pandas as pd

from surveypandas import SeriesW, DataFrameW


class TestFrameClass(unittest.TestCase):

    def test_frame(self):
        frame_w = DataFrameW(np.range(10),weights=np.ones(10))
        self.assertEqual(frame_w, pd.DataFrame(np.range(10)))

    def test_series(self):
        series_w = SeriesW(np.range(10),weights=np.ones(10))
        self.assertEqual(series_w, pd.Series(np.range(10)))

    def test_mean(self):
        series_w = SeriesW(np.range(10),weights=np.range(10))
        self.assertEqual(series_w.mean(), 
                         np.average(np.range(10),weights=np.range(10)))

    def test_transform(self):
        series_w = SeriesW(np.range(10),weights=np.range(10))
        frame_w = DataFrameW(np.range(10),weights=np.range(10))
        self.assertEqual(series_w.mean(),frame_w[0].mean())


if __name__ == '__main__':
    unittest.main()