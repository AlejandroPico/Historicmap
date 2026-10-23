"""Incremental 1950–1959 acquisition; never reset later curated decades."""
import importlib.util, pathlib
spec=importlib.util.spec_from_file_location('history_acquisition',pathlib.Path(__file__).with_name('enrich-1970-authorities.py'))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.START='1950-01-01';module.PERIOD_END='1959-12-31';module.ACQUISITION='historical-0.10'
module.LIFETIMES['VNM']=('1976-07-02',module.TODAY)
if __name__=='__main__':module.acquire(skip_media=True)
