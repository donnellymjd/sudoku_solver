import string
import sys

class unit:
    
    def __init__(self, key, startvalue):
        self._key = key
        if startvalue > 0:
            self._domain = [startvalue]
        else:
            self._domain = range(1,10)
        self._value = startvalue
        self._neighbors = []
    
    def _getneighbors(self):
        rows = [chr(i) for i in range(ord('A'),ord('I')+1)]
        cols = range(1,10)
        currentrow = [self._key[0]]
        currentcol = [int(self._key[1])]
        self._neighbors.extend(["%s%01d" % t for t in zip(currentrow*9, cols)])
        self._neighbors.extend(["%s%01d" % t for t in zip(rows, currentcol*9)])
        firstrowinsq = ord(currentrow[0]) - ((ord(currentrow[0])-65)%3)
        firstcolinsq = currentcol[0] - ((currentcol[0]-1)%3)
        self._neighbors.extend(["%s%01d" % t for t in zip(sorted([chr(firstrowinsq), chr(firstrowinsq+1), chr(firstrowinsq+2)]*3), [firstcolinsq, firstcolinsq+1, firstcolinsq+2]*3)])
        self._neighbors = sorted(list(set(self._neighbors)))
        self._neighbors.remove(self._key)
    
    def _remfromD(self, value):
        temp = self._domain
#         print self._domain
        temp.remove(value)
        self._domain = temp
#         print self._domain, temp
    
class solver:
    
    def __init__(self, startboard):
        self._startingboard = startboard
        self._board = {}
        self._finalboard = startboard
        
    def ac3(self):
        queue = self.makequeue()
        while not queue == []:
            xi, xj = queue.pop(0)
            squarei = self._board[xi]
            if self._finalboard.values().count(0) == 0:
                return True
            if self.revise(squarei, xj):
                if len(squarei._domain) ==0:
                    return False
                elif len(squarei._domain) == 1:
                    temp = zip(squarei._neighbors, [xi]*20)
                    temp.remove((xj,xi))
                    queue.extend(temp)
        return False

    def revise(self, squarei, xj):
        revised = False
        if self._board[xj]._value in squarei._domain: 
            squarei._remfromD(self._board[xj]._value)
            revised = True
            if len(squarei._domain) == 1:
                squarei._value = squarei._domain[0]
                self._finalboard[squarei._key] = squarei._value
        return revised

    def backtrack_search(self):
#         print len(self.makepriorityheap({}))
        assignments = self.backtrack({})
#         print assignments
        for xi in sorted(assignments.keys()):
            self._finalboard[xi] = assignments[xi]

    def backtrack(self,assignments):
#         print assignments
        if len(assignments) == self._finalboard.values().count(0):
#             print "did this"
            return assignments
#         for xi in sorted(self._board.keys()):
        for _, xi in self.makepriorityheap(assignments):

#             print "hi", self.getvalueorasmt(xi, assignments)
#             for xi in sorted(assignments.keys()):
#                 self._finalboard[xi] = assignments[xi]
#             solvedboard = [value for (key, value) in sorted(self._finalboard.items())]
#             print ''.join([str(item) for item in solvedboard])
            
            if self.getvalueorasmt(xi, assignments) == 0:
                for value in self.getdomain(xi, assignments):
                    if self.checkconsist(xi,value,assignments):
#                         print xi, value
                        assignments[xi] = value
#                         print assignments
                        result = self.backtrack(assignments)
                        if result != False:
                            return result
                        del assignments[xi]
                return False
    
    def checkconsist(self,xi,value, assignments):
        for neighbor in self._board[xi]._neighbors:
            if value == self.getvalueorasmt(neighbor, assignments):
                return False
        return True
    
    def getdomain(self, xi, assignments):
        squarei = self._board[xi]
        if self.getvalueorasmt(xi, assignments) > 0:
            return [self.getvalueorasmt(xi, assignments)]
        else:
            domain = range(1,10)
            for neighbor in squarei._neighbors:
                neighborval = self.getvalueorasmt(neighbor, assignments)
                if neighborval in domain:
                    domain.remove(neighborval)
            return domain
    
    def getvalueorasmt(self, xi, assignments):
        if xi in assignments:
            return assignments[xi]
        else:
            return self._board[xi]._value
    
    def makepriorityheap(self, assignments):
        priorityheap = [] #Items will be tuple with remaining legal values then key
        for key in sorted(self._board.keys()):
            lendomain = len(self.getdomain(key, assignments))
            if self.getvalueorasmt(key, assignments) == 0:
                priorityheap.append((lendomain,key))
        return sorted(priorityheap)
                    
    def makequeue(self):
        queue = []
        for key in sorted(self._startingboard.keys()):
            self._board[key] = unit(key, self._startingboard[key])
            self._board[key]._getneighbors()
            queue.extend( zip([key]*20, self._board[key]._neighbors) )
        return queue
        
input = sys.argv[1]

rows = [chr(i) for i in range(ord('A'),ord('I')+1)]
cols = range(1,10)
keys = ["%s%01d" % t for t in zip(sorted(rows*9), cols*9)]
startingboard = dict(zip(keys,[int(x) for x in list(input)]))
michael = solver(startingboard)
if michael.ac3():
#     print "ac3 solved it alone"
    solvedboard = [value for (key, value) in sorted(michael._finalboard.items())]
else:
    solvedboard = [value for (key, value) in sorted(michael._finalboard.items())]
#     print ''.join([str(item) for item in solvedboard])
#     print "ac3 left {} zeros".format(michael._finalboard.values().count(0))
#     print "trying backtrack search"
    michael.backtrack_search()
#     print "backtrack left {} zeros".format(michael._finalboard.values().count(0))
    solvedboard = [value for (key, value) in sorted(michael._finalboard.items())]
# print ''.join([str(item) for item in solvedboard])
# print expectout
# answer = [int(x) for x in list(expectout)]
f = open('output.txt', 'w')
print >> f, ''.join([str(item) for item in solvedboard])
f.close()