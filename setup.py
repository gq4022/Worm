import setuptools

with open("README.md", mode="r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name = "worm-package-zyuomo",
    version = "0.0.1",
    author = "zyuomo",
    author_email = "r4nd0mmachine@gmail.com",
    description = "todo",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/zyuomo/Worm",
    project_urls = {
        "Bug Tracker": "https://github.com/zyuomo/Worm/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating SYstem :: OS Independent",
    ],
    package_dir = {"": "srv"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6",
)