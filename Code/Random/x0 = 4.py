x0 = 4.0
i = 0
prev_x = x0

for i in range(1, 1000):
    f = (prev_x)**2 - 3
    df = 2 * prev_x
    
    next_x = prev_x - (f / df)
    
    if (next_x - prev_x) < 0.001 and (next_x - prev_x) > -0.001:
        print(f"Result found as: {next_x} in {i} iterations")
        break
    else:
        prev_x = next_x
else:
    print("Error, whoops")
