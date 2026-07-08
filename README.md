[![Build Status](https://travis-ci.com/arthuroe/fp.svg?token=UkY1KBXLvhKhX8CgS2Jn&branch=develop)](https://travis-ci.com/arthuroe/fp)

# Fantasy Rugby API

Fantasy Rugby is a platform that lets users assemble virtual teams from real rugby players, join competitive leagues, and earn points based on how those players perform in live matches — bringing the fantasy sports model to a sport that's largely underserved by existing platforms. This repository contains the backend REST API that powers the app.

## Features

- **User accounts** — registration, login, password reset via email, and profile management
- **Fantasy teams** — draft real players onto a virtual squad within transfer limits
- **Leagues** — create, join, or leave private leagues, plus a global public league
- **Scoring** — points calculated automatically from real player/gameweek performance
- **Seasons & fixtures** — season, fixture, and gameweek data, with the current gameweek advanced automatically on a schedule
- **Articles** — rugby news and content served through the API

## Tech Stack

| Layer      | Technology                      |
| ---------- | ------------------------------- |
| Framework  | Flask                           |
| Database   | PostgreSQL + SQLAlchemy         |
| Migrations | Alembic (via Flask-Migrate)     |
| Auth       | JWT (PyJWT) + bcrypt            |
| Email      | Flask-Mail                      |
| Scheduling | APScheduler                     |
| Testing    | pytest, Flask-Testing, coverage |
| CI         | Travis CI                       |

## Project Structure

The API is organized into resource-based Flask blueprints, each with its own views and models:

```
api/
├── auth/                     # registration, login, password reset/update
├── users/                    # user profile management
├── teams/                    # real-world rugby teams & league standings
├── players/                  # player data
├── fixtures/                 # match fixtures
├── seasons/                  # season data
├── game_week/                # gameweek data
├── gameweek_stats/           # per-player/team stats and scoring
├── fantasy_leagues/          # league creation, join/leave, standings
├── fantasy_teams/            # fantasy team & squad management
├── user_fantasy_team_gameweek/  # per-user, per-gameweek fantasy results
├── articles/                 # news/content
└── models/                   # SQLAlchemy models
```

## Getting Started

### Prerequisites

- Python 3
- PostgreSQL

### Setup

1. **Clone the repo**

   ```bash
   git clone https://github.com/arthuroe/fp.git && cd fp
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Copy `.env.sample` to `.env` and fill in your local settings (database URL, secret key, mail credentials, etc.):

   ```bash
   cp .env.sample .env
   ```

5. **Set up the database**

   Create a PostgreSQL database and user, then point `DATABASE_URL` in `.env` at it. Run migrations:

   ```bash
   python manage.py db upgrade
   ```

6. **Run the app**

   ```bash
   python run.py
   ```

   The API will be available at `http://localhost:5000/api/v1`.

### Running Tests

```bash
pytest
```

## API Overview

All endpoints are prefixed with `/api/v1`. A few highlights:

| Resource             | Example endpoints                                                              |
| -------------------- | ------------------------------------------------------------------------------ |
| Auth                 | `POST /auth/register`, `POST /auth/login`, `POST /auth/reset_password`         |
| Users                | `GET/PUT /current_user`, `GET/PUT/DELETE /users/<user_id>`                     |
| Fantasy Teams        | `GET/POST /fantasy_teams`, `POST /fantasy_team_players/<fantasy_team_id>`      |
| Fantasy Leagues      | `POST /join_fantasy_league`, `GET /view_fantasy_leagues`                       |
| Players              | `GET/POST /players`, `GET/PUT/DELETE /players/<player_id>`                     |
| Fixtures & Gameweeks | `GET /fixtures`, `GET /current_gameweek`, `GET /gameweek_stats/<game_week_id>` |
| Articles             | `GET/POST /articles`, `GET /highlight`                                         |

Most write/update endpoints require a valid JWT, passed as `Authorization: Bearer <token>`.
