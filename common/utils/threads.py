from threading import Thread

# from https://stackoverflow.com/questions/18420699/multithreading-for-python-django
# NOTE: Django automatically creates a new DB connection per threads - YOU must MANUALLY close it: "connection.close()"
def run_in_separate_thread(function):
  def decorator(*args, **kwargs):
    t = Thread(target = function, args=args, kwargs=kwargs)
    t.daemon = True
    t.start()
  return decorator

# https://stackoverflow.com/questions/4103773/efficient-way-of-having-a-function-only-execute-once-in-a-loop
# NOTE: Limits a function to only run one time WITHIN SAME PROCESS
def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper
