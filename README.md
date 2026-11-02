# Workout Tracker API

A Flask REST API for personal trainers to log workouts and the reusable exercises
inside them. Built with Flask, SQLAlchemy, Flask-Migrate and Marshmallow.

## Installation

```bash
git clone <your-repo-url>
cd workout-tracker-api
pipenv install
pipenv shell
flask --app server.app db init
flask --app server.app db migrate -m "create tables"
flask --app server.app db upgrade head
python -m server.seed
```

## Run

```bash
python -m server.app
```

The API runs at http://localhost:5555.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | /workouts | List all workouts |
| GET | /workouts/<id> | Show one workout with its exercises and reps/sets/duration |
| POST | /workouts | Create a workout (`date`, `duration_minutes`, optional `notes`) |
| DELETE | /workouts/<id> | Delete a workout and its associated workout exercises |
| GET | /exercises | List all exercises |
| GET | /exercises/<id> | Show an exercise and the workouts it appears in |
| POST | /exercises | Create an exercise (`name`, `category`, optional `equipment_needed`) |
| DELETE | /exercises/<id> | Delete an exercise and its associated workout exercises |
| POST | /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises | Add an exercise to a workout (`reps` + `sets`, or `duration_seconds`) |

## Dependencies

Listed in the `Pipfile`: flask, flask-sqlalchemy, flask-migrate, flask-marshmallow, marshmallow.