import ast

import SparkApi

# 以下密钥信息从控制台获取
appid = "53289378"  # 填写控制台中获取的 APPID 信息
api_secret = "YjVhNDRhNjhmMTAwODJkNzViMWRiYzI2"  # 填写控制台中获取的 APISecret 信息
api_key = "a48cd344fd1edad1c96c8c1ff6994c3e"  # 填写控制台中获取的 APIKey 信息

# 调用微调大模型时，设置为“patch”
domain = "patchv3"

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
# input_file = R'my_train.jsonl'
input_file = R'my_test.jsonl'
output_file = 'toutput.json'

import os
from datetime import datetime

# 获取当前时间并格式化为字符串
current_time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# 创建以当前时间和input_file文件名共同命名的文件夹路径
output_dir = os.path.join("output", f"{current_time_str}_{os.path.basename(input_file).split('.')[0]}")
# 确保目录存在
os.makedirs(output_dir, exist_ok=True)
# 修改输出文件的路径，使其位于新创建的目录中
output_file = os.path.join(output_dir, 'output.json')

# 存储结果的列表
results = []
import json
from pydantic import BaseModel, ValidationError, constr, Field
from typing import List


class BasicInfoName(BaseModel):
    name: constr(min_length=1) = Field(alias='基本信息-姓名')
    id: int


class BasicInfoPhone(BaseModel):
    phone: constr() = Field(alias='基本信息-手机号码')
    id: int


class BasicInfoEmail(BaseModel):
    email: constr() = Field(alias='基本信息-邮箱')
    id: int


class BasicInfoRegion(BaseModel):
    region: constr() = Field(alias='基本信息-地区')
    id: int


class BasicInfoAddress(BaseModel):
    address: constr() = Field(alias='基本信息-详细地址')
    id: int


class BasicInfoGender(BaseModel):
    gender: constr() = Field(alias='基本信息-性别')
    id: int


class BasicInfoAge(BaseModel):
    age: constr() = Field(alias='基本信息-年龄')
    id: int


class BasicInfoBirthday(BaseModel):
    birthday: constr() = Field(alias='基本信息-生日')
    id: int


class ConsultType(BaseModel):
    consult_type: List[constr()] = Field(alias='咨询类型')
    id: int


class IntentionProduct(BaseModel):
    intention_product: List[constr()] = Field(alias='意向产品')
    id: int


class PurchaseObjections(BaseModel):
    purchase_objections: List[constr()] = Field(alias='购买异议点')
    id: int


class CustomerBudgetSufficient(BaseModel):
    budget_sufficient: constr() = Field(alias='客户预算-预算是否充足')
    id: int


class CustomerBudgetTotal(BaseModel):
    budget_total: constr() = Field(alias='客户预算-总体预算金额')
    id: int


class CustomerBudgetDetails(BaseModel):
    budget_details: constr() = Field(alias='客户预算-预算明细')
    id: int


class CompetitorInfo(BaseModel):
    competitor_info: constr() = Field(alias='竞品信息')
    id: int


class CustomerIntention(BaseModel):
    customer_intention: constr() = Field(alias='客户是否有意向')
    id: int


class CustomerBlockers(BaseModel):
    customer_blockers: constr() = Field(alias='客户是否有卡点')
    id: int


class CustomerPurchaseStage(BaseModel):
    customer_purchase_stage: constr() = Field(alias='客户购买阶段')
    id: int


class NextFollowUpParticipants(BaseModel):
    next_follow_up_participants: List[constr()] = Field(alias='下一步跟进计划-参与人')
    id: int


class NextFollowUpTime(BaseModel):
    next_follow_up_time: constr() = Field(alias='下一步跟进计划-时间点')
    id: int


class NextFollowUpDetails(BaseModel):
    next_follow_up_details: constr() = Field(alias='下一步跟进计划-具体事项')
    id: int


