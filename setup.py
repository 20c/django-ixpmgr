
from setuptools import setup

setup(
    name='django-ixpmgr',
    packages=['ixpmgr'],
    version=open('facsimile/VERSION').read().rstrip(),
    author='20C',
    author_email='code@20c.com',
    description='django overlay for IXP-Manager',
    long_description=open('README.txt').read(),
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=False
)
