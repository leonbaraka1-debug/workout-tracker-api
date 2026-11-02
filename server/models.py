from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from datetime import date

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'
    __table_args__ = (
        CheckConstraint('length(trim(name)) > 0', name='ck_exercises_name_not_blank'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan'
    )
    workouts = association_proxy('workout_exercises', 'workout')

    @validates('name', 'category')
    def validate_text(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'{key} must be a non-empty string.')
        return value.strip()

    def __repr__(self):
        return f'<Exercise {self.id} {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='ck_workouts_duration_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout', cascade='all, delete-orphan'
    )
    exercises = association_proxy('workout_exercises', 'exercise')

    @validates('date')
    def validate_date(self, key, value):
        if not isinstance(value, date):
            raise ValueError('date must be a valid date.')
        return value

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError('duration_minutes must be a positive integer.')
        return value

    def __repr__(self):
        return f'<Workout {self.id} {self.date}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    __table_args__ = (
        CheckConstraint('reps >= 0', name='ck_workout_exercises_reps_non_negative'),
        CheckConstraint('sets >= 0', name='ck_workout_exercises_sets_non_negative'),
        CheckConstraint(
            'duration_seconds >= 0', name='ck_workout_exercises_duration_non_negative'
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps', 'sets', 'duration_seconds')
    def validate_measures(self, key, value):
        if value is not None and (not isinstance(value, int) or value < 0):
            raise ValueError(f'{key} must be a non-negative integer.')
        return value

    def __repr__(self):
        return f'<WorkoutExercise {self.id} w={self.workout_id} e={self.exercise_id}>'