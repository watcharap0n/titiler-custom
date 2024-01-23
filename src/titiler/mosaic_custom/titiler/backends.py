"""mosaic backends.

The goal is to build a minimalist Mosaic Backend which takes COG paths as input.

>>> with MultiFilesBackend(["cog1.tif", "cog2.tif"]) as mosaic:
    img = mosaic.tile(1, 1, 1)

app/backends.py

"""
from typing import Type, List, Tuple, Dict, Union

import attr
import httpx
from cogeo_mosaic.backends.base import BaseBackend
from cogeo_mosaic.mosaic import MosaicJSON
from geojson_pydantic.features import Feature
from geojson_pydantic.geometries import Polygon
from morecantile import TileMatrixSet
from rasterio.crs import CRS
from rio_tiler.constants import WEB_MERCATOR_TMS, WGS84_CRS
from rio_tiler.io import BaseReader, COGReader, MultiBandReader, MultiBaseReader

GET_BBOX = 'https://titiler.xyz/cog/bounds'


def raster_to_features(bbox, url):
    xmin, ymin, xmax, ymax = bbox
    return Feature(
        type="Feature",
        geometry=Polygon.from_bounds(xmin, ymin, xmax, ymax),
        properties={"path": url}).dict(exclude_none=True)


@attr.s
class MultiFilesBackend(BaseBackend):
    input: List[str] = attr.ib()

    reader: Union[
        Type[BaseReader],
        Type[MultiBaseReader],
        Type[MultiBandReader],
    ] = attr.ib(default=COGReader)
    reader_options: Dict = attr.ib(factory=dict)

    geographic_crs: CRS = attr.ib(default=WGS84_CRS)

    tms: TileMatrixSet = attr.ib(default=WEB_MERCATOR_TMS)
    minzoom: int = attr.ib(default=0)
    maxzoom: int = attr.ib(default=30)

    # default values for bounds
    bounds: Tuple[float, float, float, float] = attr.ib(
        default=(-180, -90, 180, 90)
    )
    crs: CRS = attr.ib(init=False, default=WGS84_CRS)

    # mosaic_def is outside the __init__ method
    mosaic_def: MosaicJSON = attr.ib(init=False)

    _backend_name = "MultiFiles"

    def __attrs_post_init__(self):
        """Post Init."""
        # Construct a FAKE/Empty mosaicJSON
        # mosaic_def has to be defined.
        res = httpx.get(GET_BBOX, params={'url': self.input[0]}).json()['bounds']
        features = [raster_to_features(res, url) for url in self.input]
        with COGReader(self.input[0]) as cog:
            info = cog.info()

        self.bounds = info.bounds
        self.minzoom = info.minzoom
        self.maxzoom = info.maxzoom
        self.mosaic_def = MosaicJSON.from_features(features, minzoom=info.minzoom, maxzoom=info.maxzoom)


    def write(self, overwrite: bool = True):
        """This method is not used but is required by the abstract class."""
        pass

    def update(self):
        """We overwrite the default method."""
        pass

    def _read(self) -> MosaicJSON:
        """This method is not used but is required by the abstract class."""
        pass

    def assets_for_tile(self, x: int, y: int, z: int) -> List[str]:
        """Retrieve assets for tile."""
        return self.get_assets()

    def assets_for_point(self, lng: float, lat: float) -> List[str]:
        """Retrieve assets for point."""
        return self.get_assets()

    def get_assets(self) -> List[str]:
        """assets are just files we give in path"""
        return self.input

    @property
    def _quadkeys(self) -> List[str]:
        return []
