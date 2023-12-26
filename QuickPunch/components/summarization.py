from transformers import pipeline
from pathlib import Path
from tqdm import tqdm

from QuickPunch.utils import get_supabase, bin_colors, logger
from QuickPunch.entity import SummarizationConfig
from QuickPunch.config.configuration import ConfigurationManager

class Summarization:
  def __init__(self, config: SummarizationConfig):
    self.config = config
    self.supabase = get_supabase()
    self.summarizer = None

  def summarize(self, article: str) -> str:
    summary = self.summarizer(article, min_length=self.config.min_length, max_length=self.config.max_length, truncation=True, do_sample=bool(self.config.do_sample))  
    return summary[0]['summary_text']

  def summarize_articles(self):
    self.summarizer = pipeline("summarization", model=self.config.model_path)
    logger.info(f"{bin_colors.INFO}Getting articles to summarize.{bin_colors.ENDC}")
    response = self.supabase.table("entries").select("*").execute()
    for entry in tqdm(response.data, desc="Summarizing articles", total=len(response.data)):
      summary = self.summarize(entry["article"])
      self.supabase.table("entries").update({'summary': summary}).eq('id', entry['id']).execute()  