import logging
import os
import sys
import threading
import inspect,datetime
import uuid
# Create a logger named 'FunctionLogger'

logger = logging.getLogger("FunctionLogger")
logger.setLevel(logging.INFO)

# Create a file handler that logs messages to 'function_calls.log'
file_handler = logging.FileHandler("function_calls.log")
file_handler.setLevel(logging.INFO)

# Define a formatter that includes the timestamp and message
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)


def log_for_main(event_type):
    """
    Logs details about function entry or exit.

    Args:
        event_type (str): Indicates whether the log is for 'entry' or 'exit'.
                          Default is 'entry'.
    """
    # Capture the current stack
    stack = inspect.stack()

    # Ensure there are enough frames to inspect

    # [0] - Current function (`log_function_entry_exit`)
    # [1] - The function that called `log_function_entry_exit` (callee)
    # [2] - The caller of the callee (caller)

    # Extract frames
    callee_frame_info = stack[1]
    caller_frame_info = stack[1]

    callee_frame = callee_frame_info.frame
    caller_frame = caller_frame_info.frame

    # 3.1. Process Details
    process_name = os.path.basename(sys.argv[0]) if hasattr(sys, 'argv') and len(sys.argv) > 0 else 'Unknown'
    process_id = os.getpid()

    # 3.2. Thread Details
    thread_name = threading.current_thread().name
    thread_id = threading.get_ident()

    # 3.3. Caller Details
    caller_filename = caller_frame_info.filename
    caller_func = caller_frame_info.function
    caller_id = id(caller_frame)
    caller_line_no=caller_frame.f_lineno
    caller_class = get_class_name(caller_frame)
    print(caller_id,callee_frame)
    # 3.4. Callee Details
    callee_filename = callee_frame_info.filename
    callee_func = callee_frame_info.function
    callee_id = id(callee_frame)
    callee_class = get_class_name(callee_frame)

    # 3.5. Log the Details
    logger.info(
        f"EventType: {event_type}, "
        f"ProcessName: {process_name}, ProcessID: {process_id}, "
        f"ThreadName: {thread_name}, ThreadID: {thread_id}, "
        f"Caller_name: {caller_filename}, Caller_func: {caller_func}, Caller_id: {caller_id}, Caller_class: {caller_class},Caller_lineno: {caller_line_no},"
        f"Callee_name: {callee_filename}, Callee_func: {callee_func}, Callee_id: {callee_id}, Callee_class: {callee_class}"
    )


def log_thread_or_process_creation(creation_type, created_id):
    """
    Logs the creation of a thread or process.

    Args:
        creation_type (str): Type of creation, either 'thread' or 'process'.
        created_id (int): ID of the created thread or process.
    """
    # 1.1. Process Details
    process_name = os.path.basename(sys.argv[0]) if hasattr(sys, 'argv') and len(sys.argv) > 0 else 'Unknown'
    process_id = os.getpid()

    # 1.2. Thread Details
    thread_name = threading.current_thread().name
    thread_id = threading.get_ident()
    stack = inspect.stack()

    # Ensure there are enough frames to inspect

    # [0] - Current function (`log_function_entry_exit`)
    # [1] - The function that called `log_function_entry_exit` (callee)
    # [2] - The caller of the callee (caller)

    # Extract frames
    callee_frame_info = stack[1]

    callee_frame = callee_frame_info.frame


    # 3.3. Caller Details
    # 3.4. Callee Details
    callee_filename = callee_frame_info.filename
    callee_func = callee_frame_info.function
    callee_id = id(callee_frame)
    callee_class = get_class_name(callee_frame)

    # 1.3. Log the Creation Event
    logger.info(
        f"EventType: {creation_type}_creation, "
        f"CreatorProcessName: {process_name}, ProcessID: {process_id}, "
        f"CreatorThreadName: {thread_name}, ThreadID: {thread_id}, "
        f"Creator_func:{callee_func},"
        f"Creator_id:{callee_id},"
        f"Created_tp_ID: {created_id}, "
        f"Message: 'Creating {creation_type} with ID {created_id}'"
    )

# 2. Helper Function to Determine Class Name
# -------------------------------------------

def get_class_name(frame):
    """
    Attempts to retrieve the class name from a frame.
    If the function is a method of a class, returns the class name.
    Otherwise, returns 'None'.
    """
    # Check if 'self' is in local variables (instance method)
    if 'self' in frame.f_locals:
        return type(frame.f_locals['self']).__name__
    # Check if 'cls' is in local variables (class method)
    elif 'cls' in frame.f_locals:
        return frame.f_locals['cls'].__name__
    else:
        return 'None'


# 3. `log_function_entry_exit` Function
# -------------------------------------

def log_function_entry_exit(event_type):
    """
    Logs details about function entry or exit.

    Args:
        event_type (str): Indicates whether the log is for 'entry' or 'exit'.
                          Default is 'entry'.
    """
    # Capture the current stack
    stack = inspect.stack()

    # Ensure there are enough frames to inspect
    if len(stack) < 3:
        # Not enough stack frames to determine caller and callee
        return

    # [0] - Current function (`log_function_entry_exit`)
    # [1] - The function that called `log_function_entry_exit` (callee)
    # [2] - The caller of the callee (caller)

    # Extract frames
    callee_frame_info = stack[1]
    caller_frame_info = stack[2]

    callee_frame = callee_frame_info.frame
    caller_frame = caller_frame_info.frame

    # 3.1. Process Details
    process_name = os.path.basename(sys.argv[0]) if hasattr(sys, 'argv') and len(sys.argv) > 0 else 'Unknown'
    process_id = os.getpid()

    # 3.2. Thread Details
    thread_name = threading.current_thread().name
    thread_id = threading.get_ident()

    # 3.3. Caller Details
    caller_filename = caller_frame_info.filename
    caller_func = caller_frame_info.function
    caller_id = id(caller_frame)
    caller_line_no = caller_frame_info.lineno
    caller_class = get_class_name(caller_frame)

    # 3.4. Callee Details
    callee_filename = callee_frame_info.filename
    callee_func = callee_frame_info.function
    callee_id = id(callee_frame)
    callee_class = get_class_name(callee_frame)

    # 3.5. Log the Details
    logger.info(
        f"EventType: {event_type}, "
        f"ProcessName: {process_name}, ProcessID: {process_id}, "
        f"ThreadName: {thread_name}, ThreadID: {thread_id}, "
        f"Caller_name: {caller_filename}, Caller_func: {caller_func}, Caller_id: {caller_id}, Caller_class: {caller_class},Caller_lineno:{caller_line_no},"
        f"Callee_name: {callee_filename}, Callee_func: {callee_func}, Callee_id: {callee_id}, Callee_class: {callee_class}"
    )


# 4. Example Usage
# ----------------

# Example standalone function
# Entry point to demonstrate the logging
if __name__ == "__main__":
    def example_function():
        log_function_entry_exit('entry')  # Log function entry
        print("Function is executing")
        log_function_entry_exit('exit')  # Log function exit


    # Example method within a class
    class ExampleClass:
        def example_method(self):
            log_function_entry_exit('entry')  # Log method entry
            print("Method is executing")
            log_function_entry_exit('exit')  # Log method exit


    example_function()

    obj = ExampleClass()
    obj.example_method()
