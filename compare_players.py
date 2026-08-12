from getplayer import Player

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
        return "position ="
    if roles1 & roles2:
        return "position close"
    return "wrong position"


def compare_height(p1, p2):
    """Compare two players by height and return relative feedback."""
    diff = p1.height - p2.height
    if diff == 0:
        return "height ="
    if 0 < diff < 3:
        return "height +"
    if -3 < diff < 0:
        return "height -"
    if diff > 3:
        return "height ++"
    return "height --"


def compare_age(p1, p2):
    """Compare two players by age and return relative feedback."""
    diff = p1.age - p2.age
    if diff == 0:
        return "age ="
    if 0 < diff < 3:
        return "age +"
    if -3 < diff < 0:
        return "age -"
    if diff > 3:
        return "age ++"
    return "age --"


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
        return "jersey ="
    if 0 < diff < 3:
        return "jersey +"
    if -3 < diff < 0:
        return "jersey -"
    if diff > 3:
        return "jersey ++"
    return "jersey --"

def compare_past_teams(p1, p2):
    """Compare two players by current team and past team history."""
    if not p1.target:
        p1.set_target()
    t2 = p2.current_team.abbreviation
    if t2 == p1.current_team.abbreviation:
        return "teams ="
    if t2 in p1.all_teams:
        return "player has played for this team"
    return "teams different"

def compare_conference(p1, p2):
    """Compare two players by their team's conference."""
    c1 = p1.current_team.conference
    c2 = p2.current_team.conference
    if c1 == c2:
        return "conference ="
    return "conference different"

def compare_division(p1, p2):
    """Compare two players by their team's division."""
    d1 = p1.current_team.division
    d2 = p2.current_team.division
    if d1 == d2:
        return "division ="
    return "division different"

def compare_player(p1, p2):
    if p1.name == p2.name:
        return "same player"
    return "different player"


player_one = Player()
player_one.print()

player_two = Player()
player_two.print()

print(compare_position(player_one, player_two))
print(compare_height(player_one, player_two))
print(compare_age(player_one, player_two))
print(compare_jersey(player_one, player_two))
print(compare_past_teams(player_one, player_two))
print(compare_conference(player_one, player_two))
print(compare_division(player_one, player_two))