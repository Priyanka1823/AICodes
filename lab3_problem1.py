import random

def generate_k_sat(k, m, n):
    clauses = []
    for _ in range(m):
        clause = []
        variables = random.sample(range(1, n+1), k)  # Select k distinct variables
        for var in variables:
            if random.choice([True, False]):
                clause.append(var)  # Include the variable
            else:
                clause.append(-var)  # Include the negation of the variable
        clauses.append(clause)
    return clauses

# Taking input from the user
k = int(input("Enter the value of k (length of each clause): "))
m = int(input("Enter the number of clauses (m): "))
n = int(input("Enter the number of variables (n): "))

# Generate and print the k-SAT problem
clauses = generate_k_sat(k, m, n)
print("Generated k-SAT problem:", clauses)