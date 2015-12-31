#!/usr/bin/env python2

class Chromosome:
    def __init__(self, genes = [], score = 0):
        self.genes = genes
        self.score = score
        self.is_top_performer = False

    def __gt__(self, other):
        return self.score > other.score

    def __lt__(self, other):
        return self.score < other.score

    def append(self, value):
        self.genes.append(value)

    def __getitem__(self, index):
        return self.genes[index]

    def __setitem__(self, index, value):
        self.genes[index] = value

    def __len__(self):
        return len(self.genes)


if __name__ == "__main__":
    c = Chromosome(score = 1)
    d = Chromosome(score = 2)
    print(c > d)
    print(d > c)
    print(c < d)
    print(d < c)
