from utils import listmap
from math import ceil


class RegexPart:
    r"""Class for storing information about regex building blocks capturing one specific character in searched string"""
    def __init__(self, char, options, percentage):
        r"""
        RegexPart initializer

        Arguments:

        char (str): regex part capturing specific character. Examples: [abc], \d, a
        options (set): set of characters included in examples that ``char`` captures. Can include None. Examples: {a, b, c}, {1, 2, 3, 4, 5. 6}, {a}
        percentage (float): percentage stored as a fraction ``len(set(options))/len(options)``. Options here is a list of possible characters *with* duplicates
        """
        self.char = char
        self.options = options
        self.percentage = percentage

class Data_Entry:
    r"""
    Class storing string and its part of interest in convenient form. Provides useful methods for viewing the entry.
    """
    def __init__(self, string, selection):
        r"""
        Data_Entry initializer. 

        Arguments:

        string (str): whole string containing part of interest to be extracted
        selection (tuple): tuple containing ``start`` and ``end`` (exclusive) indices of part of interest

        Example of inputs: 

        string = "My id is: 21"
        selection = (10,12)

        >> string[selection[0]:selection[1]]
        21

        """
        
        self.string = string
        self.selection = selection
        self.search_fragment = string[selection[0]:selection[1]] # actual searched string
        self.left_nbh = string[:selection[0]] # left neighbourhood of selection part
        self.right_nbh = string[selection[1]:] # right neighbourhood of selection part

    def __str__(self):
        return f"{self.string} with selection {self.selection} which is {self.search_fragment}\nLeft neighbourhood: {self.left_nbh}\nRight neighbourhood: {self.right_nbh}"

    def initialize_generators(self, left_reversed = True):
        r"""
        Initilizes three generators iterating through left neighbourhood of part of interest, through it itself and through right neighbourhood of it

        Arguments:

        left_reversed (bool, optional):  if set to ``True`` then left neighbourhood is iterated in reverse. (default: ``True``)
        """
        if left_reversed:
            self.left_gen = iter(self.left_nbh[::-1])
        else:
            self.left_gen = iter(self.left_nbh)
        
        self.mid_gen = iter(self.search_fragment)
        self.right_gen = iter(self.right_nbh)

    def next_left(self):
        r"""Returns next character of left neighbourhood iterator or None if its not present"""

        try:
            return next(self.left_gen)
        except:
            return None
    
    def next_mid(self):
        r"""Returns next character of left neighbourhood iterator or None if its not present"""
        try:
            return next(self.mid_gen)
        except:
            return None

    def next_right(self):
        r"""Returns next character of right neighbourhood iterator or None if its not present"""
        try:
            return next(self.right_gen)
        except:
            return None

class RegexGenerator:
    r"""
    Class providing regex generation capabilities. It is based on grid iterative algorithm.
    """

    def __init__(self):
        self.data_entries = []
        self.spans_list = []
        self.left_regex_builder = []
        self.mid_regex_builder = []
        self.right_regex_builder = []
        self.left_regex = ""
        self.mid_regex = ""
        self.right_regex = ""
        self.train_part_end_index = None # This will be the index to split ``data_entries`` to train and test sets if its sufficiently long

    def parse_data(self, data, append = False, inclusive_end = True, alternative_keys = []):
        r"""
        This method parses data provided in list-of-dictionaries fashion to list of Data_Entry objects stored inside ``RegexGenerator`` object.


        Arguments:

        data (list): list of dictionary objects having fields ``string`` and ``selections`` 
        append (bool, optional): if set to ``True`` data parsed is appended to currently stored. (default: ``False``)
        inclusive_end (bool, optional): if set to ``True`` then ``end`` index of selections will be treated inclusively in contrary to python's standard indexing. (default: ``True``)
        alternative_keys (list, optional): list of two strings that will replace original ``string`` and ``selection`` keys.

        Example of input arguments:

        >>> data = [{

            "string" : "I want to extract this id: 721 and this name: Damian",
            "selections" : [(27,29),(46,51)]

        }]

        If ``inclusive_end`` is set to ``False`` then ``selections`` in ``data`` could be like:

        >>> ...
        "selections" : [(27,30),(46,52)]
        ...

        """
        if not append:
            self.data_entries = []

        if alternative_keys:
            if len(alternative_keys) != 2:
                raise Exception('alternative_keys has to be of length 2')
            elif alternative_keys[0] == alternative_keys[1]:
                raise Exception('keys have to be different')

        string_key = 'string' if not alternative_keys else alternative_keys[0]
        selection_key = 'selections' if not alternative_keys else alternative_keys[1]
        offset = 1 if inclusive_end else 0 # offset for slicing if selections in dict are provided inclusively

        # Iterates over dicts with possibly multiple selections stored for each string
        for entry in data:
            d_entries = []
            # Creates ``Data_Entry`` for each selection (`span`) in string
            for span in entry[selection_key]:
                d_entries.append(Data_Entry(entry[string_key], (span[0],span[1]+offset)))
            
            self.data_entries.extend(d_entries)


        if len(self.data_entries) >= 5:

            self.train_part_end_index = int(ceil(len(self.data_entries) * 0.8))


    def compile_from_builders(self, ignore_mid = True, left_reversed = True):
        r"""
        Updates string regex parts using corresponding builders

        Arguments:

        ignore_mid (bool, optional): if set to ``True`` then ``mid_regex`` will not be rebuilt. (default: ``True``)
        left_reversed (bool, optional):  if set to ``True`` then ``left_regex_builder`` is reversed before compiling into string regex. (default: ``True``)
        """
        
        # used if left neighbourhood was iterated in reverse and thus regex was created from its end
        if left_reversed:
            self.left_regex = ''.join([part.char for part in reversed(self.left_regex_builder)]) 
        else:
            self.left_regex = ''.join([part.char for part in self.left_regex_builder])
        if not ignore_mid:
            self.mid_regex = ''.join([part.char for part in self.mid_regex_builder])
        self.left_regex = ''.join([part.char for part in self.right_regex_builder])


    def save_spans_data(self):
        r"""Creates ``spans_list`` list inside object that captures all spans from ``data_entries``"""

        self.spans_list = [entry['selection'] for entry in self.data_entries]


    def evaluate(self):
        r"""Evaluates current regexp for all data including test and return True or False whether all matches are correct or not"""
        pass

            

    def evolve(self, ignore_mid = True, mid = ""):

        if ignore_mid:
            if mid:
                self.mid_regex = mid
            else:
                self.mid_regex = ".*?"

        pass

