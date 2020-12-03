from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements/main.in") as fh:
    install_requires = fh.read().splitlines()

with open("requirements/dev.in") as fh:
    extras_require_dev = fh.read().splitlines()

setup(
    name="mongospawn",
    url="https://github.com/polyneme/mongospawn",
    packages=find_packages(),
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    install_requires=install_requires,
    extras_require={
        "dev": extras_require_dev,
    },
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
