# Main file to run nlstruct
# Written by Clémence Sebe 
# January 2026

from nlstruct.recipes import train_qualified_ner
import os

from nlstruct import load_pretrained
from nlstruct.datasets import load_from_brat, export_to_brat
from transform_ann import changeFormat


################### USER CONFIGURATION #######################

nb_gpu = 1   #0:cpu - 1:gpu

# 1. List of the models - You can add more 

scibert_uncased="allenai/scibert_scivocab_uncased"
bert_uncased = "bert-base-uncased"
codebert = "microsoft/codebert-base"
modernbert = "answerdotai/ModernBERT-base"

codebert = "csebe/codebert_bioinfo_voc"

selected_model = codebert
finetune_model = False  #True or False

save_models = f"models_train/{selected_model.replace('/','_')}"

os.makedirs(save_models, exist_ok=True)


# 2. Random seeds

tab_seeds = [1,8,22,42,100]


# 3. Path of the data
# - ../CPL-Article
# - ../CPL-Code
# - other paths

path_data = "../../DATA/CPL-Code"


# 4. Prediction
do_prediction = False

if do_prediction:
    # Directories where predictions will be saved
    save_prediction = f"prediction"

    # Directory containing files for the predictions
    where_file_for_prediction ="to_predict/"

    os.makedirs(save_prediction, exist_ok=True)


################### MAIN PART ################################

for seed_temp in tab_seeds:

    # Vary train/dev splits
    for i in range (1,6):

        print(f"---------------------- Iteration {i} - Model {selected_model} - Seed {seed_temp}")

        train = True
        name_save = f"{selected_model.replace('/', '_')}_iteration{i}_seed{seed_temp}.pt"
        if name_save in os.listdir(save_models):
            train = False

        if train:
            model = train_qualified_ner(
                dataset={
                    "train": f"{path_data}/iteration_{i}/train",
                    "val"  : f"{path_data}/iteration_{i}/val", 
                    "test" : f"{path_data}/test"
                },
                finetune_bert= finetune_model,
                seed=seed_temp,
                bert_name=selected_model,
                fasttext_file="",
                gpus=nb_gpu,              
                xp_name="my-xp",
                return_model=True,
                max_steps = 4000,
                model_to_take_encoder="None",
            )
                
            model.save_pretrained(f'{save_models}/{name_save}')
            os.system('rm checkpoints/*')


        if do_prediction :                
            save_pred = f"{save_prediction}/{selected_model.replace('/', '_')}_iteration{i}_seed{seed_temp}/"
            os.makedirs(save_pred, exist_ok=True)

            export_to_brat(model.predict(load_from_brat(where_file_for_prediction)), filename_prefix=f'{save_pred}')
            changeFormat(save_pred)
