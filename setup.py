import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cotegen',
    version='0.0',
    url='https://github.com/kaist-cs453-2019s-team7/cs453-team-project',
    author='Team7',
    author_email='suchan.park@kaist.ac.kr',
    description='KAIST CS453 2019 Spring Team 7 Project',
    setup_requires=['astor>=0.8.0', 'anytree>=2.6.0'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)