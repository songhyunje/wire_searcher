import setuptools

install_requires = [
    'elasticsearch'
    'elasticsearch_dsl'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wire-searcher",  # Replace with your own username
    version="0.0.1",
    author="Hyun-Je Song",
    author_email="songhyunje@gmail.com",
    description="A search interface used in WIRE summarization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/songhyunje/wire_searcher",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
