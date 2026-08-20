from enum import Enum
from dataclasses import dataclass
from typing import Optional
from getplayer import Player

class MatchStatus(Enum):
    MATCH = "✓"
    CLOSE_MATCH = "~"
    NO_MATCH = "X"

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
        return "^" if diff > 0 else "v"


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

    def comp_for_game(self):
        """Return a dictionary of comparison results formatted for the game."""
        results = self.compare_all()
        game_results = {
            "team": results["team"],
            "division": results["division"],
            "conference": results["conference"],
            "position": results["position"],
            "age": [results["age"][0], results["age"][2]],
            "height": [results["height"][0], results["height"][2]],
            "jersey": [results["jersey"][0], results["jersey"][2]],
            "player": results["player"]
        }
        return game_results


    def __str__(self):
        string = []
        results = self.compare_all()
        for key in results:
            string.append(f"{key}: {results[key]}")
        return "\n".join(string)
