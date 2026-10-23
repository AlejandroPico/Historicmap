"""Acquire date-qualified flag designs for 1960 onward, preserving curated intervals."""
import importlib.util,pathlib,argparse
spec=importlib.util.spec_from_file_location('flag_acquisition',pathlib.Path(__file__).with_name('enrich-1970-flags.py'))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.h.START='1960-01-01'
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--catalog-only',action='store_true');args=parser.parse_args();module.acquire(args.catalog_only)