# 假设 input_file, output_file, required_keys 和 core_run 函数已经定义好
# 并且 ensure_required_keys 函数也已经定义好，用于确保 JSON 对象包含所有必需字段
# 初始化一个文件句柄，用于写入结果
# 注意：这里我们使用 'a' 模式（追加模式）来打开文件，这样每次写入都会追加到文件末尾
keys = ['基本信息-姓名', '基本信息-手机号码', '基本信息-邮箱', '基本信息-地区', '基本信息-详细地址', '基本信息-性别',
        '基本信息-年龄', '基本信息-生日', '咨询类型', '意向产品', '购买异议点', '客户预算-预算是否充足',
        '客户预算-总体预算金额', '客户预算-预算明细', '竞品信息', '客户是否有意向', '客户是否有卡点', '客户购买阶段',
        '下一步跟进计划-参与人', '下一步跟进计划-时间点', '下一步跟进计划-具体事项']

models = {
    '基本信息-姓名': BasicInfoName,
    '基本信息-手机号码': BasicInfoPhone,
    '基本信息-邮箱': BasicInfoEmail,
    '基本信息-地区': BasicInfoRegion,
    '基本信息-详细地址': BasicInfoAddress,
    '基本信息-性别': BasicInfoGender,
    '基本信息-年龄': BasicInfoAge,
    '基本信息-生日': BasicInfoBirthday,
    '咨询类型': ConsultType,
    '意向产品': IntentionProduct,
    '购买异议点': PurchaseObjections,
    '客户预算-预算是否充足': CustomerBudgetSufficient,
    '客户预算-总体预算金额': CustomerBudgetTotal,
    '客户预算-预算明细': CustomerBudgetDetails,
    '竞品信息': CompetitorInfo,
    '客户是否有意向': CustomerIntention,
    '客户是否有卡点': CustomerBlockers,
    '客户购买阶段': CustomerPurchaseStage,
    '下一步跟进计划-参与人': NextFollowUpParticipants,
    '下一步跟进计划-时间点': NextFollowUpTime,
    '下一步跟进计划-具体事项': NextFollowUpDetails
}


def validate_data(data, key):
    model = models[key]
    try:
        validated_data = model(**data)
        validated_dict = validated_data.model_dump(by_alias=True)
        validated_dict.pop('id', None)  # 移除 id 字段
        return validated_dict
    except ValidationError as e:
        print(f"Validation error for {key}: {e}")
        return None


with open(input_file, 'r', encoding='utf-8') as f:
    for index, line in enumerate(f):
        print("当前index:", index)
        # 解析每一行的 JSON
        result = {
            "infos": [],
            "index": index + 1
        }
        data = json.loads(line)
        # 获取 input 字段的内容
        user_input: str = data['input']
        for key in keys:
            single_input = user_input.replace("详细信息", key, 1)

            # 调用核心函数获取模型返回值
            text = []
            RETRY_TIMES = 1000
            for i in range(RETRY_TIMES):
                try:
                    model_output = core_run(text, single_input)
                    model_output_json = ast.literal_eval(model_output)
                    print(model_output_json)
                    validated_data = validate_data(model_output_json, key)
                    if validated_data:
                        print(validated_data)
                        id_value = model_output_json.get('id')
                        if len(result["infos"]) < id_value + 1:
                            result["infos"].append(validated_data)
                        result["infos"][id_value].update(validated_data)
                        break
                    break
                except Exception as e:
                    print(e)
                    continue  # 如果出错，继续下一次循环尝试
        results.append(result)
#         # 确保模型输出是 JSON 并包含所有必需字段
#         try:
#             if isinstance(model_output_json, list) and len(model_output_json) > 0:
#                 model_output_json = ensure_required_keys(model_output_json[0],
#                                                          required_keys)  # 提取列表中的第一个元素并确保其包含所有必需字段
#             model_output_json = ensure_required_keys(model_output_json, required_keys)
#         except Exception as e:
#             # 如果模型输出不是有效的 JSON，使用空值填充
#             print(index, "ERROR:", e)
#             model_output_json = ensure_required_keys({}, required_keys)
#
#         # 将结果直接写入文件
#         result = {
#             "infos": [model_output_json],
#             "index": index + 1
#         }
#         results.append(result)
with open(output_file, 'a', encoding='utf-8') as output_file_handle:
    json.dump(results, output_file_handle, ensure_ascii=False, indent=4)
print(f'Results have been written to {output_file}')
