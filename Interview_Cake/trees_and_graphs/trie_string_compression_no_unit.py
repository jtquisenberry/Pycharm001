import unittest


class Trie(object):

    def __init__(self):
        self.root_node = {}

    def add_word(self, word):
        current_node = self.root_node
        is_new_word = False

        # Work downwards through the trie, adding nodes
        # as needed, and keeping track of whether we add
        # any nodes.
        for char in word:
            if char not in current_node:
                is_new_word = True
                current_node[char] = {}
            current_node = current_node[char]

        # Explicitly mark the end of a word.
        # Otherwise, we might say a word is
        # present if it is a prefix of a different,
        # longer word that was added earlier.
        if "End Of Word" not in current_node:
            is_new_word = True
            current_node["End Of Word"] = {}

        yyy = current_node
        xxx = self.root_node

        return is_new_word

















# Tests
'''
class Test(unittest.TestCase):

    def test_trie_usage(self):
        trie = Trie()

        result = trie.add_word('catch')
        self.assertTrue(result, msg='new word 1')

        result = trie.add_word('cakes')
        self.assertTrue(result, msg='new word 2')

        result = trie.add_word('cake')
        self.assertTrue(result, msg='prefix of existing word')

        result = trie.add_word('cake')
        self.assertFalse(result, msg='word already present')

        result = trie.add_word('caked')
        self.assertTrue(result, msg='new word 3')

        result = trie.add_word('catch')
        self.assertFalse(result, msg='all words still present')

        result = trie.add_word('')
        self.assertTrue(result, msg='empty word')

        result = trie.add_word('')
        self.assertFalse(result, msg='empty word present')


if __name__ == '__main__':
    unittest.main(verbosity=2)

'''

if __name__ == '__main__':
    trie = Trie()

    result = trie.add_word('catch')


    result = trie.add_word('cakes')
    result = trie.add_word('dogs')

    result = trie.add_word('cake')




    result = trie.add_word('cake')


    result = trie.add_word('caked')


    result = trie.add_word('catch')


    result = trie.add_word('')


    result = trie.add_word('')

