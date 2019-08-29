from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],

    # metadata to display on PyPI
    author="Benji Levine",
    author_email="benjilev08@gmail.com"
)
