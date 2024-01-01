from QuickPunch.logging import logger
from QuickPunch.utils import bin_colors
from QuickPunch.components.initialization import Initialization
from QuickPunch.components.summarization import Summarization
from QuickPunch.components.categorization import Categorization
from QuickPunch.components.distribution import Distribution
from QuickPunch.config.configuration import ConfigurationManager

from pathlib import Path

config_manager = ConfigurationManager(Path("config/config.yaml"))

try:
  logger.info(f"{bin_colors.INFO}Starting daily digest.{bin_colors.ENDC}")
  initialization = Initialization()
  initialization.clear_database()
  initialization.create_entries()
  initialization.register_entries()
  initialization.register_articles()
except Exception as e:
  logger.error(f"{bin_colors.ERROR}Error starting daily digest.{bin_colors.ENDC}")
  raise e

try:
  logger.info(f"{bin_colors.INFO}Summarizing articles.{bin_colors.ENDC}")
  summarization_config = config_manager.get_summarization_config()
  summarization = Summarization(summarization_config)
  summarization.summarize_articles()
except Exception as e:
  logger.error(f"{bin_colors.ERROR}Error summarizing articles.{bin_colors.ENDC}")
  raise e 

try:
  logger.info(f"{bin_colors.INFO}Categorizing articles.{bin_colors.ENDC}")
  categorization_config = config_manager.get_categorization_config()
  categorization = Categorization(categorization_config)
  categorization.categorize_articles()
except Exception as e:
  logger.error(f"{bin_colors.ERROR}Error categorizing articles.{bin_colors.ENDC}")
  raise e

try:
  logger.info(f"{bin_colors.INFO}Sending emails.{bin_colors.ENDC}")
  distribution = Distribution()
  distribution.get_all_emails()
  distribution.send_emails()
except Exception as e:
  logger.error(f"{bin_colors.ERROR}Error sending emails.{bin_colors.ENDC}")
  raise e
