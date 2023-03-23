from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='vad',
    version='1.0.2',
    description='VAD - Simple Voice Activity Detection',
    py_modules=["EnergyVAD"],
    packages=find_packages(include=['vad', 'vad.*']),
    classifiers={
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    },
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires = [
        "numpy",
    ],
    extras_require = {
    },
    url="https://github.com/MorenoLaQuatra/vad",
    author="Moreno La Quatra",
    author_email="moreno.laquatra@gmail.com",
)