import os
import ujson
import cv2
import numpy        as np
from jinja2         import Template
from sanic          import Sanic
from sanic.response import html, file, text, empty, HTTPResponse
from dotmap         import DotMap
from subprocess     import call


with open( "./config.json", 'r' ) as file_pointer:
    config = DotMap( ujson.load( file_pointer ) )

with open( 'template.html', 'r' ) as file_pointer:
    template = Template( "".join( file_pointer.readlines() ) )

app = Sanic( "PLEX webhook listener" )


def save_thumbnail( body ):
    array = np.frombuffer( body, np.uint8 )
    image = cv2.imdecode( array, cv2.IMREAD_COLOR )
    cv2.imwrite( "thumb.jpeg", image )
    return


@app.route( "/thumb.jpeg" )
async def handler( request ):
    return await file("./thumb.jpeg")


@app.route( "/" )
async def handler( request, methods = ['GET'] ):
    return await file( "./now-playing.html" )


@app.route("/", methods = ['POST'] )
async def handle_plex( request ):
    payload = DotMap( ujson.loads( request.form['payload'][0] ) )
    print( f"{payload.event}" )

    if request.files:
        save_thumbnail( request.files['thumb'][0].body )
        pass

    if "plexamp" not in payload.Player.title:
        return empty()

    data = DotMap({
        'status'        : 'playing',
        'artist'        : payload.Metadata.grandparentTitle,
        'album'         : payload.Metadata.parentTitle,
        'year'          : payload.Metadata.parentYear,
        'title'         : payload.Metadata.title,
        'thumb'         : payload.Metadata.thumb,
        'dominant_color': "",
    })

    # payload.pprint()

    with open( './now-playing.html', 'w' ) as file_pointer:
        file_pointer.write( template.render( **data, reload = True ) )

    return empty()



def main():
    app.run( host = '0.0.0.0', port = config.plex.webhook.port, auto_reload = True, debug = False )
    return


if __name__ == '__main__':
    main()
