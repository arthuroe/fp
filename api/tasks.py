import datetime
import logging

from api.models import GameWeek, Season

from api import app


def update_current_game_week():
    with app.app_context():
        current_season = Season.find_first(is_current=True)
        game_weeks = current_season.gameweeks.order_by(
            GameWeek.date.asc()).all()
        for game_week in game_weeks:
            game_week.is_current = False
            if check_date(game_week.date):
                game_week.is_current = True
            game_week.save()

        # Using print for logging because Gunicorn is not displaying logs \
        # from logging module
        print("Updated GameWeeks..")


def check_date(date):
    today = datetime.datetime.today()
    date = date
    return (
        today.isocalendar()[1] == date.isocalendar()[1] and
        today.year == date.year
    )
