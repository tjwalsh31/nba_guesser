from enum import Enum
from dataclasses import dataclass
from typing import Optional
from getplayer import Player

class MatchStatus(Enum):
    MATCH = "match"
    CLOSE_MATCH = "close_match"
    NO_MATCH = "no_match"

@dataclass
class ComparisonResult:
    attribute: str
    status: MatchStatus
    delta: Optional[int] = None
    direction: Optional[str] = None


class PlayerComparison:
    def __init__(self, target, guess):
        self.target = target
        self.guess = guess

    @staticmethod
    def _get_direction(diff):
        """Return the target's direction relative to the guess."""
        if diff == 0:
            return "same"
        return "higher" if diff > 0 else "lower"


    def compare_position(self):
        """Compare to players by position, return relative feedback"""
        position_roles = {
            "Guard": {"Guard"},
            "Forward": {"Forward"},
            "Center": {"Center"},
            "Guard-Forward": {"Guard", "Forward"},
            "Forward-Guard": {"Guard", "Forward"},
            "Forward-Center": {"Forward", "Center"},
            "Center-Forward": {"Forward", "Center"},
        }

        target_role = position_roles.get(self.target.position, {self.target.position})
        guess_role = position_roles.get(self.guess.position, {self.guess.position})

        if target_role == guess_role:
            return ComparisonResult("position", MatchStatus.MATCH)
        if target_role & guess_role:
            return ComparisonResult("position", MatchStatus.CLOSE_MATCH)
        
        return ComparisonResult("position", MatchStatus.NO_MATCH)

    def compare_age(self):
        diff = self.target.age - self.guess.age
        direction = self._get_direction(diff)
        if diff == 0:
            return ComparisonResult("age", MatchStatus.MATCH, direction=direction)
        if -2 <= diff <= 2:
            return ComparisonResult(
                "age", MatchStatus.CLOSE_MATCH, diff, direction
            )
        return ComparisonResult("age", MatchStatus.NO_MATCH, diff, direction)

    def compare_height(self):
        diff = self.target.height - self.guess.height
        direction = self._get_direction(diff)
        if diff == 0:
            return ComparisonResult("height", MatchStatus.MATCH, direction=direction)
        if -2 <= diff <= 2:
            return ComparisonResult(
                "height", MatchStatus.CLOSE_MATCH, diff, direction
            )
        return ComparisonResult("height", MatchStatus.NO_MATCH, diff, direction)

    def compare_jersey(self):
        """Compare two players by jersey number and return relative feedback."""
        j1 = int(self.target.jersey)
        j2 = int(self.guess.jersey)
        if self.target.jersey == "00":
            j1 = -1
        if self.guess.jersey == "00":
            j2 = -1

        diff = j1 - j2
        direction = self._get_direction(diff)
        if diff == 0:
            return ComparisonResult("jersey", MatchStatus.MATCH, direction=direction)
        if -2 <= diff <= 2:
            return ComparisonResult(
                "jersey", MatchStatus.CLOSE_MATCH, diff, direction
            )
        
        return ComparisonResult("jersey", MatchStatus.NO_MATCH, diff, direction)

    def compare_teams(self):
        t2 = self.guess.current_team.abbreviation
        if t2 == self.target.current_team.abbreviation:
            return ComparisonResult("team", MatchStatus.MATCH)
        if t2 in self.target.all_teams:
            return ComparisonResult("team", MatchStatus.CLOSE_MATCH)
        return ComparisonResult("team", MatchStatus.NO_MATCH)

    def compare_conference(self):
        """Compare two players by their team's conference."""
        c1 = self.target.current_team.conference
        c2 = self.guess.current_team.conference
        if c1 == c2:
            return ComparisonResult("conference", MatchStatus.MATCH)
        return ComparisonResult("conference", MatchStatus.NO_MATCH)

    def compare_division(self):
        d1 = self.target.current_team.division
        d2 = self.guess.current_team.division
        if d1 == d2:
            return ComparisonResult("division", MatchStatus.MATCH)
        return ComparisonResult("division", MatchStatus.NO_MATCH)

    def compare_player(self):
        if self.target.id == self.guess.id:
            return ComparisonResult("player", MatchStatus.MATCH)
        return ComparisonResult("player", MatchStatus.NO_MATCH)

    def compare_all(self):
        """Compare all attributes and return a list of results."""
        position = self.compare_position()
        age = self.compare_age()
        height = self.compare_height()
        jersey = self.compare_jersey()
        team = self.compare_teams()
        conference = self.compare_conference()
        division = self.compare_division()
        player = self.compare_player()
        results = {
            "position": position.status.value,
            "age": [age.status.value, age.delta, age.direction],
            "height": [height.status.value, height.delta, height.direction],
            "jersey": [jersey.status.value, jersey.delta, jersey.direction],
            "team": team.status.value,
            "conference": conference.status.value,
            "division": division.status.value,
            "player": player.status.value
        }
        return results

    def __str__(self):
        string = []
        results = self.compare_all()
        for key in results:
            string.append(f"{key}: {results[key]}")
        return "\n".join(string)
            


