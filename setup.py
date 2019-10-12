# coding=utf-8

from setuptools import setup, find_packages

setup(name="media_server_utils",
      version="0.1.0",
      options={},
      description="Various utils to manage a Media Server",
      author="carlba",
      packages=find_packages(),
      install_requires=['click'],
      entry_points={
          'console_scripts': [
              'add_torrents_from_folder = media_server_utils.cli:add_torrents_from_folder'
          ]
      }
      )
