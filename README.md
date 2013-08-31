# cpu_cores-collectd-plugin

## What is it ?

A collectd plugin (written in python) to send the number of "physical" cpu cores (without hyperthreading logical cores) and processors of a linux/osx box to collectd.

The main goal is to calculate the load average by cpu physical core.

## Requirements

- `python`
- `collectd` (with python plugin support)
- `cpu_cores`

## How to install ?

- place `cpu_cores_plugin.py` file in `[...]/collectd/plugins/python/` directory
- configure the plugin (see below)
- restart `collectd`

## Configuration

Add the following to your collectd config :

    [...]

    <LoadPlugin python>
      Globals true
    </LoadPlugin>

    [...]
    
    <Plugin python>
      ModulePath "[...]/collectd/plugins/python"
      Import "cpu_cores_plugin"
      <Module cpu_cores_plugin>
        Verbose false
      </Module>
    </Plugin>

## Thanks

Thanks to [redis-collectd-plugin](https://github.com/powdahound/redis-collectd-plugin) for inspiration.
