from QuickPunch.components.initialization import Initialization
from QuickPunch.components.summarization import Summarization
from QuickPunch.components.categorization import Categorization
from QuickPunch.config.configuration import ConfigurationManager
from pathlib import Path

config_manager = ConfigurationManager(Path("config/config.yaml"))

initialization = Initialization()
initialization.clear_database()
initialization.create_entries()
initialization.register_entries()
initialization.register_articles()

summarization_config = config_manager.get_summarization_config()
summarization = Summarization(summarization_config)
summarization.summarize_articles()

categorization_config = config_manager.get_categorization_config()
categorization = Categorization(categorization_config)
categorization.categorize_articles()

