from asgiref.wsgi import WsgiToAsgi
from mangum import Mangum

from gcorg_resolver.app import create_app

handler = Mangum(WsgiToAsgi(create_app()), lifespan="off")
