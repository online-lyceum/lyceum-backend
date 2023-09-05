from setuptools import setup, find_packages

install_requires = [
    'asyncpg',
    'pydantic',
    'fastapi',
    'uvicorn',
    'sqlalchemy[asyncio]',
    'gunicorn'
]

setup(
    name='lyceum_backend',
    version="0.0.3.dev1",
    description='Time Managment API',
    platforms=['POSIX'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'init_models = lyceum_backend.db.base:run_init_models',
            'init_db = lyceum_backend.db.create:run_init_db',
        ]
    }
)
