import friend

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

version = friend.__version__
url = 'https://github.com/cloudboss/friend/releases/{}'.format(version)

config = {
    'description': 'Python utility library',
    'long_description': readme,
    'author': 'Joseph Wright',
    'url': 'https://github.com/cloudboss/friend',
    'download_url': url,
    'author_email': 'joseph@cloudboss.co',
    'version': version,
    'install_requires': [
        'ipaddress',
    ],
    'packages': ['friend'],
    'name': 'friend',
    'test_suite': 'tests',
}

setup(**config)
