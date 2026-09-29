class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        pass

    def display(self):
        pass

    def search(self, target):
        pass

    def delete(self, target):
        pass

if __name__ == "__main__":
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)

    print("Linked List:")
    linked_list.display()

    print("Search:")
    print(linked_list.search(2))
    print(linked_list.search(4))

    print("Delete:")
    linked_list.delete(2)
    linked_list.display()

    linked_list.delete(1)
    linked_list.display()

    linked_list.delete(3)
    linked_list.display()
