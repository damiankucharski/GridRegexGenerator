from utils import listmap
from math import ceil
import string
import re

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
        r"""Returns next character of left neighbourhood iterator or empty string if its not present"""

        try:
            return next(self.left_gen)
        except:
            return ''
    
    def next_mid(self):
        r"""Returns next character of left neighbourhood iterator or empty string if its not present"""
        try:
            return next(self.mid_gen)
        except:
            return ''

    def next_right(self):
        r"""Returns next character of right neighbourhood iterator or empty string if its not present"""
        try:
            return next(self.right_gen)
        except:
            return ''

class RegexGenerator:
    r"""
    Class providing regex generation capabilities. It is based on grid iterative algorithm.
    """

    def __init__(self):
        self.data_entries = []
        self.spans_list = []
        self.all_searched_fragments = []
        self.left_regex_builder = []
        self.mid_regex_builder = []
        self.right_regex_builder = []
        self.left_regex = ""
        self.mid_regex = ""
        self.right_regex = ""
        self.train_part_end_index = None # This will be the index to split ``data_entries`` to train and test sets if its sufficiently long

        self.set_letters = set(string.ascii_letters)
        self.set_digits = set(string.digits)
        self.set_punctuation = set(string.punctuation)
        self.set_whitespace = set(string.whitespace)

    def parse_data(self, data, start_end_keys = True, append = False, inclusive_end = True, alternative_keys = []):
        r"""
        This method parses data provided in list-of-dictionaries fashion to list of Data_Entry objects stored inside ``RegexGenerator`` object.


        Arguments:

        data (list): list of dictionary objects having fields ``string`` and ``selections`` 
        start_end_keys (bool, optional): informs if spans in dict format are part of dictionary with keys ['start', 'end'] or just in tuple (start, end) form. Defaults to True
        append (bool, optional): if set to ``True`` data parsed is appended to currently stored. (default: ``False``)
        inclusive_end (bool, optional): if set to ``True`` then ``end`` index of selections will be treated inclusively in contrary to python's standard indexing. (default: ``True``)
        alternative_keys (list, optional): list of two strings that will replace original ``string`` and ``selection`` keys.

        Example of input arguments:

        >>> data = [{

            "string" : "I want to extract this id: 721 and this id: 123",
            "selections" : [(27,29),(44,46)]

        }]

        If ``inclusive_end`` is set to ``False`` then ``selections`` in ``data`` could be like:

        >>> ...
        "selections" : [(27,30),(44,47)]
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
                if start_end_keys:
                    d_entries.append(Data_Entry(entry[string_key], (span['start'],span['end']+offset)))
                else:
                    d_entries.append(Data_Entry(entry[string_key], (span[0],span[1]+offset)))
                d_entries[-1].initialize_generators()

            self.data_entries.extend(d_entries)


        if len(self.data_entries) >= 5:

            self.train_part_end_index = int(ceil(len(self.data_entries) * 0.8))

        self.save_spans_data()
        self.save_selections_data()

    def compile_from_builders(self, ignore_mid = True, left_reversed = True, len_left = None, len_mid = None, len_right = None):
        r"""
        Updates string regex parts using corresponding builders

        Arguments:

        ignore_mid (bool, optional): if set to ``True`` then ``mid_regex`` will not be rebuilt. (default: ``True``)
        left_reversed (bool, optional):  if set to ``True`` then ``left_regex_builder`` is reversed before compiling into string regex. (default: ``True``)
        len_left (int, optional): if set - only ``len_left`` blocks will be compiled. (default: ``None``)
        len_mid (int, optional): if set - only ``len_mid`` blocks will be compiled. (default: ``None``)
        len_right (int, optional): if set - only ``len_right`` blocks will be compiled. (default: ``None``)

        Returns:

        (str): string regex
        """
        
        # used if left neighbourhood was iterated in reverse and thus regex was created from its end
        if left_reversed:
            self.left_regex = ''.join([part.char for part in list(reversed(self.left_regex_builder)])[:len_left]) 
        else:
            self.left_regex = ''.join([part.char for part in self.left_regex_builder][:len_left])
        if not ignore_mid:
            self.mid_regex = ''.join([part.char for part in self.mid_regex_builder][:len_mid])
        self.right_regex = ''.join([part.char for part in self.right_regex_builder][:len_right])
        
        self.left_regex_match = []
        self.mid_regex_match = []
        self.right_regex_match = []
        for entry in self.data_entries:
            self.left_regex_match.extend(re.findall(self.left_regex, entry.string))
            self.mid_regex_match.extend(re.findall(self.mid_regex, entry.string))
            self.right_regex_match.extend(re.findall(self.right_regex, entry.string))
        
        return f'{self.left_regex}({self.mid_regex}){self.right_regex}'

    def save_spans_data(self):
        r"""Creates ``spans_list`` list inside object that captures all spans from ``data_entries``"""

        self.spans_list = [entry.selection for entry in self.data_entries]
    
    def save_selections_data(self):
        self.all_searched_fragments = [entry.search_fragment for entry in self.data_entries]
        

    def generate_next_part(self, left = True, mid = False, right = True):
        r"""
        Generates next RegexParts for specified parts of regex

        Arguments:

        left (bool, optional): if set to ``True``, ``left_gen`` of all ``data_entries`` will be used.
        mid (bool, optional): if set to ``True``, ``mid_gen`` of all ``data_entries`` will be used.
        right (bool, optional): if set to ``True``, ``right_gen`` of all ``data_entries`` will be used.

        Returns

        (tuple): (left_block, mid_block, right_block) - ``RegexPart`` objects.
        

        """

        def find_correct_block_char(options):
            r"""
            Generates char element of ``RegexPart``.

            Arguments:

            options(list): list formed from ``data_entries`` iterators

            Returns:

            (RegexPart): RegexPart object representing fragment matching all ``options``. None if no option provided.

            """


            # 4 kroki budowania, najpierw testujemy same znaki, jak matchuje tez na testowym to git, jak nie to ogolne, jak nie to znaki {0,1}, jak nie to ogolne {0,1}
            if any(options):
                
                # it has to be chacked whether one of generators didn't finish, in this case this character should be optional
                if '' in options:
                    optional = True
                else:
                    optional = False

                if self.train_part_end_index:
                    options_set_train = set(options[:self.train_part_end_index])
                else:
                    options_set_train = set(options)

                percentage = len(options_set_train)/len(options)
                options_string = ''.join(options) # test set is included

                # attempt 1 -> only letters present in train set
                if len(options_set_train) < 3:
                    if len(options_set_train) > 1:
                        char_letters = f"[{''.join(options_set_train)}]".replace('-','\\-').replace('(','\\(').replace(')','\\)').replace('{','\\{').replace('[','\\[')
                    else:
                        char_letters = list(options_set_train)[0]
                
                    if optional:
                        char_letters += '{0,1}'
                        if len(re.findall(char_letters, options_string)) -1 == len(options_string): # everything found
                            return RegexPart(char_letters, options_set_train, percentage)

                    else:
                        if len(re.findall(char_letters, options_string)) == len(options_string): # everything found
                            return RegexPart(char_letters, options_set_train, percentage)

                # attempt 2 -> general regex characters
                char_general = ''
                counter = 0

                if self.set_letters.intersection(options_set_train):
                    counter += 1
                    char_general += r'\w' # captures also digits
                elif self.set_digits.intersection(options_set_train):
                    counter += 1
                    char_general += r'\d' # only digits if `word characters` not present
                if self.set_whitespace.intersection(options_set_train):
                    counter += 1
                    char_general += r'\s'
                if self.set_punctuation.intersection(options_set_train):
                    counter += 1
                    difference = self.set_punctuation.intersection(options_set_train)
                    char_general += ''.join(difference).replace('-','\\-').replace('(','\\(').replace(')','\\)').replace('{','\\{').replace('[','\\[')

                if counter > 1:
                    char_general = f'[{char_general}]'
                
                try:
                    if optional:
                        char_general += "{0,1}"
                        if len(re.findall(char_general, options_string)) -1 == len(options_string): # everything found
                            return RegexPart(char_general, options_set_train, percentage)
                    else:
                        if len(re.findall(char_general, options_string)) == len(options_string): # everything found
                            return RegexPart(char_general, options_set_train, percentage)
                except Exception as ex:
                    print(ex)
                    input(char_general)


                # attempt 3 -> any character or none
                if optional:
                    char_any = '.?'
                    if len(re.findall(char_any, options_string)) -1 == len(options_string): # everything found
                        return RegexPart(char_any, options_set_train, percentage)
                else:
                    char_any = '.'
                    if len(re.findall(char_any, options_string)) == len(options_string): # everything found
                        return RegexPart(char_any, options_set_train, percentage)


                raise Exception(f'Something went very wrong for set: {str(options)}')

            else:
                return None
            
        
        generated_parts = []

        left_list = []
        mid_list = []
        right_list = []

        for data_entry in self.data_entries:
            if left:
                left_list.append(data_entry.next_left())
            if mid:
                mid_list.append(data_entry.next_mid())
            if right:
                right_list.append(data_entry.next_right())


        if left:
            left_block = find_correct_block_char(left_list)     
        else:
            left_block = None
        if mid:
            mid_block = find_correct_block_char(mid_list)
        else:
            mid_block = None
        if right:
            right_block = find_correct_block_char(right_list)
        else:
            right_block = None

        return left_block, mid_block, right_block


    def fix_escaped(self, string):

        escaped = ['[','(','{','-','"','|','^']
        for char in escaped:
            string = string.replace(char, f'\\{char}')
        return string

    def prepare_mid(self, strings, quantifier = '+?', with_brackets = True):

        letters_set = set(string.ascii_letters)
        digits_set = set(string.digits)
        whitespace_set = set(string.whitespace)
        punct_set = set(string.punctuation)
        string_set = set(''.join(strings))
        options = []
        if len(letters_set.intersection(string_set)) > 0:
            options.append('\w')
        elif len(digits_set.intersection(string_set)) > 0:
            options.append('\d')
        if len(whitespace_set.intersection(string_set)) > 0:
            options.extend(string_set.intersection(whitespace_set))
        if len(punct_set.intersection(string_set)) > 0:
            options.extend(string_set.intersection(punct_set))
    
        regexp = f"[{self.fix_escaped(''.join(options))}]{quantifier}"
        if with_brackets:
            regexp = f"({regexp})"
        return regexp

    def evaluate(self, ignore_mid = True):
        r"""
        Evaluates current regexp for all data including test and return True or False whether all matches are correct or not
        
        Arguments:

        ignore_mid (bool, optional): Whether to ignore building mid regex. (default: True)
        """
        regex = self.compile_from_builders(ignore_mid=ignore_mid)
        for index, entry in enumerate(self.data_entries):

            searched = [match for match in re.finditer(regex, entry.string)]
            spans_found = [] 

            for s in searched:
                try:
                    spans_found.append(s.span(1))
                except:
                    return False ## group 1 should always exist and match at least empty string

            if (entry.selection in spans_found) and (len(set(spans_found).difference(set(self.spans_list))) == 0):
                continue
            else:
                return False
        return True

    def check_mid_reg_correct(self, ignore_mid = False):
        
        self.compile_from_builders(ignore_mid=ignore_mid)
        
        for entry in self.data_entries:
            match = re.match(self.mid_regex, entry.search_fragment)
            match_full = re.search(self.mid_regex, entry.search_fragment)
            if match.group(0) != entry.search_fragment:
                return False

        return True
        

    def evolve(self, ignore_mid = True, mid = "", max_iter = -1, min_iter = -1, check_mid = True, mid_classic = True):
        r"""
        Creates and returns regular expression that matches provided samples. Part of interest is contained in 1st group.

        Arguments:

        ignore_mid (bool, optional): Whether to ignore building mid regex. (default: True)
        mid (str, optional): If ignore mid is set to ``True`` then you can set that value to be exact match for part of interest. 

        Returns:

        (str): Regex string

        """

        if len(self.data_entries) == 0:
            raise Exception("Provide data first. Use parse_data method first.")


        if ignore_mid:
            if mid:
                self.mid_regex = mid
            else:
                self.mid_regex = ".*?"

        do_left, do_mid, do_right = True, not ignore_mid, True

        # first only mid
        while do_mid:
            if mid_classic:
                left_block, mid_block, right_block = self.generate_next_part(False, do_mid, False)
                if mid_block:
                    self.mid_regex_builder.append(mid_block)
                else:
                    do_mid = False
            else:
                self.mid_regex = self.prepare_mid(self.all_searched_fragments, with_brackets=False)
                do_mid = False
                ignore_mid = True


        if check_mid:
            if not self.check_mid_reg_correct():
                raise Exception("Bad exception! Mid regex was not found")

            if self.evaluate(ignore_mid=ignore_mid):
                return self.compile_from_builders(ignore_mid)   

        # then only neighbourhood
        if max_iter or min_iter:
            n_iters = 0
        while (do_left or do_right):

            if max_iter:
                if n_iters == max_iter:
                    break
                n_iters += 1
                print(n_iters)

            left_block, mid_block, right_block = self.generate_next_part(do_left, do_mid, do_right)
            if do_left:
                if left_block:
                    self.left_regex_builder.append(left_block)
                else:
                    do_left = False
            if do_right:
                if right_block:
                    self.right_regex_builder.append(right_block)
                else:
                    do_right = False
            
            if min_iter:
                if n_iters >= min_iter:
                    if self.evaluate(ignore_mid=ignore_mid):
                        return self.compile_from_builders(ignore_mid)

        if max_iter:
            print("Max iterations number exceeded")
            return self

        return None

