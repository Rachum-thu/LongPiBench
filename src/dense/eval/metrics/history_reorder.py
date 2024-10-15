import re
from .base import NLGMetric
from typing import List

def remove_letters_and_strip(input_str: str) -> str:
    """
    Remove all non-numeric, non-comma, and non-space characters from the input string and strip leading and trailing whitespace.

    Parameters:
    input_str (str): The input string to be cleaned.

    Returns:
    str: The cleaned string with only numbers, commas, and spaces.
    """
    # Use regex to remove all characters except digits, commas, and spaces
    cleaned_str = re.sub(r'[^0-9, ]', '', input_str)
    
    # Strip leading and trailing whitespace
    cleaned_str = cleaned_str.strip()
    
    # Additional step: replace multiple spaces with a single space
    cleaned_str = re.sub(r'\s+', ' ', cleaned_str)
    
    return cleaned_str


class HistoryReorderMetric(NLGMetric):

    def _evaluate_pair(self, llm_response: str, labels: List[str]) -> float:
        """
        Calculate the History Reorder metric for a single pair of generated text and a list of labels.

        Args:
            llm_response (str): The generated text to evaluate.
            labels (List[str]): A list of reference texts. In this task, the list contains a single string with a comma-separated list of indices of the events in the correct order.

        Returns:
            float: The History Reorder metric value between 0.0 and 1.0, representing the proportion of correctly ordered events.
        """
        llm_response = remove_letters_and_strip(llm_response)
        ground_truth_order_list = labels[0].split(", ")
        try:
            llm_response_order_list = llm_response.split(", ")
            # Every part split by ", " should be a digit
            for part in llm_response_order_list:
                if not part.isdigit():
                    raise ValueError
        except ValueError:
            # If the response is not in the expected format, return 0.0
            return 0.0

        if len(ground_truth_order_list) != len(llm_response_order_list):
            # If the number of events in the ground truth and the generated response are different, return 0.0
            return 0.0

        num_events_to_reorder = len(ground_truth_order_list)
        num_correct_indices = 0
        for i in range(num_events_to_reorder):
            if ground_truth_order_list[i] == llm_response_order_list[i]:
                num_correct_indices += 1

        return float(num_correct_indices / num_events_to_reorder)


if __name__ == "__main__":
    # Test the HistoryReorderMetric with provided cases
    llm_responses = [
        "The answer is: 0, 1",
        "1, 0, 2, 3, 4, 5",
        "9, 3, 19, 25, 14, 11, 2, 22, 17, 1, 28, 0",
    ]

    labels = [["0, 1"], ["1, 0, 4, 5, 2, 3"], ["7, 9, 3, 2, 8, 5, 4, 10, 6, 1, 0"]]

    metric = HistoryReorderMetric()
    results = metric.evaluate(llm_responses, labels)

    print(results) # Expected output: [0.0, 0.3333333333333333, 0.0]
