from distutils.core import setup

setup(
    name='pydis',
    packages=['pydis'],
    version='0.2',
    description='Python wrappers for StrictRedis',
    author='masayang',
    author_email='masayang@msushi.com',
    url='https://github.com/masayang/py_redis',
    download_url='https://github.com/masayang/py_redis/archive/0.2.tar.gz',
    requires=['redis', 'python_dotenv'],
    keywords=['redis'],
    classifiers=[],
)
