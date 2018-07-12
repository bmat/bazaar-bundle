from setuptools import setup

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name='bazaar_bundle',
    packages=['bazaar_bundle'],
    version='0.1',
    description='Bazaar support for applauncher',
    author='Alvaro Garcia Gomez',
    author_email='maxpowel@gmail.com',
    url='https://github.com/applauncher-team/bazaar_bundle',
    download_url='https://github.com/applauncher-team/bazaar_bundle/archive/master.zip',
    keywords=['bazaar', 'mongo', 's3', 'applauncher'],
    classifiers=['Topic :: Adaptive Technologies', 'Topic :: Software Development', 'Topic :: System',
                 'Topic :: Utilities'],
    install_requires=install_requires
)
