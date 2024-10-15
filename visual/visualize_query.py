import os
import json
import logging
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib import rcParams
import matplotlib.colors as mcolors
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Define task groups
TASKS_BY_SETTING = {
    'absolute': [
        'table_sql_absolute',
        'table_sql_absolute_tail',
        'table_sql_absolute_head'
    ],
    'relative': [
        'table_sql_relative',
        'table_sql_relative_tail',
        'table_sql_relative_head'
    ]
}

# Map task names to labels (replacing 'head' and 'tail' with 'front' and 'back')
TASK_LABELS = {
    'table_sql_absolute': 'both',
    'table_sql_absolute_tail': 'back',
    'table_sql_absolute_head': 'front',
    'table_sql_relative': 'both',
    'table_sql_relative_tail': 'back',
    'table_sql_relative_head': 'front'
}

# Define task colors (using new RGB values)
TASK_COLORS = {
    'front': (40/255, 120/255, 181/255),  # RGB(142, 207, 201)
    'both': (200/255, 36/255, 35/255),   # RGB(250, 127, 111)
    'back': (150/255, 195/255, 125/255)   # RGB(255, 190, 122)
}

# Define the list of models
MODELS = ['gpt', 'qwen_14b']  # Modify as needed

# Marker size
MARKER_SIZE = 50

# Define border color and line width parameters
BORDER_COLOR = 'gray'         # Border color for the plot
BORDER_LINEWIDTH = 2.0        # Border line width for the plot
PLOT_LINEWIDTH = 3.0          # Line width for performance curves

def sanitize_filename(name):
    """Replace unsafe characters in the string with underscores."""
    return re.sub(r'[^A-Za-z0-9_\-]', '_', name)

def analyze_task_model(task, model):
    """
    Analyze performance data for a specific task and model.

    Parameters:
    task (str): Name of the task.
    model (str): Name of the model.

    Returns:
    dict: Average scores for each level.
    """
    res_dir = f'res/{model}/{task}/results.json'
    if not os.path.exists(res_dir):
        logging.warning(f"File does not exist: {res_dir}")
        return None
    try:
        with open(res_dir, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON in file {res_dir}: {e}")
        return None
    
    # Initialize lists for scores at different levels
    res = defaultdict(list)
    for item in data:
        res[item['level']].append(item['score'])
    
    # Check if the number of items at each level is consistent
    lengths = {len(v) for v in res.values()}
    if len(lengths) > 1:
        logging.error(f"Inconsistent number of items across levels, model: {model}, task: {task}")
        return None
    
    # Calculate average score for each level
    res_mean = {item: sum(vals)/len(vals) for item, vals in res.items()}
    return res_mean

def configure_plot_style():
    """
    Configure global plotting style.
    """
    rcParams.update({
        'figure.figsize': (4, 3),  # Set figure size to 4x3
        'axes.facecolor': 'white',
        'figure.facecolor': 'white',
        'axes.titlesize': 18,
        'axes.labelsize': 14,
        'legend.fontsize': 12,
        'xtick.labelsize': 12,  # Increase x-axis tick label size
        'ytick.labelsize': 12,  # Increase y-axis tick label size
    })
    plt.rcParams['axes.grid'] = False  # Disable gridlines globally
    plt.subplots_adjust(hspace=0.3, wspace=0.3)  # Reduce space between subplots

def set_axes_style(ax):
    """
    Set the border color of the axes to gray, remove tick lines, but keep tick labels.

    Parameters:
    ax (matplotlib.axes.Axes): The axes object to style.
    """
    # Set border color and line width
    for spine in ax.spines.values():
        spine.set_edgecolor(BORDER_COLOR)
        spine.set_linewidth(BORDER_LINEWIDTH)
    
    # Remove tick lines but keep tick labels
    ax.tick_params(axis='both', which='both', length=0)

def draw_line_graph(model: str, setting: str, data: dict):
    """
    Draw a line graph using the second code's style.

    Parameters:
    model (str): Model name.
    setting (str): Type of setting ('absolute' or 'relative').
    data (dict): Performance data for each task.
    """
    plt.figure(figsize=(4, 3))
    plt.xlabel('feature level', fontsize=14)
    plt.ylabel('recall rate', fontsize=14)
    plt.ylim(0, 1)
    plt.xlim(1, 16)
    
    # Get current axis
    ax = plt.gca()
    set_axes_style(ax)
    
    # Set custom x-axis ticks
    ax.set_xticks([1, 4, 8, 12, 16])
    ax.set_xticklabels([1, 4, 8, 12, 16])  # Optional: ensure tick labels match tick positions
    
    # Plot performance curve for each task
    for task_label, performance_data in data.items():
        if performance_data:  # Ignore empty data
            # Extract X and Y values
            x_values = sorted([int(level.split()[-1]) for level in performance_data.keys()])
            y_values = [performance_data[f'level {lvl}'] for lvl in x_values]
            
            # Select color based on the task
            color = TASK_COLORS.get(task_label, 'black')
            
            # Plot the line
            ax.plot(x_values, y_values, label=task_label, color=color, linewidth=PLOT_LINEWIDTH)
            
            # Plot data points with circular markers
            ax.scatter(x_values, y_values, color=color, s=MARKER_SIZE, marker='o', zorder=5)
    
    # Add legend (if needed)
    # ax.legend()
    
    # Create save path
    save_dir = 'res/fig'
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f'{model}_{setting}.png')
    
    # Save the figure
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    logging.info(f"Figure saved to: {save_path}")

def main():
    """
    Main function that iterates over models and settings, analyzes data, and generates plots.
    """
    # Configure global plotting style
    configure_plot_style()
    
    for model in MODELS:
        for setting in ['absolute', 'relative']:
            data = {}
            tasks = TASKS_BY_SETTING[setting]
            for task in tasks:
                task_label = TASK_LABELS[task]
                performance_data = analyze_task_model(task, model)
                if performance_data:
                    data[task_label] = performance_data
            draw_line_graph(model, setting, data)

if __name__ == '__main__':
    main()
