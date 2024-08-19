from .click import ClickConfig
from typing import Optional, Union, List

click_list = {}


def add_click_config(click_config: Union[ClickConfig, List[ClickConfig]]):
    if isinstance(click_config, list):
        for click in click_config:
            click_list[click.view] = click
    else:
        click_list[click_config.view] = click_config


def get_click_config(name: str) -> Optional[ClickConfig]:
    return click_list.get(name)


add_click_config(
    [
        ClickConfig(view="开始游戏界面", sleep=1),
    ]
)
