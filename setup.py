import setuptools

with open("buspy/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="buspy",
    version="0.0.1",
    author="Gustaw Blachowski",
    author_email="gustaw.blachowski@gmail.com",
    description="Bus data reader package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GustawB/BUS_DATA_READER",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
