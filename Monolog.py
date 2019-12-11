import sys, os, shlex, requests, random, base64, ping3, string

var = {}
commentsymbol = ";"

try:
    filename = sys.argv[1]
except IndexError:
    filename = "code.txt"
except:
    print("ERROR WHILE SEARCHING FILE")
    sys.exit()

active = ""
activebool = False

MONOLOG = {"logvar":0,"error.ignore":0,"error.continue":0,"program.repeat":0,"program.firsttime":1}
r = ""

def MB(MV): # Monolog Boolean
    global MONOLOG
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

def cut(y):
    read = False
    end = []
    e = ""
    for x in y:
        e += x
        if read == True and x == '"':
            read = False
            end.append(e.strip())
            e = ""
        elif read == False and x == '"':
            read = True
        if read == False and x == ' ':
            end.append(e.strip())
            e = ""

    end.append(e)

    END = []
    for e in end:
        if e != "" and e != "<-": END.append(e)
    return END



def checkvar(v):
    if v == "*": return "*"
    try: int(v[0]); error("Invalid Variable-Name")
    except:
        for V in v:
            if not V in string.printable[:62]+"_": error("Invalid Variable-Name")
    return v

def getfunc(func,r):
    global active, countrepeat

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

    elif func == "len":
        return str(str(len(r)))

    elif func == "active":
        active = r
        return ""
        
    elif func == "pass":
        return ""

    elif func == "cuts":
        return r[int(active):]
    elif func == "cute":
        return r[:int(active)]
    
    elif func == "os":
        os.system(r)
        return r
    
    #elif func == "colored":
        #return COLOR+r+RESET
    
    elif func == "run":
        parser(r)
        return r
    
        """
        elif func == "exe":
            F = open(r)
            for L in F: parser(L)#if parser(L) != None: break
            F.close()
            return r
        """

    elif func == "same":
        if r == active: return ""
        else: return "{SKIP}"

    elif func == "notsame":
        if not r == active: return ""
        else: return "{SKIP}"


    elif func == "double":
        return str(str(r) + str(r))

    elif func == "exit":
        MONOLOG["program.repeat"] = 0

    elif func == "crepeat":
        return str(countrepeat)

    elif func == "creset":
        countrepeat = 0
        return ""
    

    
    elif func == "return":
        return# "$MONOLOG.STOP"

    else:
        error("Invalid Function")

def parser(line,IN=""):
    global r, M, firsttime
    times = 1
    if line[:5] == "for: ":
        times = int(active)
        line = line[5:]

    if line[:7] == "start: " and firsttime == False:
        return
    elif line[:7] == "start: ": line = line[7:]

    if line[:9] == "$MONOLOG ":
        vn = line.split()[1]
        vv = int(line.split()[2])
        if vv != 0 and vv != 1: error("Invalid Boolean (0/1)")
        try: MONOLOG[vn] = vv
        except: error("Invalid Option")
    
    for a in range(times):
        sline = shlex.split(line)
        var["for"] = str(a)
        if " <- " in line:
            XX = cut(line)
            vn = XX[0]
            r = ""
            for x in XX[1:][::-1]:
                if x[0] == "(" and x[-1] == ")":
                    if x[1:-1][0] == "*": r += getfunc(x[2:-1],r) # (*func) ADD TO FINAL
                    else: r = getfunc(x[1:-1],r) # (func) DONT ADD TO FINAL
                    if r == "{SKIP}": return
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
                        r += str(var[x])

            if not vn == "*": var[vn] = r
        
firsttime = True
countrepeat = 0

while True:
    countrepeat += 1
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
            except KeyError:
                error("Is function in brackets? Does variable exist?")
            except EOFError:
                error("Unkown Error")
            
        else:
            continue

    firsttime = False
    #MONOLOG["program.firsttime"] = 0
    
    if not MB("program.repeat"):
        break
    
if MB("logvar"): print("\n"+str(var))
