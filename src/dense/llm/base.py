"""
Module: BaseNLPModel

This is a base class for NLP models. It contains an __init__ method, two methods
get_model and get_tokenizer that are intended to be overridden by subclasses, and
an inference method.
"""

class BaseNLPModel:
    def __init__(self, device, batch_size, temperature, max_input_length,
                 max_new_tokens, num_beams, top_k, top_p):
        """
        Initialize the BaseNLPModel class.

        Parameters:
            device (str or torch.device): The device to run the model on.
            batch_size (int): The batch size for inference.
            temperature (float): The temperature for sampling.
            max_input_length (int): The maximum input length.
            max_new_tokens (int): The maximum number of new tokens to generate.
            num_beams (int): The number of beams for beam search.
            top_k (int): The top k samples to consider during sampling.
            top_p (float): The top p probability to consider during sampling.
        """
        self.device = device
        self.batch_size = batch_size
        self.temperature = temperature
        self.max_input_length = max_input_length
        self.max_new_tokens = max_new_tokens
        self.num_beams = num_beams
        self.top_k = top_k
        self.top_p = top_p

    def get_model(self):
        """
        Get the model. This method is intended to be overridden by subclasses.

        Returns:
            torch.nn.Module: The model.
        """
        pass

    def get_tokenizer(self):
        """
        Get the tokenizer. This method is intended to be overridden by subclasses.

        Returns:
            transformers.PreTrainedTokenizer: The tokenizer.
        """
        pass

    def inference(self, inputs):
        """
        Perform inference on a list of inputs.

        Parameters:
            inputs (List[Dict]): A list of dictionaries containing input data.

        Returns:
            List[str]: A list of strings containing the model's outputs.
        """
        pass
