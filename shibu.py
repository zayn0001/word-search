import tkinter
import random
#import enchant

width = 600
height = 600
gridsize = 13
extra = 100
grid = []
root = tkinter.Tk()
root.title("PUZZLEGAME")
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
root.geometry(f"{width}x{height+extra}+{(screenwidth-width)//2}+{(screenheight-height-extra)//2}")
selected = []
wordlist = []
gotwords = tkinter.StringVar()
gotwords.set("Words: ")
score = tkinter.StringVar()
scoreint = 0
score.set("Score: 0")
restricted = ""
#d = enchant.Dict("en_US") 
occupied = dict()
allwords = ["mishal","anas","nasim","farhan"]

for i in range(gridsize):
    grid.append([])
    for j in range(gridsize):
        grid[i].append("")
print(grid)

def checkpossible(w,i,j,ch):
    if ch == "h":
        countj = j
        for letter in w:
            if grid[i][countj] == "" or grid[i][countj]==letter:
                pass
            else:
                return False
            countj = countj+1
        return True
    elif ch == "v":
        counti = i
        for letter in w:
            if grid[counti][j] == "" or grid[counti][j]==letter:
                pass
            else:
                return False
            counti = counti+1
        return True
    elif ch == "du":
        counti = i
        countj = j
        for letter in w:
            if grid[counti][countj] == "" or grid[counti][countj]==letter:
                pass
            else:
                return False
            counti = counti-1
            countj = countj+1
        return True
    elif ch == "dd":
        counti = i
        countj = j
        for letter in w:
            if grid[counti][countj] == "" or grid[counti][countj]==letter:
                pass
            else:
                return False
            counti = counti+1
            countj = countj+1
        return True

#print(grid)
def assign(w):
    i = random.choice(range(gridsize))
    j = random.choice(range(gridsize))
    ch = random.choice(["h","v","du","dd"])
    if ch == "h":
        if j+len(w)-1<gridsize:
            if checkpossible(w, i, j, ch):
                count = j
                for letter in w:
                    grid[i][count]=letter
                    count = count+1
            else:
                return assign(w)
        else:
            return assign(w)
    elif ch == "v":
        if i+len(w)-1<gridsize:
            if checkpossible(w, i, j, ch):
                count = i
                for letter in w:
                    grid[count][j]=letter
                    count = count+1
            else:
                return assign(w)
        else:
            return assign(w)
    elif ch == "du":
        if (i-len(w)+1>=0 and j+len(w)-1<gridsize):
            if checkpossible(w, i, j, ch):
                counti = i
                countj = j
                for letter in w:
                    grid[counti][countj]=letter
                    counti = counti-1
                    countj = countj+1
            else:
                return assign(w)
        else:
            return assign(w)
    elif ch == "dd":
        if (i+len(w)-1<gridsize and j+len(w)-1<gridsize):
            if checkpossible(w, i, j, ch):
                counti = i
                countj = j
                for letter in w:
                    grid[counti][countj]=letter
                    counti = counti+1
                    countj = countj+1
            else:
                return assign(w)
        else:
            return assign(w)
    

for w in allwords:
    assign(random.choice([w,w[::-1]]))


for i in range(gridsize):
    for j in range(gridsize):
        if grid[i][j] == "":
            grid[i][j] = random.choice("abcdefghijklmnopqrstuvwxyz")
            #pass
            
def printpos(event):
    #print("%d %d" % (event.x, event.y))
    gridcol = event.x*gridsize//width
    gridrow = event.y*gridsize//height
    print("%d %d" % (gridrow, gridcol))
    print(grid[gridrow][gridcol])
    selectbox(gridrow, gridcol)


