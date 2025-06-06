This repo is a fork of the NLStruct repo by Perceval Wajsbürt, I have left the original README below.

This fork adds the possibility when doing NER model followed by a span classification model to take the posibility to use a specific encoder from an existing model.

It is the support for my paper [Extracting Information in a Low-resource Setting: Case Study on Bioinformatics Workflows](https://arxiv.org/abs/2411.19295) (accepted to IDA 2025).

```
@InProceedings{10.1007/978-3-031-91398-3_21,
    author="Sebe, Cl{\'e}mence and Cohen-Boulakia, Sarah and Ferret, Olivier and N{\'e}v{\'e}ol, Aur{\'e}lie",
    editor="Krempl, Georg and Puolam{\"a}ki, Kai and Miliou, Ioanna",
    title="Extracting Information in a Low-Resource Setting: Case Study on Bioinformatics Workflows",
    booktitle="Advances in Intelligent Data Analysis XXIII",
    year="2025",
    publisher="Springer Nature Switzerland",
    address="Cham",
    pages="274--287",
    abstract="Bioinformatics workflows are essential for complex biological data analyses and are often described in scientific articles with source code in public repositories. Extracting detailed workflow information from articles can improve accessibility and reusability but is hindered by limited annotated corpora. To address this, we framed the problem as a low-resource extraction task and tested four strategies: 1) creating a tailored annotated corpus, 2) few-shot named-entity recognition (NER) with an autoregressive language model, 3) NER using masked language models with existing and new corpora, and 4) integrating workflow knowledge into NER models. Using BioToFlow, a new corpus of 52 articles annotated with 16 entities, a SciBERT-based NER model achieved a 70.4 F-measure, comparable to inter-annotator agreement. While knowledge integration improved performance for specific entities, it was less effective across the entire information schema. Our results demonstrate that high-performance information extraction for bioinformatics workflows is achievable.",
    isbn="978-3-031-91398-3"
}
```

# NLStruct

Natural language struturing library.
Currently, it implements a nested NER model and a span classification model, but other algorithms might follow.

If you find this library useful in your research, please consider citing:

```
@phdthesis{wajsburt:tel-03624928,
  TITLE = {{Extraction and normalization of simple and structured entities in medical documents}},
  AUTHOR = {Wajsb{\"u}rt, Perceval},
  URL = {https://hal.archives-ouvertes.fr/tel-03624928},
  SCHOOL = {{Sorbonne Universit{\'e}}},
  YEAR = {2021},
  MONTH = Dec,
  KEYWORDS = {nlp ; structure ; extraction ; normalization ; clinical ; multilingual},
  TYPE = {Theses},
  PDF = {https://hal.archives-ouvertes.fr/tel-03624928/file/updated_phd_thesis_PW.pdf},
  HAL_ID = {tel-03624928},
  HAL_VERSION = {v1},
}
```

This work was performed at [LIMICS](http://www.limics.fr/), in collaboration with [AP-HP's Clinical Data Warehouse](https://eds.aphp.fr/) and funded by the [Institute of Computing and Data Science](https://iscd.sorbonne-universite.fr/).

## Features

- processes large documents seamlessly: it automatically handles tokenization and sentence splitting.
- do not train twice: an automatic caching mechanism detects when an experiment has already been run
- stop & resume with checkpoints
- easy import and export of data
- handles nested or overlapping entities
- multi-label classification of recognized entities
- strict or relaxed multi label end to end retrieval metrcis
- pretty logging with [rich-logger](https://github.com/percevalw/rich_logger)
- heavily customizable, without config files (see [train_ner.py](https://github.com/percevalw/nlstruct/blob/nlstruct/recipes/train_ner.py))
- built on top of [transformers](https://github.com/huggingface/transformers) and [pytorch_lightning](https://github.com/PyTorchLightning/pytorch-lightning)

## Training models

### How to train a NER model

```python
from nlstruct.recipes import train_ner

model = train_ner(
    dataset={
        "train": "path to your train brat/standoff data",
        "val": 0.05,  # or path to your validation data
        # "test": # and optional path to your test data
    },
    finetune_bert=False,
    seed=42,
    bert_name="camembert/camembert-base",
    fasttext_file="",
    gpus=0,
    xp_name="my-xp",
    return_model=True,
)
model.save_pretrained("model.pt")
```

### How to use it

```python
from nlstruct import load_pretrained
from nlstruct.datasets import load_from_brat, export_to_brat

ner = load_pretrained("model.pt")
ner.eval()
ner.predict({"doc_id": "doc-0", "text": "Je lui prescris du lorazepam."})
# Out: 
# {'doc_id': 'doc-0',
#  'text': 'Je lui prescris du lorazepam.',
#  'entities': [{'entity_id': 0,
#    'label': ['substance'],
#    'attributes': [],
#    'fragments': [{'begin': 19,
#      'end': 28,
#      'label': 'substance',
#      'text': 'lorazepam'}],
#    'confidence': 0.9998705969553088}]}
export_to_brat(ner.predict(load_from_brat("path/to/brat/test")), filename_prefix="path/to/exported_brat")
```

### How to train a NER model followed by a span classification model

```python
from nlstruct.recipes import train_qualified_ner

model = train_qualified_ner(
    dataset={
        "train": "path to your train brat/standoff data",
        "val": 0.05,  # or path to your validation data
        # "test": # and optional path to your test data
    },
    finetune_bert=False,
    seed=42,
    bert_name="camembert/camembert-base",
    fasttext_file="",
    gpus=0,
    xp_name="my-xp",
    return_model=True,
)
model.save_pretrained("model.pt")
```

## Ensembling

Easily ensemble multiple models (same architecture, different seeds):
```python
model1 = load_pretrained("model-1.pt")
model2 = load_pretrained("model-2.pt")
model3 = load_pretrained("model-3.pt")
ensemble = model1.ensemble_with([model2, model3]).cuda()
export_to_brat(ensemble.predict(load_from_brat("path/to/brat/test")), filename_prefix="path/to/exported_brat")
```

## Advanced use

Should you need to further configure the training of a model, please modify directly one 
of the recipes located in the [recipes](nlstruct/recipes/) folder.


### Install

This project is still under development and subject to changes.

```bash
pip install nlstruct==0.2.0
```
