from setuptools import setup, find_packages

setup(name='leetcode_cli',
      version='0.1.0',
      description='A CLI tool to access LeetCode',
      author='Jakub Kubiak',
      packages=find_packages(),
      entry_points={'console_scripts': ['leet = leetcode.main:main'],},
      package_data={'': ['*.yaml', '*.graphql']},
      )