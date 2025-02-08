import kociemba
#import twophase.solver  as sv
#http://kociemba.org/computervision.html


def FindSolution(state):
    solve = kociemba.solve(state)
    print("START", solve)
    #solve = "F' B' D L F2 D2 U B U' L' F' U' B F2 U2 F U F R' D F' R2 U D2 L"
    final = ""
    for x in solve.split(" "):
        if x == "U":
            x = "R L F F B B r l D R L F F B B r l"
        elif x == "U'":
            x = "R L F F B B r l d R L F F B B r l"

        elif x == "U2":
            x = "R L F F B B r l d d R L F F B B r l"

        elif "'" in x:
            x = x[:-1]
            x = str(x).lower()

        if "2" in x:
            x = x[:-1]
            x =x + x

        final += x
    return final.replace(" ", "")


def ReverseMoves(moves):
    f_moves = moves[::-1]
    f_moves = f_moves.swapcase()
    return f_moves

#print(FindSolution("URRBUFBLFUUBRRDBDDUFRUFDRDDDLLBDFBRFFLLULLRRFDFLBBBLUU"), "real")
print(ReverseMoves("RRRLFFBBrlDRLFFBBrlrbRLFFBBrlddRLFFBBrlDRRLFFBBrlDRLFFBBrllRLFFBBrlddRLFFBBrlbRRLLBBRLFFBBrlddRLFFBBrlRRLLdLLRLFFBBrlddRLFFBBrlLL"), "reverse")
#print(FindSolution(""))
if "dBrlfRLFFBBrlDRLFFBBrlDRRLLFFRRLLRLFFBBrldRLFFBBrldBB" == "dBrlfRLFFBBrlDRLFFBBrlDRRLLFFRRLLRLFFBBrldRLFFBBrldBB":
    print("same")


