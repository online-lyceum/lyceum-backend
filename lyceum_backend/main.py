import logging

from fastapi import FastAPI

from lyceum_backend import api


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(process)s] [%(levelname)s] "
           "(%(filename)s:%(lineno)d) %(msg)s"
)
logger = logging.getLogger(__name__)
logger.info('Logger start work')


def create_application():
    application = FastAPI(
        openapi_url='/api/openapi.json',
        docs_url='/api/docs',
        redoc_url='/api/redoc',
        logger=logger
    )
    application.include_router(api.hello.router)
    application.include_router(api.user.router)
    application.include_router(api.auth.router)
    return application


app = create_application()
