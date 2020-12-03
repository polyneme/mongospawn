from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mongospawn",
    url="https://github.com/polyneme/mongospawn",
    packages=find_packages(),
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    author="Donny Winston",
    author_email="donny@polyneme.xyz",
    description="Spawn MongoDB resources from JSON Schema",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires=">=3.6",
)