target = Player()
target.set_target()
guess = Player()
guess.set_random_player()

print(target)
print(guess)
comp = PlayerComparison(target, guess)
print(comp)

        







""" Remove these at some point"""
def compare_position(p1, p2):
    """Compare two players by position and return relative feedback."""
    position_roles = {
        "Guard": {"Guard"},
        "Forward": {"Forward"},
        "Center": {"Center"},
        "Guard-Forward": {"Guard", "Forward"},
        "Forward-Guard": {"Guard", "Forward"},
        "Forward-Center": {"Forward", "Center"},
        "Center-Forward": {"Forward", "Center"},
    }

    roles1 = position_roles.get(p1.position, {p1.position})
    roles2 = position_roles.get(p2.position, {p2.position})

    if roles1 == roles2:
        return "="
    if roles1 & roles2:
        return "~"
    return "!="


def compare_height(p1, p2):
    """Compare two players by height and return relative feedback."""
    diff = p1.height - p2.height
    if diff == 0:
        return "="
    if 0 < diff <= 3:
        return "+"
    if -3 <= diff < 0:
        return "-"
    if diff > 3:
        return "++"
    return "--"


def compare_age(p1, p2):
    """Compare two players by age and return relative feedback."""
    diff = p1.age - p2.age
    if diff == 0:
        return "="
    if 0 < diff <= 3:
        return "+"
    if -3 <= diff < 0:
        return "-"
    if diff > 3:
        return "++"
    return "--"


def compare_jersey(p1, p2):
    """Compare two players by jersey number and return relative feedback."""
    j1 = int(p1.jersey)
    j2 = int(p2.jersey)
    # handling jersey number 00
    if p1.jersey == "00":
        j1 = -1
    if p2.jersey == "00":
        j2 = -1

    diff = j1 - j2
    if diff == 0:
        return "="
    if 0 < diff <= 3:
        return "+"
    if -3 <= diff < 0:
        return "-"
    if diff > 3:
        return "++"
    return "--"

def compare_teams(p1, p2):
    """Compare two players by current team and past team history."""
    if not p1.target:
        return "?"
    t2 = p2.current_team.abbreviation
    if t2 == p1.current_team.abbreviation:
        return "="
    if t2 in p1.all_teams:
        return "~"
    return "!="

def compare_conference(p1, p2):
    """Compare two players by their team's conference."""
    c1 = p1.current_team.conference
    c2 = p2.current_team.conference
    if c1 == c2:
        return "="
    return "!="

def compare_division(p1, p2):
    """Compare two players by their team's division."""
    d1 = p1.current_team.division
    d2 = p2.current_team.division
    if d1 == d2:
        return "="
    return "!="

def compare_player(p1, p2):
    if p1.id == p2.id:
        return "="
    return "!="


