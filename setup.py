from setuptools import setup, find_packages
from vkmusix import __version__

setup(
    name="vkmusix",
    version=__version__,
    description="Библиотека для работы с VK Music. Документация: https://to4no4sv.gitbook.io/vkmusix.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="thswq",
    author_email="admin@vkmusix.ru",
    url="https://github.com/to4no4sv/vkmusix",
    packages=find_packages(),
    install_requires=[
        "httpx == 0.27.0",
        "aiofiles == 24.1.0",
        "pycryptodome == 3.20.0",
        "av == 13.1.0",
        "mutagen == 1.47.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)