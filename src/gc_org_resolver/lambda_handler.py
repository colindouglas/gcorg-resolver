from mangum import Mangum

from gc_org_resolver.app import create_app

handler = Mangum(create_app(), lifespan="off")
