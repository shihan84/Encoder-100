#!/usr/bin/env python3
"""
Setup script for TSDuck GUI
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="tsduck-gui",
    version="1.0.0",
    author="TSDuck GUI Team",
    author_email="tsduck-gui@example.com",
    description="A comprehensive GUI application for MPEG Transport Stream processing using TSDuck",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/tsduck-gui/tsduck-gui",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "monitoring": ["psutil>=5.9.0"],
        "influxdb": ["influxdb-client>=1.30.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-qt>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tsduck-gui=tsduck_gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json"],
    },
    keywords="tsduck, mpeg, transport-stream, scte35, gui, streaming, dvb, atsc, isdb",
    project_urls={
        "Bug Reports": "https://github.com/tsduck-gui/tsduck-gui/issues",
        "Source": "https://github.com/tsduck-gui/tsduck-gui",
        "Documentation": "https://github.com/tsduck-gui/tsduck-gui/wiki",
    },
)
