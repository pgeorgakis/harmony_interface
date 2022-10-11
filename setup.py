import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="harmony_interface",
    version="0.0.1",
    author="Ilias, Shakur",
    author_email='shakur.sarder@tum.de',
    description="A function that returns 'world'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/MobyX-HARMONY/harmony_interface.git',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
