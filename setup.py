from setuptools import setup, find_packages


def read_file(name):
    with open(name) as fobj:
        return fobj.read().strip()


LONG_DESCRIPTION = read_file("README.md")
VERSION = read_file("Ctl/VERSION")
# REQUIREMENTS = read_file("Ctl/requirements.txt").split("\n")
# TEST_REQUIREMENTS = read_file("Ctl/requirements-test.txt").split("\n")


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
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages("src", "ixpmgr"),
    package_dir={"": "src"},
    include_package_data=True,
    # install_requires=REQUIREMENTS,
    # test_requires=TEST_REQUIREMENTS,
    url="https://github.com/20c/django-ixpmgr",
    download_url=f"https://github.com/20c/django-ixpmgr/archive/{VERSION}.zip",
    install_requires=["django_extensions", "packaging"],
    zip_safe=False,
)
