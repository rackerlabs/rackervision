import getpass
import tempfile
import time
import uuid

import pyrax

#WORK IN PROGRESS
class Worker(object):

    def __init__(self, user, key, unprocessed_container, processed_container, queue):
        self.unprocessed_container = unprocessed_container
        self.processed_container = processed_container
        self.queue = queue

    def _transcode(input_file, output_file):
        pass

    def _get_work():
        claim = self.queue.claim_messages(1800, 1800, 1)

    def run():
        while True:
            work = _get_work()

            if work:
                with tempfile.TemporaryFile(mode='w+b') as input_file:
                    with tempfile.TemporaryFile(mode='w+b') as output_file:
                        _transcode(input_file, output_file)
            else:
                time.sleep(1)


#TODO Duped from server
def _generate_id():
    return str(uuid.uuid1())

if __name__ == '__main__':
    user = 'rackervision'
    key = getpass.getpass('API Key: ')
    pyrax.queues.client_id = _generate_id()
    un_c = pyrax.cloudfiles.get_container("unprocessed")
    proc_c = pyrax.cloudfiles.get_container("processed")
    queue = pyrax.queues.get("unprocessed")

    pyrax.set_setting('identity_type', 'rackspace')
    pyrax.set_credentials(user, key)

    Worker(user, key, un_c, proc_c, queue).run()
