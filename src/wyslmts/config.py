import json
from pathlib import Path
from typing import Optional, Dict, Any

class Config:
    def __init__(self, config_path: Path = Path.home() / ".wyslmts" / "config.json"):
        self.config_path = config_path
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.settings = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if self.config_path.exists():
            try:
                with open(self.config_path, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_config(self):
        temp_path = self.config_path.with_suffix(".tmp")
        try:
            with open(temp_path, "w") as f:
                json.dump(self.settings, f, indent=4)
            temp_path.replace(self.config_path)
        except Exception as e:
            if temp_path.exists():
                temp_path.unlink()
            raise e

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def set(self, key: str, value: Any):
        self.settings[key] = value
        self._save_config()

    def delete(self, key: str):
        if key in self.settings:
            del self.settings[key]
            self._save_config()
