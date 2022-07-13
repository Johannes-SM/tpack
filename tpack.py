import numpy as np

class shape: 
    def __init__(self, name, rotations, array): 
        self.name = name
        self.rotations = rotations
        self.array = np.array(array, int)

counter = 0
grid = np.zeros((7, 7), int)
solutions = []
placed = {}
shapes = [
    shape("O", [0], 
        [
            [1, 1],
            [1, 1]
        ]),
    shape("I", [0, 1],
        [
            [1],
            [1],
            [1],
            [1]
        ]),
    shape("T", [0, 1, 2, 3],
        [
            [0, 1, 0],
            [1, 1, 1]
        ]),
    shape("J", [0, 1, 2, 3],
        [
            [0, 1],
            [0, 1],
            [1, 1]
        ]),
    shape("L", [0, 1, 2, 3],
        [
            [1, 0],
            [1, 0],
            [1, 1]
        ]),
    shape("S", [0, 1],
        [
            [0, 1, 1],
            [1, 1, 0]
        ]),
    shape("Z", [0, 1],
        [
            [1, 1, 0],
            [0, 1, 1]
        ])
]

perm_count = (grid.shape[0]*grid.shape[1])**len(shapes) # bad approximation of # of permutations

def pack(): 
    s = shapes.pop()
    for gj in range(grid.shape[0]): 
        for gi in range(grid.shape[1]): 
            if grid[gj][gi]==1: continue
            for r in s.rotations: 
                if check_adjacent(s, gj, gi, r): 
                    place(s, gj, gi, r)
                    if len(shapes) > 0: pack()
                    else: solutions.append(grid.copy()); display()
                    unplace(s, gj, gi, r)
    shapes.append(s)

def display(a = grid): 
    print(np.where(a==1, "\u25A0", "\u25A1"), '\n') # replace ints with squares

def check_adjacent(s, gj, gi, r): # check if shape can be placed
    global counter
    counter += 1
    if counter%1000000==0: print(f"\
{counter:,} permutations of {perm_count:,} possible permutations | {counter/perm_count:.2f}% complete")
    s = np.rot90(s.array, r)
    for sj in range(s.shape[0]): 
        for si in range(s.shape[1]): 
            if s[sj][si]==0: continue
            if gj+sj > grid.shape[0]-1 or gi+si > grid.shape[1]-1: return False # tile off the grid?
            if grid[gj+sj][gi+si]==1: return False # tile occupied?
            if gj+sj>0 and grid[gj+sj-1][gi+si]==1: return False # north tile occupied?
            if gj+sj<grid.shape[0]-1 and grid[gj+sj+1][gi+si]==1: return False # south tile occupied?
            if gi+si>0 and grid[gj+sj][gi+si-1]==1: return False # west tile occupied?
            if gi+si<grid.shape[1]-1 and grid[gj+sj][gi+si+1]==1: return False # east tile occupied?
    return True # no adjacent tiles occupied

def place(s, gj, gi, r): # place shape on grid
    placed[s.name] = (gj, gi)
    s = np.rot90(s.array, r)
    for sj in range(s.shape[0]): 
        for si in range(s.shape[1]): 
            if s[sj][si]==0: continue
            grid[gj+sj][gi+si] = 1

def unplace(s, gj, gi, r): # remove shape from grid
    placed.pop(s.name)
    s = np.rot90(s.array, r)
    for sj in range(s.shape[0]): 
        for si in range(s.shape[1]): 
            if s[sj][si]==0: continue
            grid[gj+sj][gi+si] = 0

if __name__ == "__main__": 
    pack()
    for sol in solutions: display(sol)
    print(f"{len(solutions)} solutions found")