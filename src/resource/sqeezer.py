from flask import abort
from config import ProductionConfig
import multiprocessing
# import memcache
import math
import sys
import lzw
import os


_PATH = ProductionConfig.BASE_PATH + '/src/files'
# cache = memcache.Client(['localhost:11211'])

# == [ Sqeezer ] == #
class Sqeezer(object):

    def __init__(self, params):

        ro = {
            'error': False,
            'method': 'GET',
            'meta': {
                'command': None,
                'description': None,
                'results': 0},
            'result': []
        }

        self.response_object = ro
        self.params = params

    # == [ Sqeezer ] == #
    def sqeezer_action(self, action):

        # == [ ACTION METHOD PASSED IN URL ] == #
        ro = self.response_object.copy()

        try:
            func = getattr(self, action)
            return func()

        except Exception as e:
            print('>>> ERROR: Command Error - ' + str(e))
            ro['error'] = 'There was an error running your command. Contact Admin'
            return ro

    # == [ COMMANDS ] == #
    def compress_test_result(self):
        """

        """
        ro = self.response_object.copy()

        ro['meta']['command'] = 'compress_test_result'
        ro['meta']['description'] = 'Tests to ensure a 10G File was created and tests size of file A and File B.'

        try:
            file_a_path = os.path.join(_PATH, 'test_a.img')  # fallocate -l 1M test_a.img
            file_b_path = os.path.join(_PATH, 'test_b.lzw')

            file_a = os.path.getsize(file_a_path)
            file_b = os.path.getsize(file_b_path)

            proc = multiprocessing.active_children()
            print(proc)

            ro['result'] = {
                "finished": "no" if proc else "yes",
                "file_a_bytes": file_a,
                "file_b_bytes": file_b,
                "file_a": convert_size(file_a),
                "file_b": convert_size(file_b)
            }

            return ro

        except Exception as e:
            print('>>> ERROR: Command Error - ' + str(e))
            ro['error'] = 'There was an error running your command. Contact Admin'
            return ro

    def compress_test(self):
        """

        """
        ro = self.response_object.copy()
        file_a_path = os.path.join(_PATH, 'test_a.img')  # fallocate -l 1M test_a.img

        file_a = os.path.getsize(file_a_path)

        ro['meta']['command'] = 'compress_test'
        ro['meta']['description'] = 'Compresses File and return file size (bytes) of file before and after compression.'

        try:

            d = multiprocessing.Process(name='daemon', target=process_daemon)
            d.daemon = True
            d.start()

            ro['result'] = {
                "finished": "no",
                "file_a_bytes": file_a,
                "file_b_bytes": 0,
                "file_a": convert_size(file_a),
                "file_b": convert_size(0)
            }

            return ro

        except Exception as e:
            print('>>> ERROR: Command Error - ' + str(e))
            ro['error'] = 'There was an error running your command. Contact Admin'
            return ro


# == [ UTILITY METHODS ] == #

def process_daemon():
    p = multiprocessing.current_process()
    print 'Starting:', p.name, p.pid

    file_a_path = os.path.join(_PATH, 'test_a.img')  # fallocate -l 1M test_a.img
    file_b_path = os.path.join(_PATH, 'test_b.lzw')

    bytes = lzw.readbytes(file_a_path)
    compressed = lzw.compress(bytes)
    lzw.writebytes(file_b_path, compressed)

    print 'Exiting :', p.name, p.pid
    sys.stdout.flush()


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


