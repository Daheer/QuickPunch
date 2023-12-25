import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

project_name = "QuickPunch"

list_of_files = [
  ".github/workflows/.gitkeep",
  f"{project_name}/__init__.py",
  f"{project_name}/components/__init__.py",
  f"{project_name}/utils/__init__.py",
  f"{project_name}/utils/common.py",
  f"{project_name}/logging/__init__.py",
  f"{project_name}/config/__init__.py",
  f"{project_name}/config/configuration.py",
  f"{project_name}/pipeline/__init__.py",
  f"{project_name}/entity/__init__.py",
  f"{project_name}/constants/__init__.py",
  "config/config.yaml",
  "params.yaml",
  "app.py",
  "main.py",
  "Dockerfile",
  "requirements.txt",
  "setup.py",
  "research/trials.ipynb",
]

for filepath in list_of_files:
  path = Path(filepath)
  filedir, filename = os.path.split(filepath)
  if filedir != "":
    os.makedirs(filedir, exist_ok=True)
    logging.info(f"Created directory: {filedir}")
  if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
    with open(filepath, "w") as f:
      pass
      logging.info(f"Created empty file: {filepath}")
  else:
    logging.info(f"{filepath} already exists.")
