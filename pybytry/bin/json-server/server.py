#!/usr/bin/env python

import os
import sys
import json
import ConfigParser

import flask

app = flask.Flask(__name__)

@app.errorhandler(404)
def page_not_found(err):
  response = flask.jsonify(error=404, text=str(err))
  response.status_code = 404
  return response

@app.route('/json/<path:filepath>', methods=['GET'])
def load_json_file(filepath):

  abs_filepath = os.path.join(os.sep, filepath)
  if not os.path.exists(abs_filepath):
    return page_not_found('Path %s does not exist' % filepath)

  return flask.jsonify(json.loads(open(abs_filepath).read()))

def load_cfg(cfg_file):
  parser = ConfigParser.SafeConfigParser()
  parser.read(cfg_file)
  cfg_ds = {}
  for section in parser.sections():
    cfg_ds[section] = dict(parser.items(section))
  return cfg_ds

def main(args):
  if len(args) != 2:
    print 'ERROR: Did not provide config file'
    return 1

  cfg_file = args[1]
  if not os.path.exists(cfg_file):
    print 'ERROR: Config file %s does not exist' % cfg_file
    return 1

  cfg = load_cfg(cfg_file)

  app.run(host=cfg['server']['host'], port=int(cfg['server']['port']),
          debug=True)
  return 0

if __name__ == '__main__':
  sys.exit(main(sys.argv))
