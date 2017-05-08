from flask import abort

# == [ Sqeezer ] == #
class Sqeezer(object):

    def __init__(self, params):

        ro = {
            'error': False,
            'method': 'GET',
            'meta': {
                'command': 'build_file',
                'description': 'Builds a 1G File and stores it locally in /src/files directory',
                'results': 0},
            'result': []
        }

        self.response_object = ro
        self.params = params

    # == [ Sqeezer ] == #
    def sqeezer_action(self, action):

        # == [ ACTION METHOD PASSED IN URL ] == #
        try:
            func = getattr(self, action)
            return func()

        except:
            abort(400, {'message': 'Sqeezer Action Failure'})

    # == [ COMMANDS ] == #
    def build_file(self):
        """

        """
        ro = self.response_object.copy()

        try:
            return ro

        except Exception as e:
            print('>>> ERROR: Command Error - ' + str(e))
            ro['error'] = 'There was an error running your command. Contact Admin'
            return ro

