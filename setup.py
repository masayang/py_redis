from setuptools import setup

setup(
    name='pydis',
    packages=['pydis'],
    version='0.6.1',
    description='Python wrappers for StrictRedis',
    author='masayang',
    author_email='masayang@msushi.com',
    url='https://github.com/masayang/py_redis',
    install_requires=['redis>=2.10', 'python_dotenv>=0.6.5'],
    zip_safe=False
)
