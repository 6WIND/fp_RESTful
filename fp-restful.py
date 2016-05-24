#!flask/bin/python2

from subprocess import call,check_output
from flask import jsonify, request, Flask, make_response
from flask_restful import reqparse, abort, Api, Resource

#-------------------------------------------------------------------------------
class CpuUsage(Resource):
    def get(self):
        output = check_output(["/usr/local/bin/fp-cpu-usage", "-j"])
        return output

#-------------------------------------------------------------------------------
class Stats(Resource):
    def get(self):
        output = check_output(["/usr/local/bin/fp-cli", "stats-json"])
        return output

#-------------------------------------------------------------------------------
class CLI(Resource):
    def get(self, command):
        terms = request.args.getlist('term')
        command_array = ["/usr/local/bin/fp-cli", command ]
        command_array.extend(terms)
        output = check_output(command_array)
        return output

#-------------------------------------------------------------------------------

app = Flask(__name__)
api = Api(app)

# Error handler
@app.errorhandler(404)

def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


## Add app here
api.add_resource(CpuUsage, '/fp-cpu-usage')
api.add_resource(Stats, '/stats')
api.add_resource(CLI, '/fp-cli/<command>')

if __name__ == '__main__':
    app.run(host='localhost', debug=True)
