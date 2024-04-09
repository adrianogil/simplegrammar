""" Main class for text generation """

from random import randint


def capitalize(s):
    return s[0].upper() + s[1:]


def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        pass

    return False


def get_random_element(l):
    '''
        list l
    '''
    return l[randint(0, len(l) - 1)]


class SimpleGrammar:
    """
        Class for handling text generation
    """
    def __init__(self):
        self.reset_tags()

    def st(self, text):
        return self.set_text(text)

    def at(self, tag, expression):
        return self.add_tag(tag, expression)

    def set_text(self, text):
        self.main_text = text

        return self

    def __str__(self):
        return self.evaluate(self.main_text)

    def reset_tags(self):
        self.tags = {}
        self.static_tags = {}
        self.text_functions = {}

        self.text_functions['capitalize'] = capitalize

    def add_tag(self, tag, expression):
        """
            self.add_tag(tag='tag-name', expression=['expression_term1', 'expression_term2']) -> self

            register tag as expression
        """
        # printme('[Debug] [txtgamelib.grammar.simplegrammar] SimpleGrammar:add_tag -' + ' tag - ' + str(tag) + ' expression - ' + str(expression), debug=True)
        self.tags[tag] = expression
        return self

    def evaluate(self, text):
        # printme('[txtgamelib.grammar.simplegrammar] SimpleGrammar:evaluate -' + ' text - ' + str(text), debug=True)
        found_tags = self.parse_tags_from(text)

        tags_evaluated = self.evaluate_taglist(found_tags)

        text_evaluated = self.replace_tags_from(text, tags_evaluated)

        return text_evaluated

    def parse(self, data=None, target_tag='text'):
        if data is None:
            # Method is used statically
            data = self
            grammar = SimpleGrammar()
            return grammar.parse(data, target_tag=target_tag)

        # printme("[Debug] SimpleGrammar.parse - parsing grammar: %s" % (data,), debug=True)

        if data.__class__ == list:
            data = {"text": data}

        if data.__class__ == dict:
            return self.parse_dict(data, target_tag=target_tag)

    def parse_dict(self, dict_data, target_tag='text'):

        # printme("[Debug] SimpleGrammar.parse_dict - parsing grammar: %s" % (dict_data,), debug=True)
        for key in dict_data:
            self.add_tag(key, dict_data[key])
        return self.evaluate("#%s#" % (target_tag,))

    def evaluate_taglist(self, tag_list):
        tags_evaluated = []

        for t in tag_list:
            if '.' in t:
                real_tag = ''
                for i in range(0, len(t) - 1):
                    s = t[i]
                    if s == '.':
                        prefix_tag = t[:i]
                        real_tag = t[i + 1:]
                        # print("debug: real_tag: " + real_tag)
                        # print("debug: prefix_tag: " + prefix_tag)
                        break
                if is_integer(prefix_tag):
                    if t not in self.static_tags:
                        if real_tag in self.tags:
                            self.static_tags[t] = self.evaluate(get_random_element(self.tags[real_tag]))
                    if t in self.static_tags:
                        tags_evaluated.append(self.static_tags[t])
                elif prefix_tag in self.text_functions:
                    real_tag = self.evaluate("#" + real_tag + "#")
                    tags_evaluated.append(self.text_functions[prefix_tag](real_tag))
            elif t in self.tags:
                # print(t)
                tagged_text = get_random_element(self.tags[t])
                tags_evaluated.append(self.evaluate(tagged_text))

        return tags_evaluated

    def replace_tags_from(self, text, tag_list):
        '''
            Tags are between ##
        '''

        # print("debug: replace_tags_from " + str(tag_list))

        tag_number = 0
        inside_tag = False
        current_text = ''

        for s in text:
            if s == '#':
                if inside_tag:
                    # TODO: Fix error caused by isolated #
                    # print("%s %s" % (tag_number, tag_list))
                    current_text = current_text + tag_list[tag_number]
                    tag_number = tag_number + 1
                inside_tag = not inside_tag
            elif not inside_tag:
                current_text = current_text + s

        return current_text

    def parse_tags_from(self, text):
        '''
            Tags are between ##
        '''
        current_tag = ''
        found_tags = []
        inside_tag = False

        for s in text:
            if s == '#':
                if inside_tag:
                    found_tags.append(current_tag)
                current_tag = ''
                inside_tag = not inside_tag
            elif inside_tag:
                if s == '\n' or s == ' ':
                    inside_tag = False
                    current_tag = ''
                else:
                    current_tag = current_tag + s

        return found_tags
