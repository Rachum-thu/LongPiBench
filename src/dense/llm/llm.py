# new api interfaces for commercial models
from .claude3haiku import claude_generate
from .gpt4omini import gpt_generate
from .glm import glm_generate
from .gemini import gemini_generate
from .deepseek import deepseek_generate


# new api interfaces for open-source models
from .qwen import qwen_generate
from .llama import llama3_generate
from .wizard import wizard_generate

def llm_generate(
    inputs,
    model,
    temp=0.0,
    top_p=0.9,
    mute_tqdm=False,
):
    if model == "claude":
        return claude_generate(inputs, temp=temp, top_p=top_p, mute_tqdm=mute_tqdm)
    elif model == "gpt":
        return gpt_generate(inputs, temp=temp, top_p=top_p, mute_tqdm=mute_tqdm)
    elif model == "glm":
        return glm_generate(inputs, temp=temp, top_p=top_p, mute_tqdm=mute_tqdm)
    elif model == "gemini":
        return gemini_generate(inputs, temp=temp, top_p=top_p, mute_tqdm=mute_tqdm)
    elif model == "deepseek":
        return deepseek_generate(inputs, temp=temp, top_p=top_p, mute_tqdm=mute_tqdm)
    elif model == "qwen_7b":
        return qwen_generate(inputs, model="qwen2.5-7b-instruct", temp=temp, top_p=top_p, mute_tqdm=mute_tqdm)
    elif model == "qwen_14b":
        return qwen_generate(inputs, model="qwen2.5-14b-instruct", temp=temp, top_p=top_p, mute_tqdm=mute_tqdm)
    elif model == "qwen_32b":
        return qwen_generate(inputs, model="qwen2.5-32b-instruct", temp=temp, top_p=top_p, mute_tqdm=mute_tqdm)
    elif model == "qwen_72b":
        return qwen_generate(inputs, model="qwen2.5-72b-instruct", temp=temp, top_p=top_p, mute_tqdm=mute_tqdm)
    elif model == "llama_70b":
        return llama3_generate(inputs, model="meta-llama/Meta-Llama-3.1-70B-Instruct", temp=temp, top_p=top_p, mute_tqdm=mute_tqdm)
    elif model == "wizard":
        return wizard_generate(inputs, temp=temp, top_p=top_p, mute_tqdm=mute_tqdm)