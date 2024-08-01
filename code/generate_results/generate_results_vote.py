import ast
import json
from collections import Counter

import SparkApi

# 以下密钥信息从控制台获取
appid = "9918e391"  # 填写控制台中获取的 APPID 信息
api_secret = "NGQ3ZDFjODc3ODUxMmNmZGY0ODExZGU4"  # 填写控制台中获取的 APISecret 信息
api_key = "139ed0c8da9d148ecc72bbed3cfa986e"  # 填写控制台中获取的 APIKey 信息

# 调用微调大模型时，设置为“patch”
domain = "patchv3"

# 云端环境的服务地址
Spark_url = "wss://spark-api-n.xf-yun.com/v3.1/chat"  # 微调v3.0环境的地址

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

def ensure_required_keys(output, required_keys):
    for key, key_type in required_keys.items():
        if key not in output or not isinstance(output[key], key_type):
            if key_type == str:
                output[key] = ""
            elif key_type == list:
                output[key] = []
    return output

def aggregate_results(results_list):
    aggregated_results = {}
    for key, key_type in required_keys.items():
        if key_type == str:
            value_counts = Counter(result[key] for result in results_list)
            aggregated_results[key] = value_counts.most_common(1)[0][0] if value_counts else ""
        elif key_type == list:
            list_counter = Counter()
            for result in results_list:
                list_counter.update(result[key])
            aggregated_results[key] = [item for item, count in list_counter.most_common()]
    return aggregated_results

input_file = '../../user_data/test_processed.jsonl'
output_file = '../../prediction_result/result.json'
results = []

with open(input_file, 'r', encoding='utf-8') as f:
    for index, line in enumerate(f):
        print(index)
        data = json.loads(line)
        user_input = data['input']

        temp_results = []
        for _ in range(10):
            text = []
            model_output = core_run(text, user_input)
            model_output_json = ast.literal_eval(model_output)

            try:
                if isinstance(model_output_json, list) and len(model_output_json) > 0:
                    model_output_json = ensure_required_keys(model_output_json[0], required_keys)
                model_output_json = ensure_required_keys(model_output_json, required_keys)
            except:
                model_output_json = ensure_required_keys({}, required_keys)

            temp_results.append(model_output_json)

        final_result = aggregate_results(temp_results)
        print(final_result)

        result = {
            "infos": [final_result],
            "index": index + 1
        }
        results.append(result)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print(f'Results have been written to {output_file}')
