import sys


def leftChild(pos):
    return 2 * pos


def parent(pos):
    return pos // 2


def rightChild(pos):
    return 2 * pos + 1


class MinHeapTree:
    def __init__(self, capacity: int, neg_inf=(-1 * sys.maxsize), dump=0):
        self.capacity = capacity
        self.__size = 0
        self.Heap = [dump] * (capacity + 1)
        self.Heap[0] = neg_inf
        self.__FRONT = 1

    def get_size(self):
        return self.__size

    def isLeaf(self, pos):
        return pos * 2 > self.__size

    def swap(self, fpos, spos):
        self.Heap[fpos], self.Heap[spos] = self.Heap[spos], self.Heap[fpos]

    def minHeapify(self, pos):
        if not self.isLeaf(pos):
            spos = leftChild(pos) if self.Heap[leftChild(pos)] < self.Heap[
                rightChild(pos)] else rightChild(pos)
            if self.Heap[pos] > self.Heap[spos]:
                self.swap(pos, spos)
                self.minHeapify(spos)

    def upHeap(self, pos):
        if self.Heap[pos] < self.Heap[parent(pos)]:
            self.swap(pos, parent(pos))
            self.upHeap(parent(pos))

    def insert(self, element):
        if self.__size >= self.capacity:
            return
        self.__size += 1
        self.Heap[self.__size] = element
        self.upHeap(self.__size)
        # self.Print()

    def remove(self):
        popped = self.Heap[self.__FRONT]
        self.Heap[self.__FRONT] = self.Heap[self.__size]
        self.__size -= 1
        self.minHeapify(self.__FRONT)
        return popped

    def remove_pos(self, key):
        popped = self.Heap[key]
        self.Heap[key] = self.Heap[0]
        self.upHeap(key)
        self.__size -= 1
        self.remove()
        return popped

    def get_pop(self):
        return self.Heap[self.__FRONT]

    def __str__(self):
        return str(self.Heap)
