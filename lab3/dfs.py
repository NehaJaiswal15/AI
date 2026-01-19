from pyamaze import maze, agent, COLOR
def DFS(m):
    start=(m.rows, m.cols)
    explored=[start]
    frontlier=[start]
    dfsPath={}
    while len(frontlier)>0:
        currCell = frontlier.pop()
        if currCell==(1,1):
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell=(currCell[0], currCell[1]+1)
                elif d == 'W':
                    childCell=(currCell[0], currCell[1]-1)
                elif d == 'S':
                    childCell=(currCell[0]+1, currCell[1])
                elif d == 'N':
                    childCell=(currCell[0]-1, currCell[1])
                if childCell in explored:
                    continue
                explored.append(childCell)  #push visited
                frontlier.append(childCell)  #push into stack
                dfsPath[childCell] = currCell #store parent relationship
    fwdPath={}
    cell=(1,1)
    while cell != start:
        fwdPath[dfsPath[cell]] = cell
        cell = dfsPath[cell]
    return fwdPath

if __name__=='__main__':
    m=maze(15,10)
    m.CreateMaze(loopPercent=100)
    path = DFS(m)
    a=agent(m, footprints=True)
    m.tracePath({a:path})

    m.run()
