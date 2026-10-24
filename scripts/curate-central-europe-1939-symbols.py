"""Acquire the credited historical Slovak symbol with the bounded safe engine."""
import importlib.util,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('symbols',ROOT/'scripts/curate-1920-symbols-extra.py');engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
engine.ROWS=[('SVK-1939','Flag of Slovakia (1939–1945).svg','1939-12-31','1939-12-31',None,'Tricolor de laRepúblicaEslovaca de1939, sin proyectar las armas delEstado contemporáneo. Ventana de cierre anual, no día de adopción.')]
engine.TAG='symbols-central-europe-1939-0.12';engine.PREFIX='symbols-central-europe-1939'
engine.base.START='1939-01-01';engine.base.END='1939-12-31'
if __name__=='__main__':raise SystemExit(engine.main())
