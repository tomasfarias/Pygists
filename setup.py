from setuptools import find_packages, setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='pygists',
    version='0.1',
    author='Tomas Farias',
    author_email='tomasfariassantana@gmail.com',
    description='CLI tool to operate with the GitHub Gists API.',
    long_description=readme(),
    packages=find_packages(exclude=['tests', 'docs']),
    license='MIT',
    url='https://github.com/tomasfarias/pygists',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Implementation :: CPython',
        'Operating System :: OS Independent'
    ]
)
