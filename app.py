#!/usr/bin/env python3

from gevent import monkey; monkey.patch_all()

import json
import bottle
import logging
from lib.freguesias import Freguesias
from bottle import request, response

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

app = application = bottle.Bottle()
app.config['freguesias'] = Freguesias.getData()

def polyPoint(lat, lon):
    logger.info('Checking for point (%f, %f)' % (lat, lon))
    for poly in app.config['freguesias']:
        if poly['path'].contains_point((lat, lon, )):
            return poly['info']
    return False


@app.get('/')
def callback():
    response.set_header('Content-Type', 'application/json; charset=utf-8')

    lat = request.query.lat
    lon = request.query.lon

    if lat is None or lon is None:
        return "{'error': 'both lat and lon parameters are required'}"

    try:
        lat = float(lat)
        lon = float(lon)
    except:
        return "{'error': 'both lat and lon must be numbers'}"

    result = polyPoint(lat, lon)
    if result is False:
        return "{'error': 'unknown location'}"

    return json.dumps(result, ensure_ascii=False)

if __name__ == '__main__':
    app.run(
        host='localhost',
        port=8080,
        debug=True,
    )
