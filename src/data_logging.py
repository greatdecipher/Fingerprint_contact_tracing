import logging
import datetime


def log_data(name):
    with open('/home/pi/Fingerprint_Contact_Tracing/node_location.txt') as f:
        location = f.readline()

    time_now = datetime.datetime.now().date()

    log_file = "/home/pi/Fingerprint_Contact_Tracing/logs/{0}-{1}.log".format(
        location, str(time_now))

    # now we will Create and configure logger
    logging.basicConfig(filename=log_file,
                        format='%(message)s - %(asctime)s',
                        filemode='a')

    # Let us Create an object
    logger = logging.getLogger()

    # Now we are going to Set the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)

    logger.info(name)
