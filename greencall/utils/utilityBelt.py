import logging
from time import gmtime, strftime

def enable_log(log_name):
    """ Enable logs written to file """
    log_name = strftime("%d_%b_%Y_%H%M%S", gmtime()) + log_name
    logging.basicConfig(filename= log_name + ".log",
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s' +\
                        ' %(message)s')
