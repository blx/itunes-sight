from setuptools import setup

setup(
    name='Sight',
    version='1.0',
    long_description=__doc__,
    packages=['sight'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)