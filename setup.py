from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='trch-file-recoverer',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'recover-files=file_recoverer.file_recoverer:main',
        ],
    },
    # NEW ADDITIONS BELOW
    long_description=long_description,  # Set the long description to the README contents
    long_description_content_type='text/markdown',  # Specify the content type as Markdown
)
