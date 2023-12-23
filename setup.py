from setuptools import setup, find_packages

setup(
    name='trch-file-recoverer',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'recover-files=recover_files.recover_files:main',
        ],
    },
)