class Bad_AI:
    def __init__(self, list_words):
        """
        Function description:
        Builds the prefix trie with the list of words provided.
        :Input:
        argv1: list_words: list of str, the words to be inserted into the trie
        :Output, return or postcondition: None
        :Time complexity: O(C), where C is the total number of characters in all words
        :Time complexity analysis: In the worst case, we have to insert/iterate  over each character of each word into the trie.
        :Space complexity: O(C)
        :Space complexity analysis: In the worst case, we have to create a new node for each character of each word in the trie.
        """
        self.prefixTrie = PrefixTrie()
        for word in list_words:
            self.prefixTrie.insert(word)
        

    def check_word(self, sus_word):
        """
            (Simplified)
            Function description: Takes in a word and checks if there are any words in our prefix trie that has a levenstein distance of 1 through substitution.

            Complexity is based on modifiedDFS (main function)
        """
        results = self.prefixTrie.findWordWithLevenSubDisOne(sus_word)
        return results 



"""
Node class to be used in the Trie structure.
"""
class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.is_end_of_word = False


"""
PreFix trie to store the words, created using TrieNode class. 
"""
class PrefixTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """
        Function description:
        Inserts a word into the prefix trie
        :Input:
        argv1: word: str, the word to be inserted into the trie
        :Output, return or postcondition: None
        :Time complexity: O(n), where n is the length of the word
        :Time complexity analysis: We have to traverse each character of the word and check then insert
        :Space complexity: O(n), where n is the length of the word
        :Space complexity analysis: Worst case we have to a create a new node for each character of the word
        """
        node = self.root
        for char in word:
            index = ord(char) - ord('a')
            if node.children[index] is None:
                node.children[index] = TrieNode()
            node = node.children[index]
        node.is_end_of_word = True
    
    def modifiedDFS(node, current_depth, depth, word, substitutionUsed, current_word, results):
        """
            Approach description (if main function):

            This modifed dfs searches the prefix trie up to the depth of the sus word length.
            It checks all branches of the trie from the root node to the depth. 
            Each level of the trie corresponds to a character in the sus word at the same index, we 
            then check if these two characters match, if they dont we make our one substituion, if not we contiune.
            We do this till we hit the depth, where we make our final checks of if we are at the end of a word, and if we used our one substitution.
            We add this word/branch to our results array and return it after all traversals are done.

            :Input:
            argv1: node: TrieNode, the current node we are exploring
            argv2: current_depth: int, the current level depth in the trie, starts at 0
            argv3: depth: int, the maximum depth we can go to, which is the length of the sus word
            argv4: word: str, the sus word we are checking against
            argv5: substitutionUsed: bool, if we used our one substitution already
            argv6: current_word: str, the current word we are building up as we traverse the trie, the branch essentially
            argv7: results: list, the list that will hold all the valid words we find that match the sus word with one substitution

            :Output, return or postcondition: results: list, the list of valid words that match the sus word with one substitution
            :Time complexity:O(J * N) +O(X)
            :Time complexity analysis: 
            In the worst case, all the words added to the prefix trie share no common prefixes, and each branch is indiviual.
            So then dfs will traverse J nodes in each branch, where J is the length of the sus word. 
            So this mean J traversals for each word in the list (N). Thus O(J * N). Building up the word and 
            adding the word to results array is covered by O(X), where X is the total length of words in results.

        
            :Space complexity: O(X), where X is total length of words in results
            :Space complexity analysis: We have to store the results  in the results array, 
            which is O(X) where X is the total length of words in results. Other space requirements such 
            as the sus word which takes up O(J) space and the recursion stack in the worst case would be 
            less than O(X), where we would have to store every list_word in the results array.
        """

        #the depth of dfs should only go down to the length of the sus word, check if we are 
        #at the end of a word and if we made exacltly on substitution its a valid word, this is 
        #essentially our base case
        if current_depth == depth:
            if node.is_end_of_word and substitutionUsed:
                results.append(current_word) # resizing array is O(X) worst case, doesnt effect overall time complexity 
            #return our results array, that gets built up through the call stack, we return always after
            #hitting depth since there's no point in continuing the search (word len exceeded), this 
            #helps our time complexity
            return results
        
        #runs like normal recursive dfs where we search all neighbours of the current node, through the 
        #call stack
        for i in range(len(node.children)):
            if node.children[i] is not None:
                #we grab the child and check if it matches the same index character of the sus word
                next_char = chr(i + ord('a'))
                if i != ord(word[current_depth]) - ord('a'):
                    #if it doesnt use our one sub and keep traversing the trie, the dfs should return
                    #their results array at the base cases, either when we hit a word 
                    if not substitutionUsed:
                        # substitution
                        PrefixTrie.modifiedDFS(node.children[i],
                                    current_depth + 1, depth, word, 
                                    True, current_word + next_char, results)
                else:
                    # Match - continue without substitution
                    PrefixTrie.modifiedDFS(node.children[i],
                                current_depth + 1, depth, word,
                                substitutionUsed, current_word + next_char, results)
        return results



    def findWordWithLevenSubDisOne(self, word):
        """
        (Simplified)
        Function description: Takes in a word and checks if there are any words in our prefix trie that has a levenstein distance of 1 through substitution.

        Complexity is based on modifiedDFS (main function)
        """
        depth = len(word)
        node = self.root
        results = []
        #no need for visited, a prefix trie doesnt have cycles at all
        return PrefixTrie.modifiedDFS(node, 0, depth, word, False, "", results)

    
