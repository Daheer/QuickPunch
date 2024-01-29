from transformers import pipeline
from pathlib import Path
from tqdm import tqdm

from QuickPunch.utils import get_supabase, bin_colors, logger
from QuickPunch.entity import CategorizationConfig
from QuickPunch.config.configuration import ConfigurationManager

# The `Categorization` class provides methods for categorizing summaries of text or information using
# a pre-trained text classification model and updating the category field in a Supabase table for each
# article.
class Categorization: 
  def __init__(self, config: CategorizationConfig):
    self.config = config
    self.supabase = get_supabase()
    self.categorizer = None

  def categorize(self, summary: str) -> str:    
    """
    The `categorize` function takes a summary as input and uses a categorizer to determine the
    category of the summary. If the score of the category is above a certain threshold, it returns the
    label of the category capitalized. Otherwise, it returns "wildcard" capitalized.
    
    :param summary: The `summary` parameter is a string that represents a summary of some text or
    information. It is used as input for the categorization process
    :type summary: str
    :return: a string. If the score of the categorizer result is greater than the threshold specified
    in the config, it returns the capitalized label of the result. Otherwise, it returns "wildcard"
    capitalized.
    """
    result = self.categorizer(summary)[0]
    if result["score"] > self.config.threshold:
      return result["label"].capitalize()
    else:
      return "wildcard".capitalize()

  def categorize_articles(self):
    """
    The `categorize_articles` function categorizes articles by using a pre-trained text classification
    model and updates the category field in a Supabase table for each article.
    """
    self.categorizer = pipeline("text-classification", model=self.config.model_path)
    logger.info(f"{bin_colors.INFO}Getting articles to categorize.{bin_colors.ENDC}")
    response = self.supabase.table("entries").select("*").execute()
    for entry in tqdm(response.data, desc="Categorizing articles", total=len(response.data)):
      category = self.categorize(entry["summary"])
      self.supabase.table("entries").update({'category': category}).eq('id', entry['id']).execute()