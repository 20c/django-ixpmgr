from setuptools import setup, find_packages


def read_file(name):
    with open(name) as fobj:
        return fobj.read().strip()


LONG_DESCRIPTION = read_file("README.md")
VERSION = read_file("Ctl/VERSION")

setup(
    name="django-ixpmgr",
    version=VERSION,
    author="20C",
    author_email="code@20c.com",
    description="django overlay for IXP-Manager",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="LICENSE.txt",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    url="https://github.com/20c/django-ixpmgr",
    download_url=f"https://github.com/20c/django-ixpmgr/archive/{VERSION}.zip",
    install_requires=["semver==2.10.2"],
    zip_safe=False,
)
