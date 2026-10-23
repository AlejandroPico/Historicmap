"""Incremental 1960–1969 acquisition. Preserve previous decade acquisitions and curations."""
import importlib.util,pathlib,argparse
spec=importlib.util.spec_from_file_location('history_acquisition',pathlib.Path(__file__).with_name('enrich-1970-authorities.py'))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.START='1960-01-01';module.PERIOD_END='1969-12-31';module.ACQUISITION='historical-0.9'
module.LIFETIMES['VNM']=('1976-07-02',module.TODAY)
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--skip-media',action='store_true');args=parser.parse_args()
 module.acquire(args.skip_media)
