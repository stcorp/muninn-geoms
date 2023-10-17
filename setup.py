from setuptools import setup

setup(
    name='muninn-geoms',
    version='1.0',
    description="Muninn namespace extension for GEOMS metadata",
    url="https://github.com/stcorp/muninn-geoms",
    author="S[&]T",
    license="BSD",
    py_modules=['muninn_geoms'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Environment :: Plugins",
    ],
    install_requires=["muninn"],
)
