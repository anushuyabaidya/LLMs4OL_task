# LLMs4OL: Large Language Models for Ontology Learning

## Summary:
This paper introduces a new approach called LLMs4OL that stands for Large Language Models for Ontology Learning.
They utilize the capabilities of Large Language Models (LLMs) for important knowledge engineerng task of Ontology Learning (OL).
It investigates whether LLMs can effectively apply complex language patterns to automatically extract structured knowledge from natural language text.
The authors comprehensively evaluates nine different state-of-the-art LLM architectures on three core OL tasks - term typing, taxonomy discovery, and non-taxonomic relation extraction. 
The tasks are tested on prominent ontological knowledge sources like WordNet, GeoNames, UMLS
Prompt templates are used to instruct the LLMs to generate predictions in a zero-shot setting. 
Results indicate foundational LLMs may not yet be suitable for practical ontology construction that requires reasoning skills and domain expertise. 
However, they show potential as assistants to aid the knowledge acquisition process when strategically fine-tuned.

## WorkFlow Architecture:
- The paper proposes the LLMs4OL paradigm which uses Large Language Models (LLMs) for Ontology Learning (OL) in a zero-shot setting.
- It relies on carefully designed prompt templates to instruct the LLMs to perform 3 core OL tasks:
   - Term typing - Discover a generalized type for a input term
   - Taxonomy discovery - Recognize taxonomic "is-a" hierarchies between types
   - Non-taxonomic relation extraction - Discover relationships between types
- For each task, they design cloze-style and prefix-style prompt templates that encode the task as a textual statement with blanks or placeholders for the LLM to fill in.
- The models tested cover various architectures like BERT, BART, GPT variants, Flan-T5 across different sizes. Testing on diverse models allows comparative analysis.
- Evaluations use testsets from ontologies like WordNet, GeoNames, UMLS, schema.org. Metrics are MAP@1 for TaskA: term typing and F1-score for TaskB: taxonomy and TaskC: relation extraction tasks

## Input/Output
- Input is a prompt template instantiated with ontology terms/types/relations and relevant context per task.
- Output is model's predicted term type or truth value of taxonomic/non-taxonomic statement.
- For Example:
  - Input: "Aspirin in medicine is a [MASK]"
  - Output: "[drug]"

## How to run the code?
### Pre-requirements:
- #### Download Dataset:
  Since the original LLMs4OL repository doesnot contain the LLM models and large size dataset files we need to first make sure we have them
  - Download the WN18RR Dataset from : 
    - https://github.com/villmow/datasets_knowledge_embedding/tree/master/WN18RR
    - Place it to datasets/TaskA/WN18RR/raw folder
  - Download files required for geonames:
    - https://download.geonames.org/export/dump/
      - download allcountries.zip
        - extract and get allcountries.txt
      - download featureCodes_en.txt
      - Place it to datasets/TaskA/Geonames/raw folder
  - Download UMLs dataset from:
    - https://www.nlm.nih.gov/research/umls/licensedcontent/umlsarchives04.html
    - This will require sign in and apply/request to access the dataset- might take upto 3 bussiness days.
    - Download the 2022AB full Release
    - Place it to datasets/TaskA/UMLs/raw folder
- #### Install requirements.txt:
  Since the requirements.txt file in the origin LLMs4OL repository didnot satisfy the needs for few pacakges required to run the code, I have created an update requirements.txt file
  - You can access it at the root folder as ``` requirements.txt ```
  - You can run ``` pip install -r requirements.txt ``` to install the required packages.
- #### Create all required data files:
  Run two .py files so that we have all the required format datasets
  - These files will create the required other formatted files that we require to test the code and recreate the results.
    - Run LLMs4OL_original/TaskA/build_entity_datasets.py
    - Run LLMs4OL_original/TaskA/prepare_datasets.py
- #### Download LLM models:
  After this dataset that we require to run will be complete, now we need to insure we have the LLMs 
  - Download models bert-large-uncased, facebook/bart-large, bigscience/bloom-7b1, google/flan-t5-xl, meta-llama/Llama-2-7b, and more. (All you want to run test on.)
  - To download these you can run the code:
  - ``` 
    from transformers import AutoTokenizer,AutoModel
    model_path="facebook/bart-large" #Change Model Name here.
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModel.from_pretrained(model_path) 
    ```
  - Once the models are downloaded it will be stored in .cache folder ``` /.cache/hugginface/hub ```
    - You can copy the models from the above path and place it to ``` LLMs4OL_original/assets/LLMs/```
    - Create folder for each LLM model and place it there, the folder name will be the model names
    - For example: 
      - bart_large
      - flan-t5-xl
      - bloom-1b7, etc
