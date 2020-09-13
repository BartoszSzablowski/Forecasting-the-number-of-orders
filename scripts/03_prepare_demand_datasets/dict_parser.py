class DictParser:
    """
    Class parsing dictionary from a given file
    """

    def __init__(self, dict_file):
        self.dict_file = dict_file
        self.dict = self._load_dict()

    
    def _load_dict(self):
        d = {}

        with open(self.dict_file, "r") as dict_file:
            for line in dict_file:
                if line == "\n":
                    continue

                line = line.replace("\n", "")
                
                if "=" in line:
                    subkey, val = self._divide_str_by_char(line, "=")

                    if "," in subkey:
                        subkey = self._create_tuple(subkey, ",")
                    
                    if "," in val:
                        val = self._create_tuple(val, ",")

                    d[key][subkey] = val
                else:
                    key = line
                    d[key] = {}

        return d


    def _divide_str_by_char(self, _string, _char):
        return _string.partition(_char)[::2]


    def _create_tuple(self, _string, _char):
        el1, el2 = self._divide_str_by_char(_string, _char)
        return (el1, el2)
