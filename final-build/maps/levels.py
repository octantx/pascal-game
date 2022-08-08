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
        # [30, 30, 1, 9], #1
        # [30, 80, 1, 9], #2
        # [42.5, 80, 1, 9], #3
        # [42.5, 90, 1, 9], #4
        # [30, 90, 1, 9], #5
        # [30, 110, 1 , 9], #6
        # [52.5, 110, 1, 9], #7
        # [52.5, 80, 1, 9], #8
        # [57.5, 80, 1, 9], #9
        # [57.5, 110, 1, 9], #10
        # [80, 110, 1, 9], #11
        # [80, 90, 1, 9], #12
        # [67.5, 90, 1, 9], #13
        # [67.5, 80, 1, 9], #14
        # [80, 80, 1, 9], #15
        # [80, 30, 1, 9] #16
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
        [110, 30, 0, 10, 1],
        [140, 30, 0, 10, 1],
        [140, 90, 0, 10, 1],
        [125, 105, 0, 10, 1],
        [140, 115, 0, 10, 1],
        [140, 200, 0, 10, 1],
        [140, 200, 0, 10, 1],
        [110, 200, 0, 10, 1],
        [110, 157, 0, 10, 1],
        [125, 157, 0, 10, 1],
        [125, 152, 0, 10, 1],
        [110, 152, 0, 10, 1],
        [110, 90, 0, 10, 1],
        [125, 85, 0, 10, 1],
        [110, 75, 0, 10, 1],
    ],
    
    
]

mapEnemies = [
    # ? intro section cube
    [60, 60, 'w', 0],
    
    # ? tutorial level cubes
    [127, 177, 'g', 1],
    [133, 155, 'r', 2],
    [118, 115, 'r', 3],
    [132, 80, 'r', 4],
    [125, 43, 'b', 5],
    
]