- #### Start Testing:
- You can now run the test and see the results
- To run the test you need to run a command with desired inputs
- For TaskA:
  - Command:
    ```commandline
    python test.py --kb_name='KB_NAME' --model_name='MODEL_NAME' --template='TEMPLATE' --device='DEVICE'
    ```
  - For example: ``` python test.py --kb_name="wn18rr" --model_name="bert_large" --template="template-1" --device="cpu" ```
- For TaskB:
  - Command:
    ```commandline
    python test.py --kb_name="KB_NAME" --model="MODEL_NAME" --template="TEMPLATE" --device="DEVICE"
    ```
  - For example: ``` python test.py --kb_name="geonames" --model="bert_large" --template="1" --device="cpu" ```
- For TaskC
- - Command:
    ```commandline
    python test.py --kb_name="KB_NAME" --model="MODEL_NAME" --device="cpu"
    ```
  - For example: ``` python test.py --kb_name="umls" --model="bert_large" --device="cpu" ``` 
- After running these commands the results will be stored in Task respective results folder with timestamp
  - For example: 
    - if we ran command for TaskA then the results will be stored in ``` LLMs4OL_original/TaskA/results/wn18rr/bert_large/report-bert_large-template-8-2023-11-21 18_44_36.json ```
    - The results will look somewhat like this: task/results/dataset_name/model_name/file_with_template_timestamp.json

## Results:
- ### For TaskA: Term typing
  - ```commandline
      python test.py --kb_name="wn18rr" --model_name="bert_large" --template="template-1" --device="cpu"
      ```
    - Result: ``` {
          "MAP@1": 0.021964097148891235,
          "MAP@5": 0.021964097148891235,
          "MAP@10": 0.021964097148891235
      }```
      - The results were the same as in the original paper.
      - The full results are in ``` LLMs4OL_original/TaskA/results/wn18rr/bert_large/report-bert_large-template-1-2023-11-21 18_43_08.json ```
  - ```commandline
      python test.py --kb_name="wn18rr" --model_name="bert_large" --template="template-8" --device="cpu"
      ```
    - Result: ``` {
          "MAP@1": 0.2785638859556494,
          "MAP@5": 0.2785638859556494,
          "MAP@10": 0.2785638859556494
      }```
      - The results were the same as in the original paper.
      - The full results are in ``` LLMs4OL_original/TaskA/results/wn18rr/bert_large/report-bert_large-template-8-2023-11-21 18_44_36.json ```
  - ```commandline
     python test.py --kb_name="wn18rr" --model_name="flan_t5_xl" --template="template-8" --device="cpu"
    ```
      - Result: ``` {'MAP@1': 0.0, 'MAP@5': 0.0, 'MAP@10': 0.0} ```
        - This result seemed off and I did rerun it as well but the results did not change, I think this might be because the LLM model I downloaded was different from the model the original LLMs4OL used.
        - The full results are in ``` LLMs4OL_original/TaskA/results/wn18rr/flan_t5_xl/report-flan_t5_xl-template-8-2023-11-21 17_47_44.json ```

- ### For TaskB: Taxonomy discovery
  - ```commandline
    python test.py --kb_name="geonames" --model="bert_large" --template="1" --device="cpu"
      ```
    - Result: ``` F1-score: 0.5169802310788779 ```
      - The result was increased from original 0.41 to 0.5169
      - The full results are in ``` LLMs4OL_original/TaskB/results/geonames/bert_large/report-bert_large-1-2023-11-21 19_15_24.json ```
  - ```commandline
    python test.py --kb_name="geonames" --model="bart_large" --template="1" --device="cpu"
      ```
    - Result: ``` F1-score: 0.41033605190046646 ```
      - The result was increased from original 0.3811 to 0.4103
      - The full results are in ``` LLMs4OL_original/TaskB/results/geonames/bart_large/report-bart_large-1-2023-11-21 19_07_54.json ```

- ### For TaskC: Non-taxonomic relation extraction
  - ```commandline
    python test.py --kb_name="umls" --model="bert_large" --device="cpu"
      ```
    - Result: ``` F1-Score: 0.4010718282929362 ```
      - The results were the same as in the original paper.
      - The full results are in ``` LLMs4OL_original/TaskC/results/umls/bert_large/report-bert_large-2023-11-21 19_18_19.json ```

  - ```commandline
    python test.py --kb_name="umls" --model="bart_large" --device="cpu"
      ```
    - Result: ``` F1-Score: 0.4235504359995694 ```
      - The results were the same as in the original paper.
      - The full results are in ```LLMs4OL_original/TaskC/results/umls/bart_large/report-bart_large-2023-11-21 19_31_38.json ```
