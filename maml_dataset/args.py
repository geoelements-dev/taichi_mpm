from dataclasses import dataclass, field
from typing import Optional
from omegaconf import MISSING
from hydra.core.config_store import ConfigStore

@dataclass
class FrictionAngleConfig:
    start_angle: float = 20
    end_angle: float = 40
    increment: float = 5
    n_files: int = 60

@dataclass
class InitialStateConfig:
    random_position: bool = False
    random_velocity: bool = False

@dataclass
class Config:
    input_path: str = MISSING
    friction_angle: FrictionAngleConfig = field(default_factory=FrictionAngleConfig)
    initial_state: InitialStateConfig = field(default_factory=InitialStateConfig)
    output_path: str = MISSING

# Hydra configuration
cs = ConfigStore.instance()
cs.store(name="base_config", node=Config)