def checkvalid(gridrow, gridcol):
    global selected
    global restricted
    if len(selected) == 0:
        return True
    elif len(selected) == 1:
        if abs(selected[0][0] - gridrow)<=1 and abs(selected[0][1] - gridcol)<=1:
            if abs(selected[0][0] - gridrow)==1 and abs(selected[0][1] - gridcol)==1:
                if selected[0][1]-gridcol+selected[0][0]-gridrow==0:
                    restricted = "diagonalup"
                elif selected[0][1]-gridcol==selected[0][0]-gridrow:
                    restricted = "diagonaldown"
            elif abs(selected[0][0] - gridrow)==1 and abs(selected[0][1] - gridcol)==0:
                restricted = "vertical"
            elif abs(selected[0][0] - gridrow)==0 and abs(selected[0][1] - gridcol)==1:
                restricted = "horizontal"
            return True
    else:
        selected = sorted(selected)
        if restricted == "horizontal":
            if gridrow == selected[0][0] and ( abs(selected[0][1]-gridcol)==1 or abs(selected[-1][1]-gridcol)==1):
                return True
        if restricted == "vertical":
            if gridcol == selected[0][1] and ( abs(selected[0][0]-gridrow)==1 or abs(selected[-1][0]-gridrow)==1):
                return True
        if restricted == "diagonalup":
            if (selected[0][0]-gridrow==1 and selected[0][1]-gridcol==-1) or (selected[-1][0]-gridrow==-1 and selected[-1][1]-gridcol==1):
                return True
        if restricted == "diagonaldown":
            if (selected[0][0]-gridrow==1 and selected[0][1]-gridcol==1) or (selected[-1][0]-gridrow==-1 and selected[-1][1]-gridcol==-1):
                return True
        print(restricted)
        return False


def selectbox(gridrow, gridcol):
    
    if [gridrow,gridcol] in selected:
        c.create_rectangle(gridcol*width/gridsize, gridrow*height/gridsize, gridcol*width/gridsize + width/gridsize, gridrow*height/gridsize + height/gridsize, fill="white", outline="black")
        c.create_text(width*(2*gridcol+1)/(2*gridsize), height*(2*gridrow+1)/(2*gridsize), text=grid[gridrow][gridcol], fill="black", font=('Helvetica 15 bold'))
        selected.remove([gridrow,gridcol])
    else:
        if checkvalid(gridrow, gridcol):
            c.create_rectangle(gridcol*width/gridsize, gridrow*height/gridsize, gridcol*width/gridsize + width/gridsize, gridrow*height/gridsize + height/gridsize, fill="red", outline="black")
            c.create_text(width*(2*gridcol+1)/(2*gridsize), height*(2*gridrow+1)/(2*gridsize), text=grid[gridrow][gridcol], fill="white", font=('Helvetica 15 bold'))
            selected.append([gridrow,gridcol])

def evaluate(event):
    global selected
    global score
    global wordlist
    #global d
    global scoreint
    selected = sorted(selected)
    word = ""
    for pos in selected:
        word = word + grid[pos[0]][pos[1]]
    
    if word not in wordlist:
        if word in allwords:
            scoreint = scoreint +1
            score.set("Score: "+ str(scoreint))
            gotwords.set("Words: "+" ".join(wordlist)+" " +word)
            wordlist.append(word)
        if word[::-1] in allwords:
            scoreint = scoreint +1
            score.set("Score: "+ str(scoreint))
            gotwords.set("Words: "+" ".join(wordlist)+" " +word[::-1])
            wordlist.append(word[::-1])

    #wordlist.append(word)
    # if word not in wordlist:
    #     if d.check(word):
    #         scoreint = scoreint +1
    #         score.set("Score: "+ str(scoreint))
    #         gotwords.set("Words: "+" ".join(wordlist)+" " +word)
    #         wordlist.append(word)
    #     if d.check(word[::-1]):
    #         scoreint = scoreint +1
    #         score.set("Score: "+ str(scoreint))
    #         gotwords.set("Words: "+" ".join(wordlist)+" " + word[::-1])
    #         wordlist.append(word[::-1])
    # #print(word)
    # print(score)
    # print(word)
    refreshgrid()

    
c = tkinter.Canvas(root, bg="white",height=height, width=width)


def refreshgrid(event=1):
    global selected
    selected = []
    for i in range(gridsize):
        for j in range(gridsize):
            c.create_rectangle(j*width/gridsize, i*height/gridsize, j*width/gridsize + width/gridsize, i*height/gridsize + height/gridsize, fill="white", outline="black")
        #c.create_line(width*i/gridsize,0,width*i/gridsize,height, fill="black")
        #c.create_line(0,height*i/gridsize,width, height*i/gridsize,fill="black")
    for i in range(gridsize):
        for j in range(gridsize):
            c.create_text(width*(2*j+1)/(2*gridsize), height*(2*i+1)/(2*gridsize), text=grid[i][j], fill="black", font=('Helvetica 15 bold'))



c.bind("<Button-1>", printpos)
root.bind("<Return>", evaluate)
root.bind("<Escape>", refreshgrid)

c.pack()
scores = tkinter.Label(root, textvariable=score)
scores.pack()

words = tkinter.Label(root, textvariable=gotwords)
words.pack()
refreshgrid(1)
root.mainloop()
