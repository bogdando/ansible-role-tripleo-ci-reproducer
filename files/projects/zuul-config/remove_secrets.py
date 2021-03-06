#!/usr/bin/env python
import sys
import yaml


path = sys.argv[1]
with open(path) as f:
    t = f.read()
y = yaml.load(t)
p = []
for i in y:
    if i.get('job'):
        # Don't remove secrets from reproducer CI
        # we are able to reproduce those secrets with
        # tripleo_ci_gerrit_key role param
        job = i.get('job')
        if job.get('name') != "tripleo-ci-reproducer-base":
            job.pop('secrets', None)
        # Replace all mentions of "config" with "zuul-config"
        if job.get("required-projects") and 'config' in job.get(
                   "required-projects"):
            job['required-projects'].remove('config')
            job['required-projects'].append('zuul-config')

    p.append(i)
with open(path, "w") as f:
    yaml.dump(p, f, default_flow_style=False)
