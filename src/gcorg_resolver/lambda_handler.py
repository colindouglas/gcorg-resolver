from mangum import Mangum

from gcorg_resolver.app import create_app

handler = Mangum(create_app(), lifespan="off")
