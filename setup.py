from setuptools import find_packages, setup

setup(
    name='HouseScrape',
    version='0.1',
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
        'datetime'
    ],

    # metadata to display on PyPI
    author="Benji Levine",
    author_email="benjilev08@gmail.com"
)
