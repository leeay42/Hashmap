# Name: Ah Young Lee
# OSU Email: leeah@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap (Portfolio Assignment)
# Due Date: 08/15/2023
# Description: Implementation of a HashMap using Separate Chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map.
        """
        # double current capacity when load factor is greater than
        # or equal to 1.0
        if self.table_load() >= 1:
            self.resize_table(2 * self._capacity)

        hash_val = self._hash_function(key)
        index_val = hash_val % self._capacity
        ll_at_index = self._buckets[index_val]
        node_at_ll = ll_at_index.contains(key)

        # linked list at index is empty or node with key does not exist
        # add new node at head
        if node_at_ll is None:
            ll_at_index.insert(key, value)
            self._size += 1
        # node with key exists, change value
        else:
            node_at_ll.value = value

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        empty = 0
        # loop through array
        for index in range(self._capacity):
            # size of linked list at each index of array
            if self._buckets[index].length() == 0:
                empty += 1

        return empty

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        # load factor = average number of elements in each bucket = n/m
        # n = total number of elements stored in the table
        # m = number of buckets
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map, without changing the
        underlying hash table capacity.
        """
        self._buckets = DynamicArray()
        # empty linked lists for each array bucket
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        All existing key/value pairs must remain in the new hash map,
        and all hash table links must be rehashed.
        """
        # if new_capacity is less than 1, leave method
        if new_capacity < 1:
            return

        # if new_capacity is not prime, change to next highest prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        new_hash_map = HashMap(new_capacity, self._hash_function)

        # checking if new_capacity is 2
        # _next_prime() denotes divisible by 2 as not prime
        if new_capacity == 2:
            new_hash_map._capacity = new_capacity
            new_da = DynamicArray()
            for _ in range(new_capacity):
                new_da.append(LinkedList())
            new_hash_map._buckets = new_da

        for index in range(self._capacity):
            # if linked list contains nodes
            if self._buckets[index].length() > 0:
                # rehash existing key/value pairs into new map
                for node in self._buckets[index]:
                    new_hash_map.put(node.key, node.value)

        self._buckets = new_hash_map._buckets
        self._capacity = new_hash_map._capacity

    def get(self, key: str):
        """
        Returns the value associated with the given key.
        Returns None if the key is not in the hash map
        """
        hash_val = self._hash_function(key)
        index_val = hash_val % self._capacity
        ll_at_index = self._buckets[index_val]
        node_at_ll = ll_at_index.contains(key)

        if node_at_ll is None:
            return None
        else:
            return node_at_ll.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map,
        otherwise it returns False.
        """
        hash_val = self._hash_function(key)
        index_val = hash_val % self._capacity
        ll_at_index = self._buckets[index_val]
        node_at_ll = ll_at_index.contains(key)

        if node_at_ll is None:
            return False
        else:
            return True

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        """
        hash_val = self._hash_function(key)
        index_val = hash_val % self._capacity
        ll_at_index = self._buckets[index_val]
        node_at_ll = ll_at_index.contains(key)

        if node_at_ll is not None:
            ll_at_index.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of
        a key/value pair stored in the hash map.
        """
        new_da = DynamicArray()

        for index in range(self._capacity):
            # if linked list contains nodes
            if self._buckets[index].length() > 0:
                # add key/value pairs into array as tuple
                for node in self._buckets[index]:
                    new_da.append((node.key, node.value))

        return new_da


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receives a potentially unsorted dynamic array and returns a tuple containing,
    a dynamic array comprising the mode (most occurring) value(s) of the given array,
    and an integer representing the highest frequency of occurrence for the mode value(s).
    """
    map = HashMap()
    mode_da = DynamicArray()
    max_freq = 1

    # create hash_dictionary (key is the element in da, value is # occurrence)
    # for each element in given dynamic array
    for index in range(da.length()):
        da_key_val = da[index]
        # if hashmap already contains element, update associated value in hash
        if map.contains_key(da_key_val):
            map.put(da_key_val, map.get(da_key_val) + 1)
        # add in element to hashmap, value is 1
        else:
            map.put(da_key_val, 1)

    # new array with key/value tuples
    da_dict = map.get_keys_and_values()

    # go through new array with tuples
    for index in range(da_dict.length()):
        # if tuple has value higher than frequency
        if da_dict[index][1] > max_freq:
            # new array for mode, add key to new array, max freq is changed
            mode_da = DynamicArray()
            mode_da.append(da_dict[index][0])
            max_freq = da_dict[index][1]
        # # if tuple has same value as max freq, add to new array for mode
        elif da_dict[index][1] == max_freq:
            mode_da.append(da_dict[index][0])

    return (mode_da, max_freq)


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
