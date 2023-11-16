from setuptools import setup, find_packages

setup(
    name='gmon',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gmon=gmon.monitor:main',
        ],
    },
    install_requires=[
        'termcolor',
    ],
    description='GPU monitoring tool for Python scripts',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
