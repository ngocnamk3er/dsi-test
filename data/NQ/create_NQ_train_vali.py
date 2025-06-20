import datasets
import random
import numpy as np
import json

random.seed(313)

NUM_TRAIN = 8000
NUM_EVAL = 2000

# data = datasets.load_dataset('natural_questions', cache_dir='cache')['train']


base_url = "https://huggingface.co/datasets/google-research-datasets/natural_questions/resolve/main/default/"
data_files = {
    "train": [
        base_url + "train-00000-of-00287.parquet",
        base_url + "train-00001-of-00287.parquet",
        base_url + "train-00002-of-00287.parquet",
        base_url + "train-00003-of-00287.parquet",
        base_url + "train-00004-of-00287.parquet",
        base_url + "train-00005-of-00287.parquet",
        base_url + "train-00006-of-00287.parquet",
        base_url + "train-00007-of-00287.parquet",
        base_url + "train-00008-of-00287.parquet",
        base_url + "train-00009-of-00287.parquet",
        base_url + "train-00010-of-00287.parquet",
        base_url + "train-00011-of-00287.parquet",
        base_url + "train-00012-of-00287.parquet",
        base_url + "train-00013-of-00287.parquet",
        base_url + "train-00014-of-00287.parquet",
        base_url + "train-00015-of-00287.parquet",
        base_url + "train-00016-of-00287.parquet",
        base_url + "train-00017-of-00287.parquet",
        base_url + "train-00018-of-00287.parquet",
        base_url + "train-00019-of-00287.parquet",
        base_url + "train-00020-of-00287.parquet",
        
    ]
}

data = datasets.load_dataset("parquet", data_files=data_files, split="train")

rand_inds = list(range(len(data)))
random.shuffle(rand_inds)

title_set = set()
current_docid = 0

with open("NQ_10k_multi_task_train.json", "w") as tf, open(
    "NQ_10k_valid.json", "w"
) as vf:
    for ind in rand_inds:
        title = data[ind]["document"][
            "title"
        ]  # we use title as the doc identifier to prevent two docs have the same text
        if title not in title_set:
            title_set.add(title)
            token_inds = np.where(
                np.array(data[ind]["document"]["tokens"]["is_html"]) == False
            )[0]
            tokens = np.array(data[ind]["document"]["tokens"]["token"])[token_inds]
            doc_text = " ".join(tokens)
            question_text = data[ind]["question"]["text"]

            jitem = json.dumps(
                {"text_id": str(current_docid), "text": "document: " + doc_text}
            )
            tf.write(jitem + "\n")
            jitem = json.dumps(
                {"text_id": str(current_docid), "text": "question: " + question_text}
            )
            if len(title_set) <= NUM_TRAIN:
                tf.write(jitem + "\n")
            else:
                vf.write(jitem + "\n")
            current_docid += 1
            if len(title_set) == NUM_TRAIN + NUM_EVAL:
                break
        print(
            f"Creating training and validation dataset: {'{:.1%}'.format(len(title_set)/(NUM_TRAIN + NUM_EVAL))}",
            end="\r",
        )
