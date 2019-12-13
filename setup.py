from setuptools import find_packages, setup
setup(
    name='Choys',
    version='0.3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'datetime',
        'flask',
        'flask_sqlalchemy',
        'psycopg2',
        'requests',
        'scrapy',
        'SQLAlchemy',
        'Twisted>=19.7.0',
    ],

    # metadata to display on PyPI
    author="Benji Levine",
    author_email="benji@benjilevine.com",
    url='https://github.com/benjilev08/Choys'
)
