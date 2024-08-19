from typing import List, Optional
from pydantic import BaseModel
from yaml import safe_load
from ..config.path import config_path


class View(BaseModel):
    file: str
    view: str
    x: Optional[int] = None
    y: Optional[int] = None

    def __repr__(self):
        return f"View(view={self.view}, x={self.x}, y={self.y})"



class ViewsConfig(BaseModel):
    views: List[View]

    def __repr__(self):
        return f"ViewsConfig(views={self.views})"

    @classmethod
    def read_config(cls):
        return cls.parse_obj(
            safe_load((config_path / "views.yaml").open(encoding="utf-8"))
        )

    def get(self, view_name: str) -> Optional[View]:
        for view in self.views:
            print(view.view, view_name)
            if view.file == view_name:
                return view
        return None
