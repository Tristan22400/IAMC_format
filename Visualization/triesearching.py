# This file defines the class TrieNode to efficiently search a variable in IAMC format files.
# This class follows the logics of Trie (tree data structure)

class TrieNode:
    """A node in the Trie structure."""

    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    """A Trie data structure for efficient prefix-based search."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """
        Inserts a word into the Trie.

        Args:
            word (str): The word to insert.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, prefix):
        """
        Searches for all words in the Trie that start with the given prefix.

        Args:
            prefix (str): The prefix to search for.

        Returns:
            List[str]: A list of words that start with the prefix.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._find_words_with_prefix(node, prefix)

    def _find_words_with_prefix(self, node, prefix):
        """
        Recursively finds all words in the Trie that start with the given prefix.

        Args:
            node (TrieNode): The current Trie node.
            prefix (str): The current prefix.

        Returns:
            List[str]: A list of words that start with the prefix.
        """
        results = []
        if node.is_end_of_word:
            results.append(prefix)
        for char, child_node in node.children.items():
            results.extend(self._find_words_with_prefix(child_node, prefix + char))
        return results


def suggest_completions(trie, prefix):
    """
    Suggests word completions for a given prefix using the Trie.

    Args:
        trie (Trie): The Trie containing the words.
        prefix (str): The prefix to search for.

    Returns:
        List[str]: A list of word completions for the given prefix.
    """
    return trie.search(prefix)
