# LongPiBench

**LongPiBench** is a benchmark designed to assess the positional biases in large language models (LLMs) when processing long contexts, specifically targeting biases arising from the spacing of multiple pieces of relevant information. 

## Overview

LongPiBench evaluates how well long-context LLMs handle tasks that involve multiple relevant information pieces distributed throughout the input context. The benchmark focuses on two types of positional biases:

- **Absolute Positional Bias**: The position of relevant information in the input (beginning, middle, end).
- **Relative Positional Bias**: The spacing between relevant information pieces and how densely they are distributed across the context.

The benchmark includes tasks of varying complexity and spans four different input lengths: 32K, 64K, 128K, and 256K tokens.

## Key Features

- **Comprehensive Evaluation**: LongPiBench is the most comprehensive benchmark for isolating and analyzing positional biases in long-context LLMs. It tests the impact of both absolute and relative positional biases on model performance.
- **Diverse Tasks**: The benchmark contains three primary tasks:
  - **Table SQL**: A retrieval task that requires models to extract relevant entries from a large table.
  - **Timeline Reordering**: A challenging task where models must sort events in chronological order.
  - **Equation Solving**: The most complex task, requiring models to retrieve and solve equations across a long context.
- **11 Model Evaluations**: Thorough experiments have been conducted across eleven popular LLMs, including open-source and commercial models.

## Installation

To install and run the LongPiBench benchmark, follow these steps:

```bash
git clone https://github.com/your-repo/LongPiBench.git
cd LongPiBench
pip install -r requirements.txt
```

## Usage

You can run the benchmark using the provided script. Here is an example command:

```bash
python run_benchmark.py --task table_sql --model gpt-4 --input_length 64k
```

Arguments:

- `--task`: The task to evaluate (`table_sql`, `timeline_reordering`, `equation_solving`).
- `--model`: The language model to evaluate.
- `--input_length`: The length of the input context (e.g., 32K, 64K, 128K, 256K).

## Dataset

LongPiBench includes 7,680 instances of multiple tasks across different input lengths. The dataset is designed to test models at varying levels of absolute and relative positional bias. Each instance contains 10 relevant pieces of information.

## Results

Our experiments highlight several key findings:

- While most current models are robust against the "lost in the middle" phenomenon, they exhibit significant biases related to the spacing between relevant information pieces.
- Model performance sharply declines as the distance between relevant pieces increases, though some robustness is observed with larger models.

For detailed experimental results, please refer to the paper [here](#).

## Contributing

Contributions are welcome! Please submit issues and pull requests to help improve LongPiBench.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you find the benchmark helpful, please consider citing out paper.

