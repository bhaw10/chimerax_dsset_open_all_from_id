from chimerax.core.commands import Command
import re

# TODO: 1. set sample ID
sample_id = '7454_6d84_S'




# TODO: 2. set data base directory *note: this step only needs to be done infrequently after initial setup
data_dir = '/home/bhawi001/_heLab/deepsseetracer_training_code_copy/data/raw_data' # no trailing '/'

parts = re.split(r"[ _]", sample_id)
emdbid, pdbid, chainid = parts
sample_id = f"{emdbid}_{pdbid}_{chainid}"

# TODO: 3. fix mrc and cif path resolved from data_dir if needed
mrc_path = f"{data_dir}/{emdbid}_{pdbid}/{sample_id}.mrc"
cif_path = f"{data_dir}/{emdbid}_{pdbid}/{sample_id}_fitted.cif"

# TODO: 4. in ChimeraX terminal (with DeepSSETracer installed), run the command: runscript /path/to/cx_open_map_and_model.py

command = Command(session)
command.run("close #*")
command.run(f"open {mrc_path}")
command.run(f"open {cif_path}")
command.run(f"hide atoms")
command.run(f"show cartoons")
command.run(f"transparency #1 15") # set transparency here
