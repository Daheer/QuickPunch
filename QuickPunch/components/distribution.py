from typing import Any
from datetime import datetime
from QuickPunch.utils import get_supabase, bin_colors, logger, send_email

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
    categories = self.preference_dict[email]
    message = f"<div class='hero'></div><div class='greeting'>Here are your top articles for <b>{datetime.now().strftime('%A, %d %B, %Y')}</b>\n</div>"
    for category in categories:
      articles, n_articles = self.get_articles(category)
      self.update_n_reads(email, n_articles, category)
      message += f"<div class='section'>{articles}</div>" if articles else ""
    message += "Thank you for subscribing to QuickPunch."
    return message.replace("\n", "<br>")

  def update_n_reads(self, email: str, n_reads, category) -> None:
    total_reads = self.supabase.table(category).select("n_reads").eq("email", email).execute().data[0]["n_reads"]
    if total_reads is None:
      total_reads = 0
    total_reads += n_reads
    self.supabase.table(category).update({"n_reads": total_reads}).eq("email", email).execute()

  def send_email_to(self, email: str) -> None:
    message = self.prepare_message_for(email)
    logger.info(f"{bin_colors.INFO}Sending email to {email}...{bin_colors.ENDC}")
    send_email(email, message)
    logger.info(f"{bin_colors.SUCCESS}Email sent to {email}.{bin_colors.ENDC}")
  
  def send_emails(self) -> None:
    for email in self.emails:
      self.send_email_to(email)