# STCI

STCI stands for **SpaceTelescopeColorImage**.

STCI is a small astronomy image-composition tool for making display-ready
color JPEGs or 16-bit TIFFs from space telescope cutouts and other aligned mono images.

## Installation

```bash
pip install STCI
```

The installed Python import module is `STCI`.

## Example usage

`mk_colorimg` creates one color image from either a 3-channel RGB array or three mono images in `(R, G, B)` order. For Euclid-style color images, the default mapping is `NIR_J`, `NIR_Y`, `VIS`.

```python
from STCI import mk_colorimg

mk_colorimg(
    [
        "cutout_H.fits",    # R channel
        "cutout_VIS.fits",  # G channel
        "cutout_Y.fits",    # B channel
    ],
    output_jpg="target_mtf_vis_y_h.jpg",
    input_mode="raw",
    ReplaceL=False,
    reference_ROI=200,
)
```

For a NumPy RGB cube:

```python
from STCI import mk_colorimg

mk_colorimg(rgb_array, output_jpg="target_color.jpg", input_mode="normalized")
```

Use a `.tif` or `.tiff` output filename to write a 16-bit TIFF instead of an 8-bit JPEG:

```python
mk_colorimg(rgb_array, output_jpg="target_color.tiff", input_mode="normalized")
```

Set `ReplaceL=False` to skip replacing the CIELab L* channel with the stretched blue luminosity channel. By default, `mk_colorimg` keeps the original replacement behavior.

Set `reference_ROI=200` to estimate the raw normalization, color calibration, and STF/HT stretch from the centered `200 x 200` pixel region, then apply those settings to the full image. By default, `reference_ROI=None` estimates from the full image.

## Single-Band MTF Image

`mk_monoimg` creates one grayscale image from a single mono image. It uses the same MTF-style stretch as `mk_colorimg`, but omits RGB-only steps such as color calibration, Lab luminance replacement, SCNR, and saturation.

```python
from STCI import mk_monoimg

mk_monoimg(
    "cutout_VIS.fits",
    output_jpg="target_vis_mtf.jpg",
    input_mode="raw",
)
```

For a NumPy mono image:

```python
from STCI import mk_monoimg

mk_monoimg(mono_array, output_jpg="target_mono.jpg", input_mode="normalized")
```

## Download a Euclid Color Image

`Euclidimg` downloads Euclid DR1 `VIS`, `NIR_Y`, `NIR_J`, and `NIR_H` FITS cutouts, then renders one color image using the `NIR_J / NIR_Y / VIS` channel order.

```python
from STCI import Euclidimg

result = Euclidimg(
    ra=50.7163333,
    dec=-39.7693889,
    size=5.0,
    path="euclid_color",
    cred="Euclid/cred.txt",
    output_jpg="EUCLJ032251.92-394609.8.jpg",
    ReplaceL=True,
    RGB="auto",
    reference_ROI=None,
)

print(result["jpg"])
print(result["fits"])
print(result["rgb_bands"])
```

Arguments:

- `ra`, `dec`: target coordinates in degrees.
- `size`: cutout radius in arcsec. For example, `size=5.0` makes a `10" x 10"` image.
- `path`: output directory for the FITS files and rendered image.
- `cred`: Euclid credentials file passed to `astroquery.esa.euclid`.
- `output_jpg`: optional output filename written inside `path`; use `.tif` or `.tiff` for 16-bit TIFF.
- `ReplaceL`: if `False`, skip replacing the CIELab L* channel with the stretched blue luminosity channel.
- `RGB`: Euclid bands in `(R, G, B)` order. Use `"auto"` for the default available-band choice, or pass bands such as `("NIR_H", "NIR_Y", "VIS")` or `("H", "Y", "VIS")`.
- `reference_ROI`: optional centered square ROI size, in pixels, used to estimate the display scaling before applying it to the full image.

The returned dictionary contains the selected FITS paths and the final rendered image path. If the first overlapping mosaic tile for a band is empty or all zero, the downloader tries the next matching tile.

## Download Euclid FITS Only

```python
from Download_Euclid import EUC_download

fits_paths = EUC_download(
    ra=50.7163333,
    dec=-39.7693889,
    size=5.0,
    path="euclid_fits",
    cred="Euclid/cred.txt",
)
```
