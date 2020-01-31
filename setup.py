import setuptools

setuptools.setup(
    name="python",
    version="1.0",
    packages=setuptools.find_packages(exclude=["tests"]),
    setup_requires=[""],
    tests_require=[""],
    classifiers=["Programming Language :: Python :: 3"],
)