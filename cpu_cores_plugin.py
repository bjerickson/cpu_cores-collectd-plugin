import os
import subprocess
import psutil
import collectd

verbose_logging = True
socket_count = 0
physical_cores_count = 0
logical_cores_count = 0

def log_verbose(message):
    if not verbose_logging:
        return
    collectd.info('cpu_cores plugin [verbose]: {0}'.format(message))

def log_warning(message):
    collectd.warning('cpu_cores plugin: {0}'.format(message))

def system_call(command):
    try: 
        p = subprocess.Popen([command], stdout=subprocess.PIPE)
        p.wait()
        if p.returncode == 0:
            out = p.stdout.read()
            return out
        else:
            return 1
    except OSError as err:
        print err
        return 1

def get_cpu_map(lscpu_values):
    cpu_map = {}
    lscpu_lines = lscpu_values.split('\n')
    for line in lscpu_lines:
        line_split = line.split(':')
        if line_split[0] == 'CPU(s)':
            cpu_map['logical_cores'] = line_split[1]
        elif line_split[0] == 'Socket(s)':
            cpu_map['sockets'] = line_split[1]
    cpu_map['physical_cores'] = int(cpu_map['logical_cores']) / int(cpu_map['sockets'])
    return cpu_map

def get_cpu_map_psutil():
    cpu_map = {}
    cpu_map['logical_cores'] = psutil.cpu_count()
    cpu_map['physical_core'] = psutil.cpu_count(logical=False)
    cpu_map['sockets'] = 0
    return cpu_map

def set_poll_config(config):
    global verbose_logging, socket_count, physical_cores_count, logical_cores_count
    for node in config.children:
        if node.key == 'Verbose':
            verbose_logging = bool(node.values[0])
        else:
            log_warning("Unknown config key: {}".format(node.key))
    lscpu_values = system_call("lscpu")
    if lscpu_values != 1:
        cpu_map = get_cpu_map(lscpu_values)
    else:
        cpu_map = get_cpu_map_psutil()
    socket_count = int(cpu_map['sockets'])
    physical_cores_count = int(cpu_map['physical_cores'])
    logical_cores_count = int(cpu_map['logical_cores'])
    log_verbose('Configured with verbose={0}, physical_processors={1}, physical_cores={2}, logical_cores={3}'.format(verbose_logging, socket_count, physical_cores_count, logical_cores_count ))

def dispatch_poll_values(key, value, type):
    log_verbose('Sending values: {0}={1}'.format(key, value))
    collectd_values = collectd.values(plugin='cpu_cores')
    collectd_values.type = type
    collectd_values.type_instance = key
    collectd_values.values = [value]
    collectd_values.dispatch()

def poll():
    log_verbose('Polling')
    dispatch_poll_values('physical_processors', socket_count, 'gauge')
    dispatch_poll_values('physical_cores', physical_cores_count, 'gauge')
    dispatch_poll_values('logical_cores', logical_cores_count, 'gauge')

collectd.register_config(set_poll_config)
collectd.register_read(poll)
