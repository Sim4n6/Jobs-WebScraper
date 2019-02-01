from functools import wraps
import datetime as dt
import logging


def duration_decorator(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		t_before = dt.datetime.now()
		output = func(*args, **kwargs)
		delta_t = dt.datetime.now() - t_before
		print(f"Execution duration of {func.__name__} is : {delta_t.seconds} in seconds and {delta_t.microseconds} in microseconds.")
		return output

	return wrapper


def log_decorator(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		logging.info(f"Call made to {func.__name__}")
		return func(*args, **kwargs)
	return wrapper
