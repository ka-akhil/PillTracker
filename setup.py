from setuptools import setup, find_packages
from typing import List


HYPEN_E_DOT = "-e ."


def get_requirements(file_path: str = 'requirements.txt') -> List[str]:
    """
    Reads a file containing requirements and returns a list of requirements.

    Args:
        file_path (str): The path to the file containing requirements. Defaults to 'requirements.txt'.

    Returns:
        List[str]: A list of requirements read from the file.
    """
    try:
        with open(file_path) as file_obj:
            return [line for line in file_obj.read().splitlines() if line != HYPEN_E_DOT]
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []


setup(
    name='pilltracker', version='1.0.0',
    author='akhi-ka',
    author_email='k.akhil.asok@gmail.com',
    description='A Python package for tracking pills',
    packages=find_packages(),
    install_requires=get_requirements('requirement.txt'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)
