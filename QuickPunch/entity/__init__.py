from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class SummarizationConfig:
  model_path: str
  max_length: int
  min_length: int
  do_sample: bool

@dataclass(frozen=True)
class CategorizationConfig:
  model_path: str
  threshold: float