"""routes.

app/router.py

"""

from dataclasses import dataclass
from typing import List

from fastapi import Query

from titiler.mosaic.factory import MosaicTilerFactory
from .backends import MultiFilesBackend


@dataclass
class MosaicTiler(MosaicTilerFactory):
    """Custom MosaicTilerFactory.

    Note this is a really simple MosaicTiler Factory with only few endpoints.
    """

    def register_routes(self):
        """This Method register routes to the router. """

        self.tile()
        self.tilejson()


def DatasetPathParams(url: str = Query(..., description="Dataset URL")) -> List[str]:
    """Create dataset path from args"""
    return url.split(",")


mosaic = MosaicTiler(reader=MultiFilesBackend, path_dependency=DatasetPathParams)
