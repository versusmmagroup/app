from setuptools import setup

requires = (
        "flask",
        "flask_mysqldb",
        "wtforms",
        "passlib.hash",
        "functools",
        "flask_moment",
        )

setup(
    name = "VersusApp Package",
    version = "0.0.1",
    author = "VersusAdmin",
    author_email = "versusmmagroup@icloud.com",
    description = ("app"),
    license = "BSD",
    keywords = "versus",
    url = "http://versusmmagroup.com",
    packages=['VersusApp',],
    # namespace_packages = ['package_name'],
    install_requires=requires,
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)