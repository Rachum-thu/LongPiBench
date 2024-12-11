from .base import NLGMetric


class EquationSolutionMetric(NLGMetric):

    def _evaluate_pair(self, llm_response: str, label: list[str]) -> float:

        assert len(label) == 1, "The label should contain a single value."
        pred_value = self._extract_predicted_value(llm_response)
        label_value = int(label[0])
        
        return 1.0 if pred_value == label_value else 0.0

    def _extract_predicted_value(self, response: str) -> int:
        try:
            prefix = "the answer is"
            start = response.lower().find(prefix) + len(prefix)
            value_str = response[start:].strip()
            
            # adjust to the condition of '='
            if '=' in value_str:
                value_str = value_str.split('=')[1].strip()
            
            # remove all the format characters like '/'. '\', '(' ...
            format_characters = ['/', '\\', '(', ')', '[', ']', '{', '}', ' ']
            for char in format_characters:
                value_str = value_str.replace(char, '')

            if value_str.endswith('.'):
                value_str = value_str[:-1]  # Remove the trailing period

            pred_value = int(float(value_str))  # Convert the substring to int
        except ValueError:
            # Handle the case where conversion to int fails
            pred_value = -100

        return pred_value


if __name__ == "__main__":
    # Test the CodeRunMetric with provided cases
    llm_responses = ["To find the value of \\( x_{711} \\), we need to identify the equation that directly involves \\( x_{711} \\) and solve it. Let's look through the list of equations to find such an equation.\n\nUpon examining the list, we find:\n\nEquation 493: \\(-5 x_{711} - 3 x_{674} = -1\\)\n\nTo solve for \\( x_{711} \\), we need to know the value of \\( x_{674} \\). Let's find the equation involving \\( x_{674} \\).\n\nEquation 447: \\(3 x_{674} = -9\\)\n\nSolving for \\( x_{674} \\):\n\n\\[ x_{674} = \\frac{-9}{3} = -3 \\]\n\nNow that we have \\( x_{674} = -3 \\), we can substitute this value back into Equation 493:\n\n\\[\n-5 x_{711} - 3(-3) = -1\n\\]\n\nSimplify the equation:\n\n\\[\n-5 x_{711} + 9 = -1\n\\]\n\nSubtract 9 from both sides:\n\n\\[\n-5 x_{711} = -1 - 9\n\\]\n\n\\[\n-5 x_{711} = -10\n\\]\n\nDivide both sides by -5:\n\n\\[\nx_{711} = \\frac{-10}{-5} = 2\n\\]\n\nTherefore, the answer is \\( x_{711} = 2 \\).",
                     "To find the value of \\( x_{711} \\), we need to identify the equation that directly involves \\( x_{711} \\) and solve it. Let's look through the list of equations to find such an equation.\n\nUpon examining the list, we find:\n\nEquation 493: \\(-5 x_{711} - 3 x_{674} = -1\\)\n\nTo solve for \\( x_{711} \\), we need to know the value of \\( x_{674} \\). Let's find the equation involving \\( x_{674} \\).\n\nEquation 447: \\(3 x_{674} = -9\\)\n\nSolving for \\( x_{674} \\):\n\n\\[ x_{674} = \\frac{-9}{3} = -3 \\]\n\nNow that we have \\( x_{674} = -3 \\), we can substitute this value back into Equation 493:\n\n\\[\n-5 x_{711} - 3(-3) = -1\n\\]\n\nSimplify the equation:\n\n\\[\n-5 x_{711} + 9 = -1\n\\]\n\nSubtract 9 from both sides:\n\n\\[\n-5 x_{711} = -1 - 9\n\\]\n\n\\[\n-5 x_{711} = -10\n\\]\n\nDivide both sides by -5:\n\n\\[\nx_{711} = \\frac{-10}{-5} = 2\n\\]\n\nTherefore, the answer is \\( x_{711} = 2 \\).",
                     "To find the value of \\( x_{711} \\), we need to identify the equation that directly involves \\( x_{711} \\) and solve it. Let's look through the list of equations to find such an equation.\n\nUpon examining the list, we find:\n\nEquation 493: \\(-5 x_{711} - 3 x_{674} = -1\\)\n\nTo solve for \\( x_{711} \\), we need to know the value of \\( x_{674} \\). Let's find the equation involving \\( x_{674} \\).\n\nEquation 447: \\(3 x_{674} = -9\\)\n\nSolving for \\( x_{674} \\):\n\n\\[ x_{674} = \\frac{-9}{3} = -3 \\]\n\nNow that we have \\( x_{674} = -3 \\), we can substitute this value back into Equation 493:\n\n\\[\n-5 x_{711} - 3(-3) = -1\n\\]\n\nSimplify the equation:\n\n\\[\n-5 x_{711} + 9 = -1\n\\]\n\nSubtract 9 from both sides:\n\n\\[\n-5 x_{711} = -1 - 9\n\\]\n\n\\[\n-5 x_{711} = -10\n\\]\n\nDivide both sides by -5:\n\n\\[\nx_{711} = \\frac{-10}{-5} = 2\n\\]\n\nTherefore, the answer is \\( x_{711} = what \\)."]

    labels = [[2], [3], [4]]

    metric = EquationSolutionMetric()
    results = metric.evaluate(llm_responses, labels)

    print(results)  # Expected output: [1.0, 0.0, 0.0]