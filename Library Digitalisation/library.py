import hash_table as ht

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):
    def __init__(self, book_titles, texts):  # kw logw + k logk
        self.metadata = [[book_titles[i], texts[i]] for i in range(len(book_titles))]

        self.metadata = self.merge_sort(self.metadata)
        # meta data consists of distinct words
        self.distinctmetadata = self.create_distinct_metadata()

    def distinct_words(self, book_title):  # D + logk
        reqBook = self.binary_search(self.distinctmetadata, book_title)
        return reqBook[1] if reqBook else None

    def count_distinct_words(self, book_title):  # log k
        result = self.binary_search(self.distinctmetadata, book_title)
        return len(result[1]) if result else 0

    def search_keyword(self, keyword):  # k log D
        foundBooks = []
        for [bookTitle, bookContent] in self.distinctmetadata:
            if self.search_word(bookContent,keyword):
                foundBooks.append(bookTitle)
        return foundBooks

    def search_word(self, words, target_word):  # log n 
        left, right = 0, len(words) - 1

        while left <= right:
            mid = (left + right) // 2
            mid_word = words[mid]

            if mid_word == target_word:
                return True
            elif self.compare_strings(mid_word, target_word):
                left = mid + 1
            else:
                right = mid - 1

        return False

    def print_books(self):  # kD
        for title, words in self.distinctmetadata:
            text_output = ' | '.join(words)
            print(f"{title}: {text_output}")

    def compare_strings(self, str1, str2):
        
        for i in range(min(len(str1), len(str2))):
            if str1[i] < str2[i]:
                return True
            elif str1[i] > str2[i]:
                return False

        return len(str1) <= len(str2)

    def merge_sort(self, arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])

        return self.merge(left, right)

    def merge(self, left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if self.compare_strings(left[i][0], right[j][0]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def merge_sort_words(self, words):
        if len(words) <= 1:
            return words

        mid = len(words) // 2
        left = self.merge_sort_words(words[:mid])
        right = self.merge_sort_words(words[mid:])

        return self.merge_words(left, right)

    def merge_words(self, left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if self.compare_strings(left[i], right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def create_distinct_metadata(self):
        distinct_metadata = []
        for title, words in self.metadata:

            unique_words = list(set(words))

            sorted_unique_words = self.merge_sort_words(unique_words)
            distinct_metadata.append([title, sorted_unique_words])
        return distinct_metadata

    def binary_search(self, data, target_title):
        left, right = 0, len(data) - 1
        
        while left <= right:
            mid = left + (right - left) // 2
            mid_title = data[mid][0]
            
            if mid_title == target_title:  
                return data[mid]
            elif self.compare_strings(mid_title, target_title):
                left = mid + 1
            else:
                right = mid - 1
        
        return None  


class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params): # table_size
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        if name == "Jobs":
            collision_type = "Chain"
            self.z, self.table_size = params
        elif name == "Gates":
            collision_type = "Linear" 
            self.z, self.table_size = params
        elif name == "Bezos":
            collision_type = "Double"
            self.z, self.z2, self.c2, self.table_size = params
        else:
            raise ValueError("Invalid library name")
        self.collision_type = collision_type
        self.params = params
        self.books_titles = []
        self.books_content = ht.HashMap(collision_type, params)

    def add_book(self, book_title, text):
        if not self.books_content.find(book_title):
            textHash = ht.HashSet(self.collision_type, self.params)
            for i in text:
                textHash.insert(i)
            self.books_content.insert((book_title, textHash))
            self.books_titles.append(book_title)
            # if self.collision_type == "Linear": pdb.set_trace()
        else:
            return
        
    def distinct_words(self, book_title):
        book_hash = self.books_content.find(book_title)
        if not book_hash:
            return None
            
        distinct = []
        if self.collision_type == "Chain":
            for bucket in book_hash.table:
                distinct.extend(bucket)
        else:
            distinct = [word for word in book_hash.table if word is not None]
        return distinct


    def count_distinct_words(self, book_title):
        length = 0
        if self.collision_type == "Chain":
            for text_slot in self.books_content.find(book_title).table:
                length+=len(text_slot)
            return length
        else: # Linear and Double Hashing
            for text_slot in self.books_content.find(book_title).table:
                if text_slot:
                    length+=1
            return length

    def search_keyword(self, keyword):
        matches = []
        for book_title in self.books_titles:
            if self.books_content.find(book_title).find(keyword):
                matches.append(book_title)
        return matches


    def print_books(self):
        """Print all books and their distinct words"""

        if self.collision_type == "Chain":
            for title_slot in self.books_content.table:
                for (book_title,textHash) in title_slot:
                    print(f"{book_title}: {' | '.join(' ; '.join(str(word) for word in words) if words else '<EMPTY>' for words in textHash.table)}")
                    
        else: # Linear and Double Hashing
            for title_slot in self.books_content.table:
                if title_slot:
                    (book_title, textHash) = title_slot
                    print(f"{book_title}: {' | '.join(word if word else '<EMPTY>' for word in textHash.table)}")
