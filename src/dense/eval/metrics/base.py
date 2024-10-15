from abc import ABC, abstractmethod
from typing import List, Dict

class NLGMetric(ABC):
    """
    Abstract base class for NLG metrics.

    This class defines the interface for all NLG metrics.
    Subclasses should implement the _evaluate_pair method to compute the metric.

    Methods:
    evaluate(self, llm_responses: List[str], labels: List[List[str]]) -> List[List[float]]:
        Calculate the metric for each generated text and its labels.

    _evaluate_pair(self, llm_response: str, labels: List[str]) -> List[float]:
        Calculate the metric for a single pair of generated text and a list of labels.
    """

    def evaluate(self, llm_responses: List[str], labels: List[List[str]], *args, **kwargs) -> List[float]:
        """
        Calculate the metric for each generated text and its labels.

        Parameters:
        llm_responses (List[str]): A list of generated texts.
        labels (List[List[str]]): A list of lists, where each sublist contains reference texts for each generated text.

        Returns:
        List[List[float]]: A list of lists of calculated metric values between 0.0 and 1.0.
        """
        results = []
        for response, label_list in zip(llm_responses, labels):
            scores = self._evaluate_pair(response, label_list, *args, **kwargs)
            results.append(scores)
        return results

    @abstractmethod
    def _evaluate_pair(self, llm_response: str, labels: List[str], *args, **kwargs) -> float:
        """
        Calculate the metric for a single pair of generated text and a list of labels.

        Parameters:
        llm_response (str): The generated text to evaluate.
        labels (List[str]): A list of reference texts.

        Returns:
        List[float]: A list of calculated metric values between 0.0 and 1.0.
        """
        pass
