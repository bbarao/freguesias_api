import json
import matplotlib.path as mplPath
import logging
from zipfile import ZipFile

logger = logging.getLogger(__name__)


class Freguesias():

    polyData = None

    @classmethod
    def getData(cls):
        if cls.polyData is None:
            tmpPolyData = []
            geoData = None
            logger.info('Loading JSON')
            with ZipFile('./lib/freguesias.zip') as zipf:
                with zipf.open('freguesias.min.json') as f:
                    geoData = json.load(f)

            logger.info('Converting Data')
            for poly in geoData:
                polyPath = mplPath.Path(poly['geometry'])
                del poly['geometry']
                tmpPolyData.append({'info': poly, 'path': polyPath})

            logger.info('Done')

            cls.polyData = tmpPolyData
        return cls.polyData
