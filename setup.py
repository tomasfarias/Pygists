from setuptools import find_packages, setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='pygists',
    version='1.1.0',
    author='Tomas Farias',
    author_email='tomasfariassantana@gmail.com',
    description='CLI tool to operate with the GitHub Gists API.',
    scripts=['bin/pygists'],
    long_description=readme(),
    packages=find_packages(exclude=['tests', 'docs']),
    license='MIT',
    url='https://github.com/tomasfarias/Pygists',
    install_requires=[
        'requests==2.24.0'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent'
    ]
)
