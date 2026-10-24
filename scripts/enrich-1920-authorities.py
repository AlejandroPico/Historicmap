"""Incremental1920–1949 acquisition, preserving later terms, curations and media."""
import importlib.util,pathlib
spec=importlib.util.spec_from_file_location('history_acquisition',pathlib.Path(__file__).with_name('enrich-1970-authorities.py'))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.START='1920-01-01';module.PERIOD_END='1949-12-31';module.ACQUISITION='historical-0.11'
module.LIFETIMES.update({'VNM':('1976-07-02',module.TODAY),'VSV':('1949-06-14','1955-10-25'),'MAL':('1948-02-01','1963-09-15'),'UAR':('1958-02-22','1961-09-28')})
if __name__=='__main__':module.acquire(skip_media=True)
