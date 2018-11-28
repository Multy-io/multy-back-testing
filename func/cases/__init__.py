import os
import sys

fixtures_path = os.path.dirname(__file__)
fixtures_files = sorted(os.listdir(fixtures_path))
scenario_module_names = [mod[:-3]
                         for mod in fixtures_files if mod.startswith('case_')]
sys.path.append(fixtures_path)


cases = {}
for mod in map(__import__, scenario_module_names):
    name = mod.__name__
    if name.startswith('case_'):
        name = name.replace('case_', '')
        cases[name] = mod
        mod.NAME = name
