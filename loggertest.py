import logging,subprocess
import multiprocessing
import os
import time
from datetime import datetime
import threading
import uuid
import inspect
import logutils
class demotest:
    def __init__(self):
        self.name='demotest'
        print("Initialized the class")
    def demorun(self):
        time.sleep(1)
        logutils.log_function_entry_exit('call')
        print("Running started for demorun")
        logutils.log_function_entry_exit('exit')
def commonfunc():
    time.sleep(1)
    #loghandler=logging.getLogger(loggername)
    logutils.log_function_entry_exit('call')
    obj=demotest()
    obj.demorun()
    time.sleep(1)
    """
    current_func,class_name,caller= get_caller_info()
    loghandler.info("Entering commonfunc", extra={
        'event_type': 'Start',
        'current_func':current_func,
        'caller': caller,
        'class_name': class_name
    })
    """
    print("Inside common function")
    logutils.log_function_entry_exit('exit')
class CustomLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        kwargs.setdefault('extra', {})
        kwargs['extra'].setdefault('event_type', 'Undefined')
        kwargs['extra'].setdefault('caller', 'Unknown')
        kwargs['extra'].setdefault('class_name', 'None')
        #kwargs['extra'].setdefault('correlation_id', self.extra.get('correlation_id', 'N/A'))
        kwargs['extra'].setdefault('parent_process', self.extra.get('parent_process', 'N/A'))
        kwargs['extra'].setdefault('current_func', self.extra.get('current_func', 'N/A'))
        return msg, kwargs




def get_caller_info():
    frame = inspect.currentframe()
    frame = frame.f_back  # Go back one level to the caller of get_caller_info
    class_name = None
    func_name = None
    func_name = frame.f_code.co_name
    while frame:
        class_name = frame.f_locals.get('self', None)
        if class_name:
            class_name = class_name.__class__.__name__
            break
        frame = frame.f_back

    if class_name is None:
        class_name = "None"
    if func_name is None:
        func_name = "None"
    if func_name is None:
        func_name = "None"
    prev_func=inspect.currentframe().f_back
    if(prev_func!=None):
        prev_func= inspect.currentframe().f_back.f_back
    if(prev_func!=None):
        print(prev_func.f_code.co_name)
        caller_func=prev_func.f_code.co_name
    else:
        caller_func=None
    return func_name, class_name,caller_func


def log_to_root(root_logger, message, **kwargs):
    root_logger.info(message, extra=kwargs)


def function1(correlation_id=None,root_logger=None, log_to_root_flag=True):
    logutils.log_function_entry_exit('call')
    time.sleep(1)
    current_func,class_name,caller = get_caller_info()

    commonfunc()
    time.sleep(1)
    logutils.log_function_entry_exit('exit')

def test1():
    logutils.log_function_entry_exit('call')
    time.sleep(1)
    logutils.log_function_entry_exit('exit')
def function2(correlation_id=None, root_logger=None, log_to_root_flag=True):
    time.sleep(1)
    logutils.log_function_entry_exit('call')
    count=0
    while(count!=10):
        commonfunc()
        count=count+1
        #time.sleep()
    for i in range(0,2):
        #current_func, class_name,caller = get_caller_info()
        p1=multiprocessing.Process(target=commonfunc)

        p1.start()
        print(p1.pid, p1.ident)
        logutils.log_thread_or_process_creation('Process', p1.ident)
        time.sleep(1)
    test1()
    #commonfunc()
    #time.sleep(1)
    #if log_to_root and root_logger:
    logutils.log_function_entry_exit('exit')




# Example usage in a threaded environment
if __name__ == "__main__":
    logutils.log_for_main('call')

    #exit()
    time.sleep(1)
    commonfunc()

    thread1 = threading.Thread(target=function1, args=('','', True))
    thread2 = threading.Thread(target=function2, args=('','', True))
    thread1.start()
    time.sleep(1)
    thread2.start()
    print(thread2.ident)
    logutils.log_thread_or_process_creation('Thread', thread2.ident)
    logutils.log_thread_or_process_creation('Thread', thread1.ident)

    thread1.join()
    thread2.join()
    logging.info("Threads started and running")


    process1 = subprocess.Popen(
        ['python', 'C:\\Users\\Admin\\PycharmProjects\\tasker\\demo1.py', "hello","Hi"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    #process1.communicate()
    # Get the PID of the subprocess
    pid = process1.pid
    print(pid,"PID")
    logutils.log_thread_or_process_creation('Process',pid)
    logutils.log_function_entry_exit('exit')