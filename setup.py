
from setuptools import setup, find_packages

setup(
    name='jma_data_tools',
    version='0.1.0',
    description='Utilities for downloading and visualizing JMA ground and upper-air data',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/yourusername/jma_data_tools',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'requests',
        'beautifulsoup4',
        'metpy',
        'matplotlib',
        'cartopy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
