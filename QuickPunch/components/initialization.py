import feedparser

from QuickPunch.utils import get_supabase, bin_colors, logger, read_article

class Initialization:
  """
  Initialize the database.
  """
  def __init__(self):
    self.supabase = get_supabase()	
    self.links = []

  def clear_database(self):
    """
    Clear the database.
    """
    logger.info(f"{bin_colors.INFO}Clearing database.{bin_colors.ENDC}")
    self.supabase.table("entries").delete().neq("id", -1).execute()
    logger.info(f"{bin_colors.SUCCESS}Database cleared.{bin_colors.ENDC}")

  def create_entries(self):
    """
    Create the entries.
    """
    url = "https://rss.punchng.com/v1/category/latest_news"
    logger.info(f"{bin_colors.INFO}Parsing {url}.{bin_colors.ENDC}")
    feed = feedparser.parse(url)
    for entry in feed.entries:
      self.links.append(entry.link)
    logger.info(f"{bin_colors.SUCCESS}Successfully parsed {url}.{bin_colors.ENDC}")

  def register_entries(self):
    """
    Register the entries in the database.
    """
    logger.info(f"{bin_colors.INFO}Registering entries in database.{bin_colors.ENDC}")
    for i, entry in enumerate(self.links):
      self.supabase.table("entries").insert({"id": i+1, "link": entry}).execute()
    logger.info(f"{bin_colors.SUCCESS}Entries registered in database.{bin_colors.ENDC}")

  def register_articles(self):
    """
    Register the articles in the database.
    """
    logger.info(f"{bin_colors.INFO}Parsing links to get articles.{bin_colors.ENDC}")
    response = self.supabase.table("entries").select("*").execute()
    for entry in response.data:
      article = read_article(entry["link"])
      self.supabase.table("entries").update({'article': article}).eq('id', entry['id']).execute()     