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

app = Flask(__name__)
api = Api(app)

# Error handler
@app.errorhandler(404)

def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


## Add app here
api.add_resource(CpuUsage, '/fp-cpu-usage')
api.add_resource(Stats, '/stats')

if __name__ == '__main__':
    app.run(host='localhost', debug=True)
