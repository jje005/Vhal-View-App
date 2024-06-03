from setuptools import setup, find_packages

setup(
    name = 'VHAL Controller',
    version = '0.0.1',
    packages=find_packages(include=['commands', 'core', 'model', 'vcan', 'network']),
    install_requires=[
        'python-can>=4.3.1',
        'typer>=0.12.3',
        'typing_extensions>=4.12.0'
    ],
    entry_points={
        "console_scripts": [
            "vhal-cli=commands.Vhal_api:app",
        ],
    },

    dependency_links = [
        'https://github.com/jje005/Vhal-View-App.git'
    ]
)