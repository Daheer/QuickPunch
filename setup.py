from setuptools import setup, find_packages
from typing import List

with open("README.md", "r") as fh:
  long_description = fh.read()

AUTHOR_USER_NAME = 'Daheer'
REPO_NAME = 'QuickPunch'

def get_requirements(file_path: str='requirements.txt') -> List[str]:
  with open(file_path) as f:
    requirements = f.read().splitlines()
  if '-e .' in requirements:
    requirements.remove('-e .')
  return requirements

setup(
  name='QuickPunch',
  version='1.0.0',
  description='See your e-commerce products in 3D',
  author='Dahiru Ibrahim',
  long_description=long_description,
  author_email='suhayrid6@gmail.com',
  packages=find_packages(),
  long_description_content_type="text/markdown",
  url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
  project_urls={
    "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
  },
  install_requires=get_requirements(),
  python_requires=">=3.6",
)