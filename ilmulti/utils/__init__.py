import os

ILMULTI_DIR = os.path.join(os.environ['HOME'], '.ilmulti')

# Handling a special case for supernova.
if 'HOSTNAME' in os.environ:
    if os.environ['HOSTNAME'] in ['fusor', 'supernova']:
        print("{hostname} detected. Switching. Please check if ok.".format(hostname=os.environ['HOSTNAME']))
        user = os.environ['USER']
        ILMULTI_DIR = os.path.join('/home/{user}'.format(user=user), '.ilmulti')

from .language_utils import canonicalize, language_token
from .download_utils import download_resources
from .language_utils import detect_lang

def autolog(message):
    "Automatically log the current function details."
    import inspect, logging
    # Get the previous frame in the stack, otherwise it would
    # be this function!!!
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    #logging.debug("%s: %s in %s:%i" % (
    #    message, 
    #    func.co_name, 
    #    func.co_filename, 
    #    func.co_firstlineno
    #))
    print("%s: %s in %s:%i" % (
        message, 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))
