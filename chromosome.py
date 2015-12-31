class Chromosome:
    def __init__(self, genes = [], score = 0):
        self.genes = genes
        self.score = score

    def append(self, value):
        self.genes.append(value)

    def __getitem__(self, index):
        return self.genes[index]

    def __setitem__(self, index, value):
        self.genes[index] = value

    def __len__(self):
        return len(self.genes)
