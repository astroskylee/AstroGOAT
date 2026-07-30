import unittest

import numpy as np

from Tian_color import normalize_raw_channels_common


class RawNormalizationTests(unittest.TestCase):
    def test_saturated_outlier_does_not_set_shared_scale(self):
        red = np.ones((100, 100), dtype=np.float32)
        green = np.full((100, 100), 0.5, dtype=np.float32)
        blue = np.full((100, 100), 0.25, dtype=np.float32)
        red[0, 0] = 10_000.0

        red_out, green_out, blue_out, scale = normalize_raw_channels_common(
            red, green, blue
        )

        self.assertAlmostEqual(scale, 1.0)
        self.assertAlmostEqual(float(red_out[50, 50]), 1.0)
        self.assertAlmostEqual(float(green_out[50, 50]), 0.5)
        self.assertAlmostEqual(float(blue_out[50, 50]), 0.25)
        self.assertAlmostEqual(float(red_out[0, 0]), 1.0)

    def test_negative_background_values_are_preserved(self):
        red = np.ones((100, 100), dtype=np.float32)
        green = np.ones((100, 100), dtype=np.float32)
        blue = np.ones((100, 100), dtype=np.float32)
        blue[10, 10] = -0.2

        _, _, blue_out, _ = normalize_raw_channels_common(red, green, blue)

        self.assertLess(float(blue_out[10, 10]), 0.0)


if __name__ == "__main__":
    unittest.main()
