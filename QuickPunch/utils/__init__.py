from typing import List, Dict, Any
import yaml
from pathlib import Path
import os
from supabase import create_client, Client
import dotenv
from bs4 import BeautifulSoup
import requests
from box.exceptions import BoxValueError
# from ensure import ensure_annotations
from box import ConfigBox
import ssl
import smtplib
from email.message import EmailMessage


# @ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
  """
  Read a yaml file and return a ConfigBox object.
  """
  try:
    with open(path_to_yaml, "r") as yaml_file:
      yaml_dict = yaml.safe_load(yaml_file)
      logger.info(f"yaml file: {yaml_file.name} read successfully.")
      return ConfigBox(yaml_dict)
  except BoxValueError:
    raise ValueError(f"Error reading yaml file at {path_to_yaml}.")
    logger.error(f"Error reading yaml file at {path_to_yaml}.")
  except Exception as e:
    raise e
    logger.error(f"Error reading yaml file at {path_to_yaml}.")

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
  SUPABASE_URL = os.getenv("SUPABASE_URL")
  SUPABASE_KEY = os.getenv("SUPABASE_KEY")
  logger.info(f"{bin_colors.INFO}Connecting to database at {SUPABASE_URL}.{bin_colors.ENDC}")
  supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
  if supabase is None:
    logger.error(f"{bin_colors.ERROR}Error connecting to database at {SUPABASE_URL}.{bin_colors.ENDC}")
    raise Exception("Error connecting to database.")
  logger.info(f"{bin_colors.SUCCESS}Connected to database at {SUPABASE_URL}.{bin_colors.ENDC}")
  return supabase


def read_article(link: str) -> str:
  """
  Read the article from the link.
  """
  response = requests.get(link)
  soup = BeautifulSoup(response.content, 'html.parser')
  article = []
  post_content = soup.find('div', class_='post-content')
  for p in post_content.find_all('p'):
    article.append(p.text)

  return "".join(article)

def send_email(email: str, message: str) -> None:
    """
    Send an email to a user.
    """
    dotenv.load_dotenv()

    email_sender = "quick.punch.daily@gmail.com"
    email_password = os.getenv("APP_PASSWORD")

    email_receiver = email
    subject = "Your daily digest from QuickPunch"

    # Use HTML formatting with inline CSS for the border
    body = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <style>
                    .email-body {{
                      font-family: Arial;
                      font-size: 14px;
                    }}
                    .article {{
                      border: 1px solid black;
                      padding: 10px;
                      border-radius: 5px;
                      margin-bottom: 10px;
                      box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
                    }}
                    .greeting {{
                      display: flex;
                      align-items: center;
                      justify-content: center;
                      border-radius: 3px;
                      border: 1px solid black;
                      padding: 5px;
                    }}
                    .hero {{
                      height: 100px;
                      width: 100%;
                      border-radius: 5px;
                      background: rgba(255, 255, 255, 0.8);
                      background: url('https://64.media.tumblr.com/91d00b07096a6b02b2b240ac4f436707/debc7e0e3a58a66d-54/s250x400/fe81635fe446e3c2b87ab319eabe205f5fcc92af.jpg');
                      background-position: center;
                      background-size: contain;
                    }}
                </style>
            </head>
            <body>
                <div class="email-body">
                    {message}
                </div>
            </body>
        </html>
    """

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, em.as_string())
