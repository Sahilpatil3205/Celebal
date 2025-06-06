def lower_triangular(n):
    for i in range(n):             
        for j in range(i + 1):     
            print("*", end=" ")    
        print()                    
lower_triangular(5)