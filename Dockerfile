FROM python:3.11
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY setup.py ./
COPY lyceum_backend ./time_manager
RUN pip install .
CMD cd time_manager && \
        init_db && \
        alembic -c ./alembic.prod.ini upgrade head && \
        cd /app && \
        gunicorn time_manager.main:app -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80
