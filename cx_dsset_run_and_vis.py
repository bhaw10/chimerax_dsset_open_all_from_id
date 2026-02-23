# TODO: 1. set sample_id (format: 'emdb_pdb_chain' or 'emdb pdb chain')
sample_id = '17942_8pug_A'

# TODO: 2. specify if prediction files should be overwritten each run. if false, a subdir will be created for each new sample_id
overwrite = True




# *note: the rest of the steps only need to be done infrequently after initial setup
####################################################################################
# TODO: 3. set output_dir
output_dir = '/home/bhawi001/_heLab/CryoEM/DeepSSETracer/Inference/chimerax_dsset_open_all_from_id/output' # no trailing '/'
if not overwrite: output_dir += f"/{sample_id}"

# TODO: 4. set input data directory
data_dir = '/scratch/cs-bioinfo/tngu/DATA' # no trailing '/'

# ignore this block of code:
############################################################
import re
parts = re.split(r"[ _]", sample_id)
emdbid, pdbid, chain_id = parts
sample_id = f"{emdbid}_{pdbid}_{chain_id}"
############################################################

# TODO: 5. fix mrc_path and cif_path if needed
mrc_path = f"{data_dir}/{emdbid}_{pdbid}/{sample_id}.mrc"
cif_path = f"{data_dir}/{emdbid}_{pdbid}/{sample_id}_fitted.cif"

# TODO: 6. in ChimeraX terminal (with DeepSSETracer installed), run the command: runscript /path/to/cx_open_map_and_model.py



from chimerax.deepssetracer.deepssetracer import deepssetracer_model
from chimerax.core.commands import Command
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Args:
    mrc_path: str
    output_dir: str
    pred_helix_path:str
    pred_sheet_path:str
    pred_helix_path_NoEdge:str
    pred_sheet_path_NoEdge:str
    cuda = "yes"
    seed = 0
    layers = 3

Path(output_dir).mkdir(parents=True,exist_ok=True)
pred_helix_path = output_dir + '/pre_helix.mrc'
pred_sheet_path = output_dir + '/pre_sheet.mrc'
pred_helix_path_NoEdge = output_dir + '/pre_helix_Cropped.mrc'
pred_sheet_path_NoEdge = output_dir + '/pre_sheet_Cropped.mrc'
print(pred_helix_path)
    
args = Args(mrc_path=mrc_path, output_dir=output_dir, 
            pred_helix_path=pred_helix_path, pred_sheet_path=pred_sheet_path,
            pred_helix_path_NoEdge=pred_helix_path_NoEdge, pred_sheet_path_NoEdge=pred_sheet_path_NoEdge)

deepssetracer_model(args)

pred_ids = "#3 #4 #5 #6"
pred_uncropped_ids = "#3 #4"
pred_uncropped_ids_hide = "#!3 #!4" #i'm not sure why it wants the '!' for the hide command, but it does
pred_cropped_ids_hide = "#!5 #!6"
pred_cropped_ids = "#5 #6"
helix_ids = "#3 #5"
sheet_ids = "#4 #6"

command = Command(session)
command.run("close #*")
command.run(f"open {mrc_path}")
command.run(f"open {cif_path}")
command.run(f"open {pred_helix_path}")
command.run(f"open {pred_sheet_path}")
command.run(f"open {pred_helix_path_NoEdge}")
command.run(f"open {pred_sheet_path_NoEdge}")
command.run(f"hide atoms")
command.run(f"show cartoons")

command.run(f"volume {pred_ids} level 0.999") # have to wiggle the volume threshold to make them appear
command.run(f"transparency {pred_ids} 60") # set transparency %
command.run(f"color {helix_ids} #00ff0066 models") # set colors - hex code is printed in ChimeraX log (top right) after selecting a color. Just place that here.
command.run(f"color {sheet_ids} #00ffff66 models") # set colors
command.run(f"hide {pred_uncropped_ids_hide} models") # replace with {pred_cropped_ids_hide} if you prefer
