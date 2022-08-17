from pascalengine.linedef import LineDef
from pascalengine.solidbspnode import SolidBSPNode

def createBSP(polygons):

    allLineDefs = []
    for i, v in enumerate(polygons):
        polygon = polygons[i]
        lineDefs = []
        for idx, val in enumerate(polygon):
            lineDef = LineDef()

            # first point, connect to second point
            if idx == 0:
                lineDef.asRoot(polygon[idx][0], polygon[idx][1], polygon[idx + 1][0], polygon[idx + 1][1], polygon[idx + 1][2], polygon[idx + 1][3])
                lineDefs.append(lineDef)
                allLineDefs.append(lineDef)

            # some point in the middle
            elif idx < len(polygon) - 1:
                lineDef.asChild(lineDefs[-1], polygon[idx + 1][0], polygon[idx + 1][1], polygon[idx + 1][2], polygon[idx + 1][3])
                lineDefs.append(lineDef)
                allLineDefs.append(lineDef)

            # final point, final line, connects back to first point
            elif idx == len(polygon) - 1:
                lineDef.asLeaf(lineDefs[-1], lineDefs[0], polygon[idx][2], polygon[idx][3])
                lineDefs.append(lineDef)
                allLineDefs.append(lineDef)

    solidBsp = SolidBSPNode(allLineDefs)
    returnees = [solidBsp, allLineDefs]
    return returnees

# # MAP ROOMS
# # Lines, each vertex connects to the next one in CW fashion
# # third element is direction its facing, when CW facing 1 = left


mapMoogus = [
    [
            ]
]

map = [
    
        # ? X, Y, 0 = right 1 = left, HEIGHT
    [
        # ? beginning section
        [30, 30, 0, 5, 1], # 1
        [90, 30, 0, 5, 1], # 2
        [90, 90, 0, 5, 1], # 4
        [30, 90, 0, 5, 1], # 3
    ],
    
    [
        # ? tutorial level
        [110, 30, 0, 10, 1], # 1
        [140, 30, 0, 10, 1], # 2
        [140, 90, 0, 10, 1], # 3
        [125, 105, 0, 10, 1], # 4
        [140, 115, 0, 10, 1], # 5
        [140, 200, 0, 10, 1], # 6
        [140, 200, 0, 10, 1], # 7
        [110, 200, 0, 10, 1], # 8
        [110, 157, 0, 10, 1], # 9
        [125, 157, 0, 10, 1], # 10
        [125, 152, 0, 10, 1], # 11 
        [110, 152, 0, 10, 1], # 12
        [110, 90, 0, 10, 1], # 13
        [125, 85, 0, 10, 1], # 14
        [110, 75, 0, 10, 1], # 15
    ],
    
    [
        [160, 30, 1, 9],
        [160, 80, 1, 9],
        [172.5, 80, 1, 9],
        [160, 90, 1, 9],
        [160, 110, 1, 9],
        [182.5, 110, 1, 9],
        [182.5, 50, 1, 9],
        [187.5, 50, 1, 9],
        [187.5, 110, 1, 9],
        [210, 110, 1, 9],
        [210, 90, 1, 9],
        [197.5, 90, 1, 9],
        [210, 80, 1, 9],
        [210, 30, 1, 9],
    ],
]

mapEnemies = [
    # ? intro section cube
    # [
    [60, 60, 'w', 0],
    # ],

    # ? tutorial level cubes
    # [
    [127, 177, 'r', 1],
    [133, 155, 'r', 2],
    [118, 115, 'r', 3],
    [132, 80, 'r', 4],
    [125, 43, 'b', 5],
    # ],
    
    # ? second level cubes
    # [
    [191, 81, 'r', 6],
    [203, 54, 'r', 7],
    [185, 40, 'r', 8],
    [177, 79, 'r', 10],
    [170, 102, 'b', 11],
    # ],
]
