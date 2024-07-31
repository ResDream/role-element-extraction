import ast
import json
import random
import SparkApi

# Define the keys for validation
required_keys = {
    "基本信息-姓名": str,
    "基本信息-手机号码": str,
    "基本信息-邮箱": str,
    "基本信息-地区": str,
    "基本信息-详细地址": str,
    "基本信息-性别": str,
    "基本信息-年龄": str,
    "基本信息-生日": str,
    "咨询类型": list,
    "意向产品": list,
    "购买异议点": list,
    "客户预算-预算是否充足": str,
    "客户预算-总体预算金额": str,
    "客户预算-预算明细": str,
    "竞品信息": str,
    "客户是否有意向": str,
    "客户是否有卡点": str,
    "客户购买阶段": str,
    "下一步跟进计划-参与人": list,
    "下一步跟进计划-时间点": str,
    "下一步跟进计划-具体事项": str
}

# Spark API credentials
appid = "9918e391"
api_secret = "NGQ3ZDFjODc3ODUxMmNmZGY0ODExZGU4"
api_key = "139ed0c8da9d148ecc72bbed3cfa986e"
domain = "patchv3"
Spark_url = "wss://spark-api-n.xf-yun.com/v3.1/chat"

text = []

def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

def core_run(text, prompt):
    text.clear()
    Input = prompt
    question = checklen(getText("user", Input))
    SparkApi.answer = ""
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    getText("assistant", SparkApi.answer)
    return text[-1]['content']

def ensure_required_keys(output, required_keys):
    for key, key_type in required_keys.items():
        if key not in output or not isinstance(output[key], key_type):
            if key_type == str:
                output[key] = ""
            elif key_type == list:
                output[key] = []
    return output

def load_train_examples(train_file, num_examples=0):
    with open(train_file, 'r', encoding='utf-8') as f:
        train_data = json.load(f)
        return random.sample(train_data, num_examples)

def format_few_shot_examples(examples):
    formatted_examples = ""
    for example in examples:
        formatted_examples += "Example:\n"
        formatted_examples += f"ChatText:\n{example['chat_text']}\n"
        formatted_examples += f"Infos:\n{json.dumps(example['infos'], ensure_ascii=False, indent=4)}\n\n"
    return formatted_examples

# Read the few-shot examples from train.json
train_file = '../../user_data/train.json'
few_shot_examples = load_train_examples(train_file)
few_shot_context = format_few_shot_examples(few_shot_examples)

# Read the input file and process each line
input_file = '../../user_data/test_processed.jsonl'
output_file = '../../prediction_result/result.json'

results = []

with open(input_file, 'r', encoding='utf-8') as f:
    for index, line in enumerate(f):
        print(index)
        data = json.loads(line)
        user_input = data['input']

        # Modify the input to include few-shot examples
        modified_input = few_shot_context + "Instruction:\n" + user_input

        # print(modified_input)
        # break

        # Call the core function to get the model output
        text = []
        model_output = core_run(text, modified_input)
        model_output_json = ast.literal_eval(model_output)

        # Ensure the output contains all required fields
        try:
            if isinstance(model_output_json, list) and len(model_output_json) > 0:
                model_output_json = ensure_required_keys(model_output_json[0], required_keys)
            model_output_json = ensure_required_keys(model_output_json, required_keys)
        except:
            model_output_json = ensure_required_keys({}, required_keys)

        # Store the result
        result = {
            "infos": [model_output_json],
            "index": index + 1
        }
        results.append(result)

# Write the results to the output file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print(f'Results have been written to {output_file}')
