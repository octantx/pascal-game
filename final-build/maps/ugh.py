map = [
    
        [110, 30, 0, 20, 2],
        [140, 30, 0, 20, 1],
        [140, 90, 0, 20, 1],
        [125, 105, 0, 20, 1],
        [140, 115, 0, 20, 1],
        [140, 200, 0, 20, 1],
        [125, 200, 0, 20, 1],
        [125, 205, 0, 20, 1],
        [140, 205, 0, 20, 1],
        [140, 220, 0, 20, 1],
        [110, 220, 0, 20, 1],
        [110, 157, 0, 20, 1],
        [125, 157, 0, 20, 1],
        [125, 152, 0, 20, 1],
        [110, 152, 0, 20, 1],
        [110, 90, 0, 20, 1],
        [125, 85, 0, 20, 1],
        [110, 75, 0, 20, 1],
    ]

# for i, v in enumerate(map):
#     map[i][0] += 80
#     # map[i][1] += 150
#     print(str(map[i]) + ',')

for i, v in enumerate(map):
    # map[i][3] -= 80
    # map[i][4] -= 1
    map[i][3] -= 10
    
    print(str(map[i]) + ',')