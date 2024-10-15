import os
import fire
import json

from dense.llm import llm_generate
from dense.eval import EquationSolutionMetric, HistoryReorderMetric, SQLMetric

# Mapping for the model and metric
Metric = {
    "history_reorder_absolute": HistoryReorderMetric,
    "history_reorder_relative": HistoryReorderMetric,
    "table_sql_absolute": SQLMetric,
    "table_sql_relative": SQLMetric,
    "equation_solution_absolute": EquationSolutionMetric,
    "equation_solution_relative": EquationSolutionMetric,
}

def select_prompt(head_query: bool, tail_query: bool):
    assert head_query or tail_query, "At least one of head_query and tail_query should be True."
    if head_query and tail_query:
        return "default_prompt"
    elif head_query:
        return "query_head_prompt"
    elif tail_query:
        return "query_tail_prompt"

def main(
    model: str,
    task: str,
    length_lower_bound: int,
    length_upper_bound: int,
    seed_num: int,
    head_query: bool,
    tail_query: bool
):
    """
    Main function to process the data and evaluate using specified model and task.

    Parameters:
    model (str): The model to use for inference.
    task (str): The task for evaluation.
    length_lower_bound (int): The lower bound of length for sampling data.
    length_upper_bound (int): The upper bound of length for sampling data.
    num_per_grid (int): The number of samples per grid.
    """
    if head_query and tail_query:
        save_dir = f"res/{model}/{task}"
    elif head_query:
        save_dir = f"res/{model}/{task}_head"
    elif tail_query:
        save_dir = f"res/{model}/{task}_tail"
    
    # Ensure the save directory exists and is empty
    os.makedirs(save_dir, exist_ok=True)
    assert len(os.listdir(save_dir)) == 0, "The save_dir should be empty. Please check the path."
    
    # Load and sample data
    with open(f"data/{task}.json") as file:
        data = json.load(file)
    
    # sample a subset
    def valid_length(elem):
        return length_lower_bound <= elem['token_level'] <= length_upper_bound
    
    def valid_seed_num(elem):
        int_seed = int(elem['seed_id'].split('_')[-1])
        return int_seed <= seed_num

    sampled_data = [elem for elem in data if valid_length(elem) and valid_seed_num(elem)]

    metric = Metric[task]()
    
    # Prepare inputs for inference
    prompt_type = select_prompt(head_query, tail_query)
    
    inputs = [
        {
            "system_prompt": elem[prompt_type]['system_prompt'],
            "user_message": elem[prompt_type]["user_message"].format(
                context=elem['context'], 
                query=elem['question']
            )
        }
        for elem in sampled_data
    ]
    
    # Perform inference and get responses
    str_responses = llm_generate(inputs, model)
    
    # Extract labels and evaluate responses
    labels = [elem["answers"] for elem in sampled_data]
    
    # Append responses to the sampled data
    for i, elem in enumerate(sampled_data):
        elem["llm_response"] = str_responses[i]
    
    with open(os.path.join(save_dir, "generates.json"), 'w') as file:
        json.dump(sampled_data, file, indent=4)
    
    with open(os.path.join(save_dir, "generates.json"), 'r') as file:
        sampled_data = json.load(file)

    str_responses = [elem["llm_response"] for elem in sampled_data]
    labels = [elem['answers'] for elem in sampled_data]
        
    scores = metric.evaluate(str_responses, labels)    
    # Append scores to the sampled data
    for i, elem in enumerate(sampled_data):
        elem["score"] = scores[i]
    
    # Analyze and save the results
    with open(os.path.join(save_dir, "results.json"), 'w') as file:
        json.dump(sampled_data, file, indent=4)
        
    # if successfully saved, remove the generates.json because all the information is in results.json
    os.remove(os.path.join(save_dir, "generates.json"))

if __name__ == "__main__":
    fire.Fire(main)
