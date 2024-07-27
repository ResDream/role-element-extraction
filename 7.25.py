import ast

import SparkApi
import json

# 以下密钥信息从控制台获取
appid = "9918e391"  # 填写控制台中获取的 APPID 信息
api_secret = "NGQ3ZDFjODc3ODUxMmNmZGY0ODExZGU4"  # 填写控制台中获取的 APISecret 信息
api_key = "139ed0c8da9d148ecc72bbed3cfa986e"  # 填写控制台中获取的 APIKey 信息

# 调用微调大模型时，设置为“patch”
domain = "patchv3"
# domain = "patch"

# 云端环境的服务地址
# Spark_url = "wss://spark-api-n.xf-yun.com/v1.1/chat"  # 微调v1.5环境的地址
Spark_url = "wss://spark-api-n.xf-yun.com/v3.1/chat"  # 微调v3.0环境的地址

text = []


# length = 0

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
    # print('prompt',prompt)
    text.clear
    Input = prompt
    question = checklen(getText("user", Input))
    SparkApi.answer = ""
    # print("星火:",end = "")
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    getText("assistant", SparkApi.answer)
    # print(text)
    return text[-1]['content']


import json

# 你的 core_run 函数和相关的代码需要在这里定义或导入
# from your_module import core_run

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
    """
    确保输出包含所有必需字段，并填充默认值。
    """
    for key, key_type in required_keys.items():
        if key not in output or not isinstance(output[key], key_type):
            # 根据字段类型填充默认值
            if key_type == str:
                output[key] = ""
            elif key_type == list:
                output[key] = []
    return output


# 读取 JSONL 文件并处理每一行的输入
input_file = 'dataset/my_test.jsonl'
output_file = 'output.json'

# 存储结果的列表
results = []

# 读取文件并处理
with open(input_file, 'r', encoding='utf-8') as f:
    for index, line in enumerate(f):
        # 解析每一行的 JSON
        data = json.loads(line)
        # 获取 input 字段的内容
        user_input = data['input']

        # 调用核心函数获取模型返回值
        text = []
        model_output = core_run(text, user_input)
        # print(model_output)
        try:
            model_output_json = ast.literal_eval(model_output)
        except:
            model_output = core_run(text, model_output+"无法解析，请重新生成，回复不允许出现其他任何无关json的内容")
            model_output_json = ast.literal_eval(model_output)
        print(model_output_json)

        # 确保模型输出是 JSON 并包含所有必需字段
        try:
            if isinstance(model_output_json, list) and len(model_output_json) > 0:
                if len(model_output_json) > 1:
                    model_output_json = ensure_required_keys(model_output_json[1], required_keys)
                else:
                    model_output_json = ensure_required_keys(model_output_json[0], required_keys)  # 提取列表中的第一个元素并确保其包含所有必需字段
            model_output_json = ensure_required_keys(model_output_json, required_keys)
        except :
            # 如果模型输出不是有效的 JSON，使用空值填充
            print(index)
            print("ERROR")
            model_output_json = ensure_required_keys({}, required_keys)

        print(model_output_json)

        # 将结果存储在列表中
        result = {
            "infos": [model_output_json],
            "index": index + 1
        }
        results.append(result)

# 将结果写入 28.37.json 文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print(f'Results have been written to {output_file}')
