import ast
from .base import NLGMetric
from typing import List

class SQLMetric(NLGMetric):
    """
    RetrievalMetric class for evaluating the correctness of code-generated responses.

    This class parses the predicted value from the generated response and compares it with the label.
    """

    def _evaluate_pair(self, llm_response: str, label: List[str]) -> float:
        """
        Calculate the metric for a single pair of generated text and label.

        Parameters:
        llm_response (str): The generated text to evaluate.
        labels (List[str]): A list of reference texts.

        Returns:
        float: The calculated metric value between 0.0 and 1.0.
        """
        label_recall_num = 0
        for single_label in label:
            if single_label in llm_response:
                label_recall_num += 1
        
        total_score = label_recall_num / len(label)
        return total_score


if __name__ == "__main__":
    
    instance = {
        "uuid": "d53b1252-37f1-4b39-95b2-9be066b6497d",
        "answers": [
            "| China | Zhao Wei | 1982 | September | A |",
            "| China | Zhao Wei | 1970 | September | AB |",
            "| China | Zhao Wei | 2014 | December | A |",
            "| China | Wang Wei | 1961 | May | O |",
            "| China | He Wei | 1970 | October | O |",
            "| China | Huang Wei | 1991 | July | B |",
            "| China | Zhou Wei | 1993 | March | AB |",
            "| China | Wang Fang | 2014 | August | A |",
            "| China | Zhou Wei | 1989 | April | O |",
            "| China | Zhao Wei | 2005 | October | B |"
        ],
        "answer_locations": "b",
        "range_level": 1,
        "location": [
            5190,
            5191,
            5192,
            5193,
            5194,
            5195,
            5196,
            5197,
            5198,
            5199
        ],
        "token_length": 65500,
        "density": 0.0019230769230769162,
        "default_prompt": {
            "system_prompt": "You are a helpful assistant. You are given a table of entries with the following columns: Country, Name, Birth Year, Birth Month, Blood Type. ",
            "user_message": "Here is the table:\n\n{context}\n\nYour task is to find all the entry with the following Country:\n\n{query}\n\nYou should return all the entries that match the query as a python list. For example, ['| China | Hong Liang | 1991 | August | A |', ...]. You should not generate anything else."
        }
    }
    responses = ["Here are the entries from the table that match the query for the country 'China':\n\n['| China | Zhao Wei | 1982 | September | A |', '| China | Wang Fang | 2011 | July | A |', '| China | Hu Wei | 2005 | May | A |', '| China | Yang Wei | 1991 | April | AB |', '| China | Xu Wei | 1997 | March | O |', '| China | Sun Wei | 1963 | October | A |', '| China | Wang Fang | 1971 | August | O |', '| China | Li Wei | 1983 | June | O |', '| China | Wu Wei | 1952 | May | AB |', '| China | Zhou Wei | 1969 | August | O |']", "Here are the entries from the table that match the query for the country 'China':\n\n['| China | Li Na | 2010 | February | O |', '| China | Zhou Wei | 1989 | June | O |', '| China | Ma Wei | 1972 | January | O |', '| China | Gao Wei | 1996 | February | B |', '| China | Zhao Wei | 2003 | July | AB |', '| China | Sun Wei | 2018 | June | AB |', '| China | He Wei | 2005 | March | AB |', '| China | Zhou Wei | 1951 | April | A |', '| China | Chen Wei | 1994 | July | AB |', '| China | He Wei | 2006 | January | AB |']", "Here are the entries from the table that match the query for the country 'China':\n\n['| China | Xu Wei | 2014 | July | A |', '| China | Wang Wei | 1950 | February | B |', '| China | Hu Wei | 1957 | January | A |', '| China | Xu Wei | 1969 | January | O |', '| China | Chen Wei | 2016 | February | A |', '| China | Yang Wei | 1974 | January | AB |', '| China | Yang Wei | 1999 | June | AB |', '| China | Li Wei | 1990 | March | AB |', '| China | Xu Wei | 2008 | August | A |', '| China | Gao Wei | 1999 | November | A |']", "['| China | Li Wei | 2015 | November | B |', '| China | Guo Wei | 2005 | March | A |', '| China | He Wei | 1976 | January | AB |', '| China | Zhou Wei | 1968 | December | B |', '| China | Liu Wei | 1979 | December | A |', '| China | Xu Wei | 2000 | June | O |', '| China | Wang Wei | 2011 | July | A |']", "Here are the entries from the table that match the Country query for China:\n\n['| China | Zhao Wei | 2012 | November | A |', '| China | Wu Wei | 1990 | August | B |', '| China | He Wei | 1950 | December | B |', '| China | Wang Fang | 2008 | December | A |', '| China | Liu Wei | 2005 | September | A |', '| China | Li Wei | 2014 | November | AB |']", "Here are the entries from the table that match the query for the country 'China':\n\n['| China | He Wei | 1981 | January | A |', '| China | Hu Wei | 1958 | June | O |', '| China | Liu Wei | 1953 | May | AB |', '| China | Ma Wei | 1988 | December | B |', '| China | Wang Wei | 1997 | March | B |', '| China | Zhao Wei | 1968 | February | B |', '| China | Zhang Wei | 1977 | April | A |']", "Here are the entries from the table that match the query for the country 'China':\n\n['| China | Zhu Wei | 1961 | May | B |', '| China | Yang Wei | 2009 | September | AB |', '| China | Li Na | 1969 | February | O |', '| China | Wu Wei | 1965 | January | A |', '| China | Ma Wei | 1979 | September | A |', '| China | Hu Wei | 1957 | October | O |', '| China | Zhang Wei | 1996 | June | AB |']", "Here are the entries from the table that match the query for the country 'China':\n\n['| China | Sun Wei | 1963 | December | B |', '| China | Huang Wei | 2001 | July | AB |', '| China | Huang Wei | 2004 | April | A |', '| China | Wang Fang | 1983 | July | A |', '| China | Zhou Wei | 1985 | August | AB |', '| China | Ma Wei | 2017 | November | B |']", "Here are the entries from the table that match the query for the country 'China':\n\n['| China | Huang Wei | 1953 | June | O |', '| China | Li Wei | 2006 | August | O |', '| China | Wu Wei | 1954 | February | AB |', '| China | Yang Wei | 1983 | September | A |']", "Here are the entries from the table that match the query for the country 'China':\n\n['| China | Ma Wei | 1966 | March | O |']", "Here are the entries from the table that match the query for the country 'China':\n\n['| China | Sun Wei | 1982 | April | O |', '| China | Zhu Wei | 1954 | June | B |', '| China | Chen Wei | 2016 | March | O |', '| China | Wang Wei | 1997 | September | B |', '| China | Xu Wei | 2014 | July | AB |']", "Here are the entries from the table that match the query for the country 'China':\n\n['| China | Sun Wei | 2006 | October | A |', '| China | Guo Wei | 1980 | March | AB |', '| China | Zhao Wei | 2002 | July | B |', '| China | Li Wei | 1954 | August | B |', '| China | Xu Wei | 1971 | July | O |']"]
    metric = SQLMetric()
    metric._evaluate_pair(responses[0], instance['answers'])
    