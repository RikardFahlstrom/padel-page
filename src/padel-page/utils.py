import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


def get_todays_date():
    return datetime.date.today()


class GameInfoStore(BaseModel):
    id: str
    date: str
    start_time: str
    end_time: str
    place: str
    player1: Optional[str] = "player1"
    player2: Optional[str] = "player2"
    player3: Optional[str] = "player3"
    player4: Optional[str] = "player4"


class GameInfo(BaseModel):
    id: UUID
    date: datetime.date
    start_time: str
    end_time: str
    place: str
    player1: str = "player1"
    player2: str = "player2"
    player3: str = "player3"
    player4: str = "player4"


def compare_old_new_name(old_name: str, new_name: str):
    old_name: str = old_name.strip().lower()
    new_name: str = new_name.strip().lower()

    if new_name == old_name:
        return old_name.capitalize()
    elif new_name:
        return new_name.capitalize()
    else:
        return old_name.capitalize()


def get_final_names(current_names, new_names):
    player_names = {}
    for player_nr in range(1, 5):
        player_names[f"player{player_nr}"] = compare_old_new_name(
            old_name=current_names.get(f"player{player_nr}"),
            new_name=new_names.get(f"player{player_nr}"),
        )
    return player_names
