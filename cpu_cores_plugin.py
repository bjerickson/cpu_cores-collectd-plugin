# This file is part of cpu_cores_plugin released under the MIT license.
# See the LICENSE file for more information.

import collectd

from cpu_cores import CPUCoresCounter

VERBOSE_LOGGING = True
PROCESSORS_COUNT = 0
CORES_COUNT = 0


def log_verbose(msg):
    if not VERBOSE_LOGGING:
        return
    collectd.info('cpu_cores plugin [verbose]: %s' % msg)


def log_warning(msg):
    collectd.warning('cpu_cores plugin: %s' % msg)


def configure_callback(conf):
    global VERBOSE_LOGGING, CORES_COUNT, PROCESSORS_COUNT
    for node in conf.children:
        if node.key == 'Verbose':
            VERBOSE_LOGGING = bool(node.values[0])
        else:
            log_warning('Unknown config key: %s.' % node.key)
    c = CPUCoresCounter.factory()
    PROCESSORS_COUNT = c.get_physical_processors_count()
    CORES_COUNT = c.get_physical_cores_count()
    log_verbose('Configured with verbose=%i, processors=%i, cores=%i'
                % (VERBOSE_LOGGING, PROCESSORS_COUNT, CORES_COUNT))


def dispatch_value(value, key, typ):
    log_verbose('Sending value: %s=%s' % (key, value))
    val = collectd.Values(plugin='cpu_cores')
    val.type = typ
    val.type_instance = key
    val.values = [value]
    val.dispatch()


def read_callback():
    log_verbose('Read callback called')
    dispatch_value(PROCESSORS_COUNT, 'physical_processors', 'gauge')
    dispatch_value(CORES_COUNT, 'physical_cores', 'gauge')


collectd.register_config(configure_callback)
collectd.register_read(read_callback)
