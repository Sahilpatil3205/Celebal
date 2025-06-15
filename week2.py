class Node:

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
 
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def print_list(self):
    
        temp = self.head
        if not temp:
            print("The list is empty.")
            return
        while temp:
            print(temp.data, end=" -> ")
            temp = temp.next
        print("None")

    def delete_nth_node(self, n):
       
        try:
            if self.head is None:
                raise Exception("Cannot delete from an empty list.")

            if n <= 0:
                raise Exception("Index must be 1 or greater.")

            if n == 1:
                print(f"Deleting node at position {n} with value {self.head.data}")
                self.head = self.head.next
                return

            temp = self.head
            count = 1
            while temp and count < n - 1:
                temp = temp.next
                count += 1

            if temp is None or temp.next is None:
                raise Exception("Index out of range.")

            print(f"Deleting node at position {n} with value {temp.next.data}")
            temp.next = temp.next.next

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    ll = LinkedList()

    ll.add_node(10)
    ll.add_node(20)
    ll.add_node(30)
    ll.add_node(40)

    print("Original List:")
    ll.print_list()

    ll.delete_nth_node(2)
    print("After deleting 2nd node:")
    ll.print_list()

    ll.delete_nth_node(10)

    empty_ll = LinkedList()
    empty_ll.delete_nth_node(1)
