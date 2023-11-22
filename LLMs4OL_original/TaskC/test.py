import json

from configuration import BaseConfig
from datahandler import DataReader, DataWriter
import argparse
import datetime
from src import ZeroShotPromptClassifierFactory, EvaluationMetrics
import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
# openai.api_key  = os.environ['OPENAI_API_KEY']


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb_name", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--device", required=True)
    args = parser.parse_args()

    print("args:", args)
    config = BaseConfig().get_args(kb_name=args.kb_name, model=args.model)
    start_time = datetime.datetime.now()
    print("Starting the Inference time is:", str(start_time).split('.')[0])
    dataset = DataReader.load_json(config.processed_test)
    templates = DataReader.load_text(config.template_text).split("\n")
    template = templates[config.template]
    print(f"Working on template: {config.template}: {template}")
    label_mapper = DataReader.load_json(config.labels_path)

    zero_shot_prompt_classifier = ZeroShotPromptClassifierFactory(model_name = config.model_name)

    model = zero_shot_prompt_classifier(model_name=config.model_name,
                                         model_path=config.model_path,
                                         dataset=dataset,
                                         template=template,
                                         label_mapper=label_mapper,
                                         device=args.device)


    if "gpt" in config.model_name:
        # config.model_name == "gpt3" or config.model_name == "gpt3-ada":
        print("Runing model: ", config.model_name)
        results = model.test()
        print(f"output predictions in :{config.model_output}")
        # Serializing json
        json_object_res = json.dumps(results, indent=4)
        model_output = os.path.abspath(config.model_output)
        # Writing to sample.json
        with open(model_output, "w") as outfile:
            outfile.write(json_object_res)
        # DataWriter.write_json(results, config.model_output)
    else:
        y_true, y_pred  = model.test()
        results = EvaluationMetrics.evaluate(actual=y_true, predicted=y_pred)
        print("F1-Score:", results['clf-report']['macro avg']['f1-score'])
        report_dict = {
            "baseline-run-args": str(args),
            "report_output_refrence": config.report_output,
            "results": results,
            "dataset-in-use": str(args.kb_name),
            "configs": vars(config)
        }

        print(f"scoring results in:{config.report_output}")
        # Serializing json
        json_object_res = json.dumps(report_dict, indent=4)
        report_output = os.path.abspath(config.report_output)
        # Writing to sample.json
        with open(report_output, "w") as outfile:
            outfile.write(json_object_res)
        # DataWriter.write_json(report_dict, config.report_output)
        end_time = datetime.datetime.now()
        print("Ending the Inference time is:", str(end_time).split('.')[0])
        print("Total duration is===>", str(end_time - start_time))