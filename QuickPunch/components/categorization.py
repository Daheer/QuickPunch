from transformers import pipeline
from pathlib import Path
from tqdm import tqdm

from QuickPunch.utils import get_supabase, bin_colors, logger
from QuickPunch.entity import CategorizationConfig
from QuickPunch.config.configuration import ConfigurationManager

class Categorization: 
  def __init__(self, config: CategorizationConfig):
    self.config = config
    self.supabase = get_supabase()
    self.categorizer = None

  def categorize(self, summary: str) -> str:
    result = self.categorizer(summary)[0]
    if result["score"] > self.config.threshold:
      return result["label"].capitalize()
    else:
      return "wildcard".capitalize()

  def categorize_articles(self):
    self.categorizer = pipeline("text-classification", model=self.config.model_path)
    logger.info(f"{bin_colors.INFO}Getting articles to categorize.{bin_colors.ENDC}")
    response = self.supabase.table("entries").select("*").execute()
    for entry in tqdm(response.data, desc="Categorizing articles", total=len(response.data)):
      category = self.categorize(entry["summary"])
      self.supabase.table("entries").update({'category': category}).eq('id', entry['id']).execute()