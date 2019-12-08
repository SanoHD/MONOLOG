import sys, os, shlex, requests, random, base64, requests, ping3, string

var = {}
num = 0
commentsymbol = ";"
filename = sys.argv[1]

MONOLOG = {"logvar":0,"error.ignore":0,"error.continue":0}

def MB(MV): # Monolog Boolean
    if MONOLOG[MV] == 1: return True
    else: return False

def error(txt):
    if MB("error.ignore"):
        pass
    else:
        print("[ERROR] >",LN,">",txt)
        if MB("error.continue"):
            pass
        else:
            sys.exit()
    
def checkvar(v):
    if v == "*": return "*"
    try: int(v[0]); error("Invalid Variable-Name")
    except:
        for V in v:
            if not V in string.printable[:62]+"_": error("Invalid Variable-Name")
    return v

def getfunc(func,r):
    
    if func == "reversed":
        return str(r)[::-1]

    elif func == "b64e":
        return str(base64.b64encode(r.encode("utf-8")))[2:-1]

    elif func == "b64d":
        return str(base64.b64decode(r))[2:-1]

    elif func == "outln":
        print(r)
        return ""
    
    elif func == "out":
        print(r,end="")
        return ""
    
    elif func == "input":
        return input()

    elif func == "request":
        return requests.get(r)

    elif func == "ping":
        return str(ping3.ping(r))

    else:
        error("Invalid Function")

def parser(line):
    global r, M

    if line[:9] == "$MONOLOG ":
        vn = line.split()[1]
        vv = int(line.split()[2])
        if vv != 0 and vv != 1: error("Invalid Boolean (0/1)")
        try: MONOLOG[vn] = vv
        except: error("Invalid Option")
        
    




    
    sline = shlex.split(line)
    if " <- " in line:
        vn = checkvar(line.split(" <- ")[0])
        r = ""
        for x in line.split(" <- ")[1:][::-1]:
            if x[0] == "(" and x[-1] == ")":
                if x[1:-1][0] == "*": r += getfunc(x[2:-1],r) # (*func) ADD TO FINAL
                else: r = getfunc(x[1:-1],r) # (func) DONT ADD TO FINAL
                
            elif x[0] == "\"" and x[-1] == "\"":
                r += str(x[1:-1])
                
            else:
                if "+" in x or "-" in x or "*" in x or "/" in x:
                    m = x.split()
                    if m[1] == "+": r += str(int(int(m[0]) + int(m[2])))
                    elif m[1] == "-": r += str(int(int(m[0]) - int(m[2])))
                    elif m[1] == "*": r += str(int(int(m[0]) * int(m[2])))
                    elif m[1] == "/": r += str(int(int(m[0]) / int(m[2])))
                
                # BACKUP CALC IS HERE
                    
                else:
                    r += var[x]

        if not vn == "*": var[vn] = r
        

    
LN = 0
file = open(filename)
comment = False
for line in file:
    LN += 1
    line = line.strip()
    if line[:2] == "/:" and comment == False: comment = True
    elif line[:2] == ":/" and comment == True: comment = False
    if line != "" and line[0] != commentsymbol and comment == False:
        try: parser(line)
        except: error("Unkown Error")
    else:
        continue

if MB("logvar"): print("\n"+str(var))
