#!flask/bin/python2
# Copyright 2016 6WIND S.A.
# LICENSE: Apache 2.0

from random import randint, choice
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

    def _data_gen(self, filename):
        try:
            fdesc = open(filename, "w")
        except:
            print("error occured")
            sys.exit(0)

        desc_len = [128,256,512]
        for port in range(0, randint(1,4)):
            for queue in range(0, randint(1,4)):
                total = choice(desc_len)
                fdesc.write("%i|%i|%i|%i|%i\n" % (port, queue, total,
                        randint(0, total), randint(0,10000)))
        fdesc.close()
        return "File filled randomly with success"

    def get(self, command):
        if command == "gen":
            return self._data_gen("results")

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
        result = {}
        with open('results', 'r') as fdisc:
            for line in fdisc:
                port, queueid, total, used, tsc = map(int, line.strip().split("|"))
                queue = {
                    "total" : total,
                    "used" : used,
                    "tscp" : tsc,
                }
                if port in result:
                    result[port][queueid] = queue
                else:
                    result[port] = {queueid : queue}

        return jsonify(result)

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
