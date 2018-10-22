# Andrew Walsh, abw9yd, 13 Oct 18


class HashTable:

    @staticmethod
    def isPrime(n):
        if n <= 1:
            return False
        if n == 2:
            return True

        if n % 2 == 0:
            return False

        for i in range(3, n, 2):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def nextPrime(n):
        if n % 2 == 0:
            n += 1
        while not HashTable.isPrime(n):
            n += 2
        return n

    def __init__(self, size=671, maxLoad=0.75):
        self.maxLoadFactor = maxLoad
        self.ts = self.nextPrime(int(float(size)/maxLoad))
        self.load = 0.0
        self.num_elements = 0
        self.collisions = 0
        self.lastInt = 0
        self.lastStr = ""
        self.grid = None
        self.table = [""] * self.ts

        self.marker = [0] * self.ts

        self.num = 31
        self.exponentials = [1] * 25
        for i in range(1, 25):
            self.exponentials[i] = self.num * self.exponentials[i - 1]

        self.quadratics = [-1] * 1000
        for q in range(0, 1000):
            self.quadratics[q] = q * q

    def insert(self, s):
        loc = self.hash(s)
        mod = loc
        count = 0
        while self.marker[loc] and self.table[loc] != s:

            loc = (mod + self.quadratics[count]) % self.ts
            count += 1
            self.collisions += 1
        if self.table[loc] != s:
            self.table[loc] = s
            self.num_elements += 1
            self.marker[loc] = 1
            self.load = float(self.num_elements) / self.ts

    def find(self, s):
        loc = self.hash(s)
        mod = loc
        count = 0
        while self.marker[loc]:
            if self.table[loc] == s:
                return self.marker[loc]
            loc = (mod + self.quadratics[count]) % self.ts
            count += 1
        return 0

    def pc(self):
        for i in range(self.ts):
            if self.table[i] != "":
                print(self.table[i])

    def view(self):
        print("Hash uses exponentials of " + str(self.exponentials[1]))
        print("Max LoadFactor: " + str(self.maxLoadFactor))
        print("Current Load Factor: " + str(self.load))
        print("Current number of elements: " + str(self.num_elements))
        print("Size of hashTable: " + str(self.ts))
        print("Total # of Collisions: " + str(self.collisions))

    def hash(self, s):
        result = 0
        for i in range(len(s)):
            result += ord(s[i]) * self.exponentials[i]

        return result % self.ts
