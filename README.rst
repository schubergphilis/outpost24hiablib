============
outpost24lib
============

A python library for interfacing with Outpost24 HIAB api


* Documentation: https://outpost24lib.readthedocs.org/en/latest


Important Information
=====================

This template is based on pipenv. In order to be compatible with requirements.txt so the actual created package can be used by any part of the existing python ecosystem some hacks were needed.
So when building a package out of this **do not** simple call

    $ python setup.py sdist bdist_egg

**as this will produce an unusable artifact with files missing.**
Instead use the provided build and upload scripts that create all the necessary files in the artifact.



Project Features
================

* Manages users, usergroups, targets, targetgroups


Todo
====

* This code is MVP. It requires a lot of optimizations and extensions.
* Things to do are, try to make the retrieving faster and implement smart caching for entities.
