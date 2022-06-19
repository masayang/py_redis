# pydis

Python wrappers for StrictRedis inspired by https://blog.jverkamp.com/2015/07/16/automagically-storing-python-objects-in-redis/

<a href='https://coveralls.io/github/masayang/py_redis?branch=master'><img src='https://coveralls.io/repos/github/masayang/py_redis/badge.svg?branch=master' alt='Coverage Status' /></a>

## Installation

pip install -U pydis

## Configuration

See redis_settings.py for detail.

## Usage

See tests/sample.py

## test
python -m pytest --cov-report term-missing --cov=pydis 
