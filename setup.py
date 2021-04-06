import sys

required_verion = (3,6)
if sys.version_info < required_verion:
    raise ValueError('needs at least python {}! You are trying to install it under python {}'.format('.'.join(str(i) for i in required_verion), sys.version))

# import ez_setup
# ez_setup.use_setuptools()

from setuptools import setup
# from distutils.core import setup
setup(
    name="pops_gui",
    version="0.1",
    packages=['pops_gui'],
    author="Hagen Telg",
    author_email="hagen@hagnet.net",
    description="GUI for POPS",
    license="MIT",
    keywords="POPS gui",
    url="https://github.com/hagne/pops_gui",
    # scripts=['scripts/scrape_sat', 
    #          # 'scripts/hrrr_smoke2gml'
    #          ],
    # install_requires=['numpy','pandas'],
    # extras_require={'plotting': ['matplotlib'],
    #                 'testing': ['scipy']},
    # test_suite='nose.collector',
    # tests_require=['nose'],
)