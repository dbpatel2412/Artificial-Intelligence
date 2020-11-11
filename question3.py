BOARD_SIZE = 4
class NQueensCSP:
    def __init__(self, N):
        self.size = N

        for i in range(BOARD_SIZE+1):
            self.variables = i   
            
        self.variables = self.variables
        x = set(range(BOARD_SIZE))
        self.domains = {v: set(x) for v in range(self.variables)}
    
    def under_attack(col, queens,{}):
        return col in queens or \
           any(abs(col - x) == len(queens)-i for i,x in enumerate(queens))
     
    def inference(self, var, value):    
        inferences = {}
        # Find all unassigned neighbors of var
        neighbors = set([v for v in self.variables if v != var and len(self.domains[v]) != 1])
        for neighbor in neighbors:
            neighbor_domain = list(self.domains[neighbor])
            # Go through all the values of the neighbor's domain, and remove any value that
            # is not consistent with the assignment {var:value}
            for val in neighbor_domain:
                if under_attack(neighbor, val, {var:value, neighbor:val}):
                    self.domains[neighbor].remove(val)
            # If the domain is empty, no inference is made and return None
            if len(self.domains[neighbor]) == 0:
                return None
            # If the domain has exactly 1 variable, add it to the inferences
            elif len(self.domains[neighbor]) == 1:
                inferences[neighbor] = list(self.domains[neighbor])[0]
        return inferences
    
    def show(self, assignment):
        locations = [(i, assignment[j]) for i, j in enumerate(self.variables)
                     if assignment.get(j, None) is not None]
        displayBoard(locations, self.size)
    
   def select(csp, assignment):
    # Implement minimum-remaining-values heuristic, i.e. choosing the variable 
    # with the fewest "legal" values
    sorted_variables = sorted(csp.domains.items(), key=lambda x: len(x[1]))
    for var_value_pair in sorted_variables:
        if var_value_pair[0] not in assignment:
            return var_value_pair[0]
    return None

def order_values(var, assignment, csp):
    return csp.domains[var]

def backtracking_search(csp):
    return backtrack({}, csp)

def backtrack(assignment, csp):
    var = select(csp, assignment)
    
    assignment_copy = assignment.copy()
    domains_copy = copy.deepcopy(csp.domains)
    inferences = {}
    
    for value in order_values(var, assignment, csp):
        if csp.is_consistent(var, value, assignment):
            assignment[var] = value
            # Update the domain for var with value
            csp.domains[var] = {value}
            inferences = csp.inference(var, value)
            if inferences != None:
                for variable in inferences:
                    if csp.is_consistent(variable, inferences[variable],assignment):
                        assignment[variable] = inferences[variable]
                    else: 
                        inferences = None
                        break
            if inferences != None: # e.g., {}, {col2: 1, col3: 2}, etc.
                result = backtrack(assignment, csp)
                if result:
                    return result
        assignment = assignment_copy.copy()
        csp.domains = copy.deepcopy(domains_copy)
    return None

num_queens = BOARD_SIZE
csp = NQueensCSP(num_queens)