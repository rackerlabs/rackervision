import getpass
import tempfile
import time

import pyrax


class Worker(object):

    def __init__(self, user, key):
        pass

    def _transcode(input_file, output_file):
        pass

    def _get_work():
        pass

    def run():
        while True:
            work = _get_work()

            if work:
                with tempfile.TemporaryFile(mode='w+b') as input_file:
                    with tempfile.TemporaryFile(mode='w+b') as output_file:
                        _transcode(input_file, output_file)
            else:
                time.sleep(1)


if __name__ == '__main__':
    user = 'rackervision'
    key = getpass.getpass('API Key: ')

    pyrax.set_setting('identity_type', 'rackspace')
    pyrax.set_credentials(user, key)

    Worker(user, key).run()
