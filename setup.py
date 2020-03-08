from setuptools import find_packages
from setuptools import setup
import os
from pathlib import Path

REQUIREMENTS = Path(os.path.dirname(os.path.realpath(__file__))) / "requirements.txt"

with open(REQUIREMENTS, 'r') as f:
    requirements = f.readlines()

setup(
    name="antipodal",
    version="0.1.0",
    author="Jack Wardell",
    author_email="jackwardell@me.com",
    description="cli tool for using antipodal",
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points="""
    [console_scripts]
    wanc=manage:cli
    """,
    install_requires=requirements,
)
