# setup.py
from setuptools import setup, find_packages

setup(
    name="code-counter",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "python-fire",
    ],
    entry_points={
        "console_scripts": [
            "code-count=code_counter.cli:main",
        ],
    },
    author="Xiyuan Yang",
    author_email="yangxiyuan@sjtu.edu.cn",
    description="A utility to count lines of code in a repository.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xiyuanyang-code/Repo-Code-Line-Counting",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
)
