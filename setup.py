from setuptools import setup, find_packages

setup(name='Leetcode API Client',
      version='0.1',
      packages=find_packages(),
      entry_points={'console_scripts': ['leet = leetcode.main:main'],},
      package_data={'': ['*.yaml', '*.graphql']},
      )