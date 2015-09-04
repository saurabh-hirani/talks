def check_nlimits(kwargs, json_ds):
  output = {
    'state': 'OK',
    'msgs': []
  }

  warning = int(kwargs['warning'])
  critical = int(kwargs['critical'])

  n = len(json_ds)
  output['msgs'] = '%d < warning %d < critical %d' % (n, warning, critical)
  nlimit = None

  if n >= warning:
    output['state'] = 'WARNING'
    nlimit = warning
  elif n >= critical:
    output['state'] = 'CRITICAL'
    nlimit = critical

  if output['state'] != 'OK':
    output['msgs'] = 'n %d >= %d' % (n, nlimit)

  return output
