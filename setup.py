from setuptools import find_packages, setup

from shitcord import __version__

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# No extra requirements at the moment ¯\_(ツ)_/¯
extra_requires = {}

setup(
    name='Shitcord',
    version=__version__,
    author='Valentin B.',
    author_email='itisvale1@gmail.com',
    description='A framework to interact with the Discord API.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/itsVale/Shitcord',
    license='GNU General Public License v3 (GPLv3)',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extra_requires=extra_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
