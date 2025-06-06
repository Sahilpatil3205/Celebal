def upper_triangular(n):
    for i in range(n):
        for j in range(n - i):
            print("*", end=" ")
        print()
        
upper_triangular(5)