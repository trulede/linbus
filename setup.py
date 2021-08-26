import os
from setuptools import setup, find_packages


install_requires =  [
    'redis',
]


DESCRIPTION = """
LIN Bus Library.
"""


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read().strip()


setup(
    name='linbus',
    version=os.getenv('PACKAGE_VERSION', 'devel'),
    author='Timothy Rule',
    author_email='trule.de@gmail.com',
    license='MIT',
    description='LIN Bus Library',
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/trulede/linbus',
    keywords='LIN LINBUS',
    packages=find_packages(include=['linbus']),
    python_requires='>=3.8',
    install_requires=install_requires,
    setup_requires=[],
    entry_points={
        'console_scripts' : [
            'lin.master=linbus.master:main',
            'lin.slave=linbus.slave:main',
            'lin.monitor=linbus.monitor:main',
        ],
    },

    classifiers=[
        "License :: MIT",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: LIN Bus",
        "Topic :: Hardware Development :: LIN Bus",
    ],
)
