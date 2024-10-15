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
git clone https://github.com/Rachum-thu/LongPiBench.git
cd LongPiBench
bash setup.sh
```

This Bash script will do the following things: 

- **Data Download and Extraction**: Downloads necessary data files (`data.zip` and `original_res.zip`) from specified URLs and extracts their contents into designated directories (`data` and `original_res`).
- **Environment Configuration**: Generates a `.env` file where you can input required API keys and URLs for various services. 
- **Conda Environment Setup**: Creates and activates a Conda environment named `longpibench` with Python version `3.10.14`. 
- **Python Dependencies Installation**: Upgrades `pip`, installs the Python packages listed in `requirements.txt`, and installs the local package in editable mode.

Remember to populate .env for the API keys. You may change API base of each model by modifying the script in  `src/llm` if you want to use different API platforms or use your local implementation. 

## Usage

You can run the benchmark using the provided script. 

Run this command to debug with a small scale of testing data.

```bash
bash eval/debug.sh
```

Then use this command to eval through the whole dataset.

```bash
bash eval/eval.sh
```

To investigate the impact of query contextualization, the script would be:

```bash
bash eval/eval_head.sh
```

```bash
bash eval/eval_tail.sh
```

For each script, you can change the configuration of tasks, models, instance length, data num and query position. The results will be saved at `res`. Then you can use the following script for visualization:

```bash
python res/visualize.py
```

## Results

Our experiments highlight several key findings:

- While most current models are robust against the "lost in the middle" phenomenon, they exhibit significant biases related to the spacing between relevant information pieces.
- Model performance sharply declines as the distance between relevant pieces increases, though some robustness is observed with larger models.

The original response are downloaded with the setup.sh script. You can have a good look at it in the `orginal_res` directory.

## Contributing

Contributions are welcome! Please submit issues and pull requests to help improve LongPiBench.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



