from typing import Any
from datetime import datetime
from QuickPunch.utils import get_supabase, bin_colors, logger, send_email

# The `Distribution` class is responsible for retrieving articles from a Supabase table based on a
# specified category, preparing personalized email messages for subscribers, and sending the emails to
# the subscribers.
class Distribution:
  def __init__(self):
    self.supabase = get_supabase()
    self.categories = [
      "auto",
      "business",
      "economics",
      "finances",
      "lifestyle",
      "management",
      "opinions",
      "politics",
      "realty",
      "technologies",
    ]
    self.icons = {
      "auto": "🚗",
      "business": "💼",
      "economics": "📈",
      "finances": "💰",
      "lifestyle": "👔",
      "management": "📊",
      "opinions": "📣",
      "politics": "🗳️",
      "realty": "🏠",
      "technologies": "📱",
    }

  def get_articles(self, category: str) -> str:
    """
    The `get_articles` function retrieves articles from a Supabase table based on a specified
    category, and returns a string containing the articles' summaries and links, as well as the number
    of articles retrieved.
    
    :param category: The `category` parameter is a string that represents the category of articles you
    want to retrieve. It is used to filter the articles based on their category
    :type category: str
    :return: The `get_articles` function returns a tuple containing two values. The first value is a
    string that represents a collection of articles in HTML format. The second value is an integer
    that represents the number of articles in the collection.
    """
    result = self.supabase.table("entries").select("*").eq("category", category.capitalize()).execute().data
    articles = [
      f"{self.icons[category]} <div class='article'>{summary}\n\nLink: {link}</div>" for summary, link in zip([entry["summary"] for entry in result], [entry["link"] for entry in result])
    ]
    return "".join(articles), len(articles)

  def get_emails_(self, category: str) -> Any:
    result = self.supabase.table(category).select("*").execute().data
    emails = [entry["email"] for entry in result]
    return emails

  def get_all_emails(self) -> Any:
    """
    The function "get_all_emails" retrieves all emails from different categories and stores them in a
    list, while also creating a preference dictionary to track the categories associated with each
    email.
    """
    self.emails = []
    self.preference_dict = {}
    for category in self.categories:
      emails_in_category = self.get_emails_(category)
      for email in emails_in_category:
        if email not in self.preference_dict:
          self.preference_dict[email] = [category]
        else:
          self.preference_dict[email].append(category)
      self.emails.extend(self.get_emails_(category))
    self.emails = list(set(self.emails))

  def prepare_message_for(self, email: str) -> str:
    """
    The function prepares a personalized email message for a given email address, including the top
    articles for the subscriber's preferred categories and a thank you message.
    
    :param email: The `email` parameter in the `prepare_message_for` method is a string that
    represents the email address of the recipient
    :type email: str
    :return: a formatted message string that includes the top articles for the specified email
    address, along with a greeting and a thank you message. The message is formatted as HTML, with
    line breaks replaced by "<br>" tags.
    """
    categories = self.preference_dict[email]
    message = f"<div class='hero'></div><div class='greeting'>Here are your top articles for <b>{datetime.now().strftime('%A, %d %B, %Y')}</b>\n</div>"
    total_n_articles: int = 0
    send: bool = False
    for category in categories:
      articles, n_articles = self.get_articles(category)
      self.update_n_reads(email, n_articles, category)
      message += f"<div class='section'>{articles}</div>" if articles else ""
      total_n_articles += n_articles
    message += "Thank you for subscribing to QuickPunch."
    if total_n_articles != 0: send = True
    return message.replace("\n", "<br>"), send

  # The `update_n_reads` method is responsible for updating the number of reads for a specific
  # category and email address in the Supabase table.
  def update_n_reads(self, email: str, n_reads, category) -> None:
    total_reads = self.supabase.table(category).select("n_reads").eq("email", email).execute().data[0]["n_reads"]
    if total_reads is None:
      total_reads = 0
    total_reads += n_reads
    self.supabase.table(category).update({"n_reads": total_reads}).eq("email", email).execute()

  def send_email_to(self, email: str) -> None:
    message, send = self.prepare_message_for(email)
    if send:
      logger.info(f"{bin_colors.INFO}Sending email to {email}...{bin_colors.ENDC}")
      send_email(email, message)
      logger.info(f"{bin_colors.SUCCESS}Email sent to {email}.{bin_colors.ENDC}")
    else:
      logger.info(f"{bin_colors.INFO}No articles for {email}...{bin_colors.ENDC}")
  
  def send_emails(self) -> None:
    for email in self.emails:
      self.send_email_to(email)
