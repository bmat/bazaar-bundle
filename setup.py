# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bazaar_bundle']

package_data = \
{'': ['*']}

install_requires = \
['applauncher>=2.0.0,<3.0.0', 'bazaar>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'bazaar-bundle',
    'version': '2.0.0',
    'description': 'Bazaar support for applauncher',
    'long_description': None,
    'author': 'Alvaro Garcia',
    'author_email': 'agarcia@bmat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0.0',
}


setup(**setup_kwargs)
