"""
QuikDel: A Novel & Scalable Q-learning Based Distributed Approach for Efficient Long-haul Delivery
MSCS Thesis Project - Miami University

Setup configuration for the QuikDel package.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="quikdel",
    version="1.0.0",
    author="Robert Kilgore",
    author_email="kilgorrj@miamioh.edu",
    description="Distributed Q-learning framework for scalable urban food delivery optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quikdel",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/quikdel/issues",
        "Research Paper": "https://github.com/yourusername/quikdel/blob/main/docs/QuikDel_IEEE_TITS.pdf",
        "Documentation": "https://github.com/yourusername/quikdel/blob/main/docs/",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "jupyterlab>=3.0.0",
        ],
        "viz": [
            "cartopy>=0.19.0",
            "contextily>=1.1.0",
            "plotly>=5.0.0",
        ],
        "performance": [
            "memory-profiler>=0.58.0",
            "psutil>=5.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "quikdel-extract=qcense.extract_city_data:main",
            "quikdel-train=src.training.agent_training:main",
            "quikdel-simulate=src.simulation.run_simulation:main",
            "quikdel-analyze=src.analysis.comparative_analysis:main",
        ],
    },
    include_package_data=True,
    package_data={
        "quikdel": ["config/*.yaml", "docs/*.md"],
    },
    keywords=[
        "reinforcement-learning",
        "q-learning",
        "food-delivery",
        "urban-logistics",
        "distributed-systems",
        "ride-sharing",
        "multi-agent-systems",
        "geospatial-analysis",
        "census-data",
        "openstreetmap",
    ],
)
