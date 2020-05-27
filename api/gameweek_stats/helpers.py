def award_points(**kwargs):
    points = 0
    if kwargs.get('starting_appearance'):
        points += 2
    if kwargs.get('sub_appearance'):
        points += 2
    if kwargs.get('man_of_the_match'):
        points += 5
    if kwargs.get('assists'):
        assists = kwargs.get('assists') * 3
        points += assists
    if kwargs.get('conversions'):
        points += kwargs.get('conversions')
    if kwargs.get('penalty_kicks'):
        penalty_kicks = kwargs.get('penalty_kicks') * 2
        points += penalty_kicks
    if kwargs.get('drop_goals'):
        drop_goals = kwargs.get('drop_goals') * 2
        points += drop_goals
    if kwargs.get('yellow_card'):
        points -= 3
    if kwargs.get('red_card'):
        points -= 5
    return points
