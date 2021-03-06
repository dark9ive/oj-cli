import json
import os

from constants import TEMPLATE_FILENAME
from util.curl import curl


def get_problem(problem_id):
    endpoint = "problem?problem_id={}".format(problem_id)
    result = json.loads(curl("get", endpoint=endpoint, use_x_csrf_token=True))
    data = result["data"]
    if not data:
        print("Unexpected Error with Server")
        return
    try:
        samples = data["samples"]
        templates = data["template"]
        languages = data["languages"]
    except:
        print("Unexpected Error in Parsing Response")
        return
    dir_name = "problem_{}".format(problem_id)
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

    for language in languages:
        if language not in templates:
            continue
        template_file = dir_name + "/{}".format(TEMPLATE_FILENAME[language])
        content = templates[language]
        with open(template_file, "wt") as fout:
            fout.write(content)
            # TODO: Update to support utf-8 encoding.
    for idx, sample in enumerate(samples):
        sample_num = idx + 1
        input_sample_path = dir_name + "/" + "{}.in".format(sample_num)
        input_ = sample["input"]
        with open(input_sample_path, "wt") as fout:
            fout.write(input_)
            # TODO: Update to support utf-8 encoding.
        output_sample_path = dir_name + "/" + "{}.out".format(sample_num)
        output = sample["output"]
        with open(output_sample_path, "wt") as fout:
            fout.write(output)
            # TODO: Update to support utf-8 encoding.
