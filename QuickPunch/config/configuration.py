from QuickPunch.entity import SummarizationConfig, CategorizationConfig 
from QuickPunch.utils import read_yaml

class ConfigurationManager:
  def __init__(self, config_filepath):
    self.config = read_yaml(config_filepath)

  def get_summarization_config(self) -> SummarizationConfig:
    return SummarizationConfig(**self.config.summarization)

  def get_categorization_config(self) -> CategorizationConfig:
    return CategorizationConfig(**self.config.categorization)
