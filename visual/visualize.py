import os
import json
import logging
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib import rcParams
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Define tasks
TASKS = ['table_sql_absolute', 'table_sql_relative']

# Define model categories
REGULAR_MODELS = ['claude', 'deepseek', 'gemini', 'glm', 'gpt', 'llama_70b', 'wizard']
QWEN_MODELS = ['qwen_7b', 'qwen_14b', 'qwen_32b', 'qwen_72b']

# Define colors
ABSOLUTE_COLOR = '#1f77b4'  # Classic blue
RELATIVE_COLOR = '#ff7f0e'  # Classic orange

# Assign color gradients for Qwen series
qwen_absolute_cmap = cm.get_cmap('Blues', len(QWEN_MODELS))
qwen_relative_cmap = cm.get_cmap('Oranges', len(QWEN_MODELS))
QWEN_ABSOLUTE_COLORS = [mcolors.to_hex(qwen_absolute_cmap(i)) for i in range(len(QWEN_MODELS))]
QWEN_RELATIVE_COLORS = [mcolors.to_hex(qwen_relative_cmap(i)) for i in range(len(QWEN_MODELS))]

# Darken the lightest color
def darken_color(color, amount=0.7):
    """
    Darken a color.

    :param color: Original color (hexadecimal or RGB).
    :param amount: Degree to darken, between 0 and 1.
    :return: Darkened color (hexadecimal).
    """
    try:
        c = mcolors.to_rgb(color)
        darker = tuple(max(min(c_i * amount, 1), 0) for c_i in c)
        return mcolors.to_hex(darker)
    except Exception as e:
        logging.error(f"Unable to darken color: {color}, Error: {e}")
        return color

# Darken the lightest color in the Qwen series
QWEN_ABSOLUTE_COLORS[0] = darken_color(QWEN_ABSOLUTE_COLORS[0], amount=0.7)
QWEN_RELATIVE_COLORS[0] = darken_color(QWEN_RELATIVE_COLORS[0], amount=0.7)

# Uniform marker size
MARKER_SIZE = 50  # Adjust marker size to 50

# Define border color and line width parameters
BORDER_COLOR = 'gray'          # Border color for the plot
BORDER_LINEWIDTH = 2.0         # Border line width for the plot
PLOT_LINEWIDTH = 3.0           # Line width for performance curves


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
    path = f'res/{model}/{task}/results.json'
    if not os.path.exists(path):
        logging.warning(f"File does not exist: {path}")
        return None
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error in file {path}: {e}")
        return None

    scores = defaultdict(list)
    for item in data:
        scores[item['level']].append(item['score'])

    lengths = {len(v) for v in scores.values()}
    if len(lengths) > 1:
        logging.error(f"Inconsistent number of items across levels, model: {model}, task: {task}")
        return None

    return {level: sum(vals)/len(vals) for level, vals in scores.items()}

def configure_plot_style():
    """
    Configure global plotting style.
    """
    rcParams.update({
        # 'font.family': 'Arial',  # Change to 'Arial' or another installed font
        'figure.figsize': (4, 3),  # Set figure size to 4x3
        'axes.facecolor': 'white',
        'figure.facecolor': 'white',
        'axes.titlesize': 18,
        'axes.labelsize': 18,
        'legend.fontsize': 12,
        'xtick.labelsize': 14,  # Increase x-axis tick label size
        'ytick.labelsize': 14,  # Increase y-axis tick label size
    })
    plt.rcParams['axes.grid'] = False  # Ensure gridlines are not displayed globally
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

