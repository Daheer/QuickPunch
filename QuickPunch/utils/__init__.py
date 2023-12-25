from typing import List, Dict, Any
import yaml
from pathlib import Path
from ensure import ensure_annotations
from box import ConfigBox
import os
from supabase import create_client, Client
import dotenv

from QuickPunch.logging import logger

class bin_colors:
  HEADER = '\033[95m'
  INFO = '\033[94m'
  OKCYAN = '\033[96m'
  SUCCESS = '\033[92m'
  WARNING = '\033[93m'
  ERROR = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def create_directory(path: Path) -> None:
  """
  Create a directory if it does not exist.
  """
  try:
    if not os.path.exists(path):
      os.makedirs(path)
      logger.info(f"{bin_colors.INFO}Directory created at {path}.{bin_colors.ENDC}")
  except Exception as e:
    logger.error(f"{bin_colors.ERROR}Error creating directory at {path}.{bin_colors.ENDC}")
    raise e
  

def get_supabase():
  """
  Get the database connection.
  """
  dotenv.load_dotenv()
  supabase_url = os.getenv("SUPABASE_URL")
  supabase_key = os.getenv("SUPABASE_KEY")
  logger.info(f"{bin_colors.INFO}Connecting to database at {supabase_url}.{bin_colors.ENDC}")
  supabase = create_client(supabase_url, supabase_key)
  if supabase is None:
    logger.error(f"{bin_colors.ERROR}Error connecting to database at {supabase_url}.{bin_colors.ENDC}")
    raise Exception("Error connecting to database.")
  logger.info(f"{bin_colors.SUCCESS}Connected to database at {supabase_url}.{bin_colors.ENDC}")
  return supabase