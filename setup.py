from setuptools import setup, find_packages

setup(name='cotegen',
      version='0.1',
      url='https://github.com/kaist-cs453-2019s-team7/cs453-team-project',
      author='Team7',
      author_email='suchan.park@kaist.ac.kr',
      description='KAIST CS453 2019 Spring Team 7 Project',
      packages=find_packages('cotegen'),
      package_dir={'': 'cotegen'},
      setup_requires=['astor>=0.8.0'])