def draw_regular_model_graph(ax, model):
    """
    Draw performance curves for absolute and relative positions for regular models.

    Parameters:
    ax (matplotlib.axes.Axes): The axes object to draw on.
    model (str): Name of the model.
    """
    absolute_data = analyze_task_model('table_sql_absolute', model)
    relative_data = analyze_task_model('table_sql_relative', model)

    if not absolute_data and not relative_data:
        logging.warning(f"No available data to plot for model: {model}")
        ax.set_visible(False)
        return

    if absolute_data:
        levels = sorted(int(level.split()[-1]) for level in absolute_data)
        scores = [absolute_data[f'level {lvl}'] for lvl in levels]
        ax.plot(levels, scores, color=ABSOLUTE_COLOR, linewidth=PLOT_LINEWIDTH)
        ax.scatter(levels, scores, color=ABSOLUTE_COLOR, s=MARKER_SIZE, zorder=5)

    if relative_data:
        levels = sorted(int(level.split()[-1]) for level in relative_data)
        scores = [relative_data[f'level {lvl}'] for lvl in levels]
        ax.plot(levels, scores, color=RELATIVE_COLOR, linewidth=PLOT_LINEWIDTH)
        ax.scatter(levels, scores, color=RELATIVE_COLOR, s=MARKER_SIZE, zorder=5)

    ax.set_ylim(0, 1)
    ax.set_xlim(1, 16)  # Adjust x-axis lower limit to 1
    ax.set_xlabel("Feature Level")
    ax.set_ylabel("Recall Rate")
    ax.set_xticks([1, 4, 8, 12, 16])
    set_axes_style(ax)
    # Do not add legend

def draw_qwen_graph(ax, task, colors):
    """
    Draw performance curves for all Qwen series models under a specified task.

    Parameters:
    ax (matplotlib.axes.Axes): The axes object to draw on.
    task (str): The task name.
    colors (list): List of colors for the models.
    """
    for model, color in zip(QWEN_MODELS, colors):
        data = analyze_task_model(task, model)
        if not data:
            logging.warning(f"No available data to plot for model: {model} in task: {task}")
            continue
        levels = sorted(int(level.split()[-1]) for level in data)
        scores = [data[f'level {lvl}'] for lvl in levels]
        ax.plot(levels, scores, color=color, linewidth=PLOT_LINEWIDTH, label=model)
        ax.scatter(levels, scores, color=color, s=MARKER_SIZE, zorder=5)

    ax.set_ylim(0, 1)
    ax.set_xlim(1, 16)  # Adjust x-axis lower limit to 1
    ax.set_xlabel("Feature Level")
    ax.set_ylabel("Recall Rate")
    ax.set_xticks([1, 4, 8, 12, 16])
    set_axes_style(ax)
    # ax.legend()

def main():
    """
    Main function that configures plot styles, processes models, and generates plots.
    """
    # Configure plot style
    configure_plot_style()

    # Create save directory
    save_dir = 'res/fig'
    os.makedirs(save_dir, exist_ok=True)

    # Draw charts for regular models
    for model in REGULAR_MODELS:
        fig, ax = plt.subplots(figsize=(4, 3))  # 4x3 figure size
        draw_regular_model_graph(ax, model)

        # Construct save path and filename
        sanitized_model = sanitize_filename(model)
        filename = f"{sanitized_model}.png"
        save_path = os.path.join(save_dir, filename)

        # Adjust layout and save the figure, reducing edge margins
        plt.tight_layout(pad=0.5)
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()
        logging.info(f"Figure saved to: {save_path}")

    # Draw absolute position charts for Qwen series
    fig, ax = plt.subplots(figsize=(4, 3))  # 4x3 figure size
    draw_qwen_graph(ax, 'table_sql_absolute', QWEN_ABSOLUTE_COLORS)

    # Construct save path and filename
    filename = f"Qwen_Series_absolute.png"
    save_path = os.path.join(save_dir, filename)

    # Adjust layout and save the figure, reducing edge margins
    plt.tight_layout(pad=0.5)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    logging.info(f"Figure saved to: {save_path}")

    # Draw relative position charts for Qwen series
    fig, ax = plt.subplots(figsize=(4, 3))  # 4x3 figure size
    draw_qwen_graph(ax, 'table_sql_relative', QWEN_RELATIVE_COLORS)

    # Construct save path and filename
    filename = f"Qwen_Series_relative.png"
    save_path = os.path.join(save_dir, filename)

    # Adjust layout and save the figure, reducing edge margins
    plt.tight_layout(pad=0.5)
    plt.savefig(save_path, bbox_inches='tight', dpi=600)  # Increase resolution
    plt.close()
    logging.info(f"Figure saved to: {save_path}")

if __name__ == '__main__':
    main()
