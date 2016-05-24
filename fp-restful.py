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
class QueueStats(Resource):
    """
    Data Spec:

    Queue infos are stored like this:
    PortID|QueueID|TotalDesc|UsedDesc|TSCP|ipackets|opackets|imissed|rx_nombuf

    PortID: Port Id.
    QueueID: Queue Id.
    TotalDesc: total number of queue descriptors.
    UsedDesc: total used queue descriptors.
    TSCP: current cpu cycles.
    ipackets: Total number of successfully received packets.
    opackets: Total number of successfully transmitted packets.
    imissed: Total of RX missed packets.
    rx_nombuf: Total number of RX mbuf allocation failures.

    """
    def get(self):
        result = []
        ports = []
        cur_port = None
        fdisc = open('results', 'r')
        for line in fdisc:
            list_line = line.strip().split("|")
            cur_result = []
            if cur_port is None:
                port = ["port"+list_line[0]]
                cur_port = port
                queue = ["queue"+list_line[1]]
                queue_values = list_line[2:]
                queue.append(queue_values)
                cur_result.extend(port)
                cur_result.append(queue)
                result.append(cur_result)
            elif cur_port == ["port"+list_line[0]]:
                queue = ["queue"+list_line[1]]
                queue_values = list_line[2:]
                queue.append(queue_values)
                result[-1].append(queue)
            else:
                port = ["port"+list_line[0]]
                cur_port = port
                queue = ["queue"+list_line[1]]
                queue_values = list_line[2:]
                queue.append(queue_values)
                cur_result.extend(port)
                cur_result.append(queue)
                result.append(cur_result)
        return result

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
api.add_resource(QueueStats, '/qstats')

if __name__ == '__main__':
    app.run(host='localhost', debug=True)
