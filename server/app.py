from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.models import db, Exercise, Workout, WorkoutExercise
from server.schemas import (
    ma,
    ExerciseSchema,
    ExerciseDetailSchema,
    WorkoutSchema,
    WorkoutDetailSchema,
    WorkoutExerciseSchema,
    WorkoutExerciseWithExerciseSchema,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)


def error_response(errors, status):
    if not isinstance(errors, (list, dict)):
        errors = [str(errors)]
    return jsonify({'errors': errors}), status


def commit():
    """Commit the session; return an error message if the database rejects it."""
    try:
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        return str(err.orig)
    return None


@app.get('/workouts')
def list_workouts():
    workouts = Workout.query.order_by(Workout.date.desc()).all()
    return jsonify(WorkoutSchema(many=True).dump(workouts)), 200


@app.get('/workouts/<int:workout_id>')
def show_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if workout is None:
        return error_response('Workout not found.', 404)
    return jsonify(WorkoutDetailSchema().dump(workout)), 200


@app.post('/workouts')
def create_workout():
    try:
        data = WorkoutSchema().load(request.get_json() or {})
        workout = Workout(**data)
    except ValidationError as err:
        return error_response(err.messages, 400)
    except ValueError as err:
        return error_response(str(err), 400)

    db.session.add(workout)
    problem = commit()
    if problem:
        return error_response(problem, 400)
    return jsonify(WorkoutSchema().dump(workout)), 201


@app.delete('/workouts/<int:workout_id>')
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if workout is None:
        return error_response('Workout not found.', 404)
    db.session.delete(workout)
    db.session.commit()
    return '', 204


@app.get('/exercises')
def list_exercises():
    exercises = Exercise.query.order_by(Exercise.name).all()
    return jsonify(ExerciseSchema(many=True).dump(exercises)), 200


@app.get('/exercises/<int:exercise_id>')
def show_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)
    if exercise is None:
        return error_response('Exercise not found.', 404)
    return jsonify(ExerciseDetailSchema().dump(exercise)), 200


@app.post('/exercises')
def create_exercise():
    try:
        data = ExerciseSchema().load(request.get_json() or {})
        exercise = Exercise(**data)
    except ValidationError as err:
        return error_response(err.messages, 400)
    except ValueError as err:
        return error_response(str(err), 400)

    db.session.add(exercise)
    problem = commit()
    if problem:
        return error_response(problem, 400)
    return jsonify(ExerciseSchema().dump(exercise)), 201


@app.delete('/exercises/<int:exercise_id>')
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)
    if exercise is None:
        return error_response('Exercise not found.', 404)
    db.session.delete(exercise)
    db.session.commit()
    return '', 204


@app.post('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises')
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    if workout is None:
        return error_response('Workout not found.', 404)
    exercise = db.session.get(Exercise, exercise_id)
    if exercise is None:
        return error_response('Exercise not found.', 404)

    try:
        data = WorkoutExerciseSchema().load(request.get_json() or {})
        workout_exercise = WorkoutExercise(
            workout_id=workout.id, exercise_id=exercise.id, **data
        )
    except ValidationError as err:
        return error_response(err.messages, 400)
    except ValueError as err:
        return error_response(str(err), 400)

    db.session.add(workout_exercise)
    problem = commit()
    if problem:
        return error_response(problem, 400)
    return jsonify(WorkoutExerciseWithExerciseSchema().dump(workout_exercise)), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)