#!/bin/bash

# Define the list of models
OPEN_SOURCE_MODELS=("qwen_14b")
COMMERCIAL_MODELS=("gpt")
MODELS=("${OPEN_SOURCE_MODELS[@]}" "${COMMERCIAL_MODELS[@]}")

# Define the list of tasks
TASKS=("table_sql_absolute" "table_sql_relative")

# Common parameters
LENGTH_LOWER_BOUND=32000
LENGTH_UPPER_BOUND=32000
SEED_NUM=20
HEAD_QUERY=False
TAIL_QUERY=True

# Loop over each model
for MODEL in "${MODELS[@]}"
do
    echo "----------------------------------------"
    echo "Evaluating Model: $MODEL"
    echo "----------------------------------------"

    # Loop over each task
    for TASK in "${TASKS[@]}"
    do
        echo "  Running Task: $TASK"

        # Execute the evaluation script
        python3 eval/eval.py \
            --model "$MODEL" \
            --length_lower_bound "$LENGTH_LOWER_BOUND" \
            --length_upper_bound "$LENGTH_UPPER_BOUND" \
            --task "$TASK" \
            --seed_num "$SEED_NUM" \
            --head_query "$HEAD_QUERY" \
            --tail_query "$TAIL_QUERY"

        # Check if the Python script executed successfully
        if [ $? -ne 0 ]; then
            echo "    Error: Evaluation failed for Model: $MODEL, Task: $TASK"
            exit 1
        else
            echo "    Success: Evaluation completed for Model: $MODEL, Task: $TASK."
        fi
    done
done

echo "All evaluations completed successfully."
