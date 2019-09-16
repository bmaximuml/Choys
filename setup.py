from setuptools import find_packages, setup

setup(
    name='HouseScrape',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'psycopg2',
        'flask_sqlalchemy',
        'scrapy',
        'requests',
        'Twisted==18.9.0',
        'SQLAlchemy',
        'requests',
        'datetime',
        'pytest-flask-sqlalchemy',
        'pytest_postgresql'
    ],

    # metadata to display on PyPI
    author="Benji Levine",
    author_email="benji@benjilevine.com",
    url='https://github.com/benjilev08/HouseScrape'
)
