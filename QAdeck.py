import random
import time
import os
import platform

def load_deck(path, merge_same):
    fp1 = open("data"+"/"+path+"/front.txt",'r',encoding="utf-8")
    fp2  = open("data"+"/"+path+"/back.txt",'r',encoding="utf-8")
    fp3 = open("data/"+path+"/nhits.txt",'r')
    fp4 = open("data/"+path+"/nnum.txt",'r')
    front = fp1.readlines()
    back = fp2.readlines() 
    nhits = fp3.readlines()
    nnum = fp4.readlines()
    fp1.close()
    fp2.close()
    fp3.close()
    fp4.close()
    
    ncards = len(back)

    for i in range(0,ncards):
        back[i] = back[i].strip('\n')
        front[i] = front[i].strip('\n')
        nhits[i] = int(nhits[i].strip('\n'))
        nnum[i] = int(nnum[i].strip('\n'))

    tmp  = list(zip(front,back))

    if merge_same:
        tmp.sort()
        j=""
        d=dict()
        for i in range(len(tmp)):
            if j==tmp[i][0]:
                d[j]=d[j]+" "+tmp[i][1]
                nhits[j] += nhits.pop(i)
                nnum[j] += nnum.pop(i)
            else:
                d[tmp[i][0]]=tmp[i][1]
                j=tmp[i][0]
        deck = list(d.items())
    else:
        deck=tmp
        
    size_deck = len(deck)
    
    return deck,ncards,size_deck,nhits,nnum

def get_front_back():
    fp1 = open("data"+"/"+path+"/error/front.txt",'r',encoding="utf-8")
    fp2  = open("data"+"/"+path+"/error/back.txt",'r',encoding="utf-8")
    front = fp1.readlines()
    back = fp2.readlines() 
    fp1.close()
    fp2.close()
    
    ncards = len(back)

    for i in range(0,ncards):
        back[i] = back[i].strip('\n')
        front[i] = front[i].strip('\n')
    deck = list(zip(front,back))
    return deck,ncards,ncards

def sort_file(front,back,nhits,nnum):
    tmp  = list(zip(front,back,nhits,nnum))
    tmp.sort()
    front=list(map(lambda x: x[0], tmp))
    back=list(map(lambda x: x[1], tmp))
    nhits=list(map(lambda x: x[2], tmp))
    nnum=list(map(lambda x: x[3], tmp))
    fp1 = open("data/"+path+"/deck/front.txt",'w',encoding="utf-8")
    fp2 = open("data/"+path+"/deck/back.txt",'w',encoding="utf-8")
    fp3 = open("data/"+path+"/deck/nhits.txt",'w')
    fp4 = open("data/"+path+"/deck/nnum.txt",'w')
    for i in range(len(front)):
        fp1.write(front[i]+"\n")
        fp2.write(back[i]+"\n")
        fp3.write(str(nhits[i])+"\n")
        fp4.write(str(nnum[i])+"\n")
    fp1.close()
    fp2.close()
    fp3.close()
    fp4.close()
    
def sort_deck():
    deck,ncards,size_deck,nhits,nnum=load_deck(path+"/deck", False)
    front, back = zip(*deck)
    front = list(front)
    back = list(back)
    sort_file(front,back,nhits,nnum)

def play_options():
    while True:
        os.system(clear_comand)
        print("------------------------------------")
        print("1 - Play with all cards")
        print("2 - Play with a specific number of cards")
        print("3 - Play with back error cards")
        print("4 - Play with new cards")
        print("5 - Play cards in a rate")
        print("6 - Quit")
        print("------------------------------------")
        op=int(input())
        if op==1:
            deck, ncards, size_deck,nhits,nnum = load_deck(path+"/deck",True)
        elif op==2:
            deck, ncards, size_deck,nhits,nnum = load_deck(path+"/deck",True)
            size_deck=int(input("n = "))
        elif op==3:
            deck, ncards, size_deck = get_front_back()
        elif op==4:
            deck=list(new_cards.items())
            ncards = len(deck)
            size_deck = ncards
            if size_deck==0:
                continue
        elif op==5:
            deck, ncards, size_deck,nhits,nnum = load_deck(path+"/deck",True)
            x = int(input("minimum rate = "))
            y = int(input("maximum rate = "))
            tmp=[]
            for i in range(len(deck)):
                p = divp(nhits[i],nnum[i])
                if ((p>=x)and(p<=y)):
                    tmp.append(deck[i])
            deck = tmp
            size_deck = len(deck)
        elif op==6:
            break
        else:
            continue
        
        random.shuffle(deck)
        deck = deck[0:size_deck]
        correct, wrong = test_deck(deck,size_deck)

        if ((op!=3)and(op!=4)):
            deck, ncards, size_deck,nhits,nnum = load_deck(path+"/deck",True)
            
            for i in range(len(deck)):
                for j in range(len(correct)):
                    if deck[i][0]==correct[j]:
                        nhits[i]+=1
                        nnum[i]+=1
                        break
                for j in range(len(wrong)):
                    if deck[i][0]==wrong[j]:
                        nnum[i]+=1
                        break
            fp1 = open("data"+"/"+path+"/deck/nhits.txt",'w')
            fp2 = open("data"+"/"+path+"/deck/nnum.txt",'w')
            for i in range(len(nhits)):
                fp1.write(str(nhits[i])+"\n")
                fp2.write(str(nnum[i])+"\n")
            fp1.close()
            fp2.close()    


def test_deck(deck,size_deck):
    correct = []
    wrong = []
    error_f = []
    error_b = []
    acertos=size_deck

    start_time = time.time()
    for i in range(0,size_deck):
        os.system(clear_comand)
        print(str(i+1)+"/"+str(size_deck)+" - "+deck[i][0]+" : ",end="")
        s=str(input())
        print(s==deck[i][1])
        if s!=deck[i][1]:
            wrong.append(deck[i][0])
            error_f.append(deck[i][0]+"\n")
            error_b.append(deck[i][1]+"\n")
            acertos = acertos - 1
            print(">> "+deck[i][1])
            while s!=deck[i][1]:
                print(deck[i][0]+" : ",end="")
                s=str(input())
        else:
            correct.append(deck[i][0])
        x=input()
    elapsed_time = time.time() - start_time
    
    os.system(clear_comand)
    print("----------------------------------------")
    for i in range(0,size_deck-acertos):
        print(str(error_f[i].strip('\n'))+" - "+str(error_b[i].strip('\n')))
    print()
    print("hits = "+str(acertos)+"/"+str(size_deck))
    print("hit rate = "+str((acertos/size_deck)*100)+" % ")
    print("time = "+str(elapsed_time))
    print("velocity = "+str(size_deck/elapsed_time))
    print("----------------------------------------")
    x=input()

    fp1 = open("data"+"/"+path+"/error/front.txt",'w',encoding="utf-8")
    fp2 = open("data"+"/"+path+"/error/back.txt",'w',encoding="utf-8")
    fp1.truncate(0)
    fp2.truncate(0)
    fp1.writelines(error_f)
    fp2.writelines(error_b)
    fp1.close()
    fp2.close()

    fp1 = open("data"+"/"+path+"/statistic/hits.txt",'a')
    fp2 = open("data"+"/"+path+"/statistic/size_deck.txt",'a')
    fp3 = open("data"+"/"+path+"/statistic/time.txt",'a')
    fp1.write(str(acertos)+"\n")
    fp2.write(str(size_deck)+"\n")
    fp3.write(str(elapsed_time)+"\n")
    fp1.close()
    fp2.close()
    fp3.close()
    
    return correct , wrong        
    
def divp(x,y):
    if y==0:
        return 0
    else:
        return 100*(x/y)

def list_deck(arg):
    deck, ncards, size_deck,nhits,nnum = load_deck(path+arg,False)
    os.system(clear_comand)
    for i in range(0,size_deck):
        print("("+str(i+1)+") "+deck[i][0]+" - "+deck[i][1])
        s=" "*len("("+str(i+1)+") ")
        print(s+str(nhits[i])+"/"+str(nnum[i])+" "+str(divp(nhits[i],nnum[i]))+"%")
    print()
    print("number of cards = "+str(ncards))
    print("size of deck = "+str(size_deck))
    x=input()
    

def list_error():
    deck,ncards,size_deck = get_front_back()
    os.system(clear_comand)
    for i in range(0,ncards):
        print("("+str(i+1)+") "+deck[i][0]+" - "+deck[i][1])
    print()
    print("number of cards = "+str(ncards))
    print("size of deck = "+str(ncards))
    x=input()    
    
def list_deck_lim(x,y):
    deck, ncards, size_deck,nhits,nnum = load_deck(path+"/deck",False)
    os.system(clear_comand)
    n=0
    for i in range(0,size_deck):
        p = divp(nhits[i],nnum[i])
        if ((p>=x) and (p<=y)):
            print("("+str(n+1)+") "+deck[i][0]+" - "+deck[i][1])
            s=" "*len("("+str(n+1)+") ")
            print(s+str(nhits[i])+"/"+str(nnum[i])+" "+str(divp(nhits[i],nnum[i]))+"%")
            n+=1
    print()
    print("number of cards = "+str(n))
    x=input()

def list_newcards():
    v=list(new_cards.items())
    os.system(clear_comand)
    for i in range(len(v)):
        print("("+str(i+1)+") "+v[i][0]+" - "+v[i][1])
    x=input()

def list_statistics():
    fp1 = open("data/"+path+"/statistic/hits.txt")
    fp2 = open("data/"+path+"/statistic/size_deck.txt")
    fp3 = open("data/"+path+"/statistic/time.txt")
    l1 = fp1.readlines()
    l2 = fp2.readlines()
    l3 = fp3.readlines()

    size = len(l1)
    os.system(clear_comand)
    print("----------------------------------------")
    tacertos = 0
    tsize_deck = 0
    ttime = 0
    for i in range(0,size):
        acertos = int(l1[i])
        size_deck = int(l2[i])
        time = float(l3[i])
        tacertos += acertos
        tsize_deck += size_deck
        ttime += time
        print(str(i+1)+" - "+str(acertos)+"/"+str(size_deck)+"  "+str((acertos/size_deck)*100)+" %  "+str(time)+" s  "+str(size_deck/time)+" r/s")
    print("----------------------------------------")
    print("TOTAL - "+str(tacertos)+"/"+str(tsize_deck)+"  "+str((tacertos/tsize_deck)*100)+" %  "+str(ttime)+" s  "+str(tsize_deck/ttime)+" r/s")
    print("----------------------------------------")
    x=input()
    
def set_path():
    global path, new_cards
    os.system(clear_comand)
    fp=open("conf/path.txt",'w')
    fp.truncate(0)
    pth=str(input("path = "))
    if pth!=path:
        new_cards=dict()
    path=pth
    fp.write(path)
    fp.close()

def get_path():
    global path
    os.system(clear_comand)
    print(path)
    x=input()
    

def add_card():
    global new_cards

    deck,ncards,size_deck,nhits,nnum=load_deck(path+"/deck", False)
    front, back = zip(*deck)
    front = list(front)
    back = list(back)
    
    while True:
        os.system(clear_comand)
        f = str(input("front = "))
        if f=="":
            break
        b = str(input("back = "))
        front.append(f)
        back.append(b)
        nhits.append(0)
        nnum.append(0)
        print("("+str(len(front))+") "+f+" - "+b)
        new_cards[f]=b
        x=input()
    sort_file(front,back,nhits,nnum)
      
def edit_card():
    global new_cards

    deck,ncards,size_deck,nhits,nnum=load_deck(path+"/deck", False)
    front, back = zip(*deck)
    front = list(front)
    back = list(back)
    
    while True:
        os.system(clear_comand)
        s = str(input("row = "))
        if s=="":
            break
        i = int(s)
        print("("+str(i)+") "+str(front[i-1])+" - "+str(back[i-1]))
        c = str(input("edite, not edit or stop (y/n/s) ? "))
        if c=="y":
            front[i-1] = str(input("front = "))
            back[i-1] = str(input("back = "))
            new_cards[front[i-1]]=back[i-1]
        elif c=="n":
            continue
        elif c=="s":
            break
        else:
            continue
    sort_file(front,back,nhits,nnum)

def delete_card():
    global new_cards

    deck,ncards,size_deck,nhits,nnum=load_deck(path+"/deck", False)
    front, back = zip(*deck)
    front = list(front)
    back = list(back)
    
    while True:
        os.system(clear_comand)
        s = str(input("row = "))
        if s=="":
            break
        i = int(s)
        print("("+str(i)+") "+str(front[i-1])+" - "+str(back[i-1]))
        c = str(input("delete, not delete or stop (y/n/s) ? "))
        if c=="y":
            if front[i-1] in new_cards:
                new_cards.pop(front[i-1])
            front.pop(i-1)
            back.pop(i-1)
            nhits.pop(i-1)
            nnum.pop(i-1)
        elif c=="n":
            continue
        elif c=="s":
            break
        else:
            continue
    sort_file(front,back,nhits,nnum)

def busca_indice():
    deck, ncards, size_deck,nhits,nnum = load_deck(path+"/deck", False)
    while True:
        try:
            os.system(clear_comand)
            s=str(input("id = "))
            if s=="":
                break
            i=int(s)
            if i<size_deck:
                print("("+str(i)+") "+str(deck[i-1][0])+" - "+str(deck[i-1][1]))
                s=" "*len("("+str(i-1)+") ")
                print(s+str(nhits[i-1])+"/"+str(nnum[i-1])+" "+str(divp(nhits[i-1],nnum[i-1]))+"%")
            else:
                print("Invalid id .....")
        except:
            print("Error.....")
        finally:
            x=input()

def busca_elem(j):
    deck, ncards, size_deck,nhits,nnum = load_deck(path+"/deck", False)
    while True:
        os.system(clear_comand)
        s=str(input("element = "))
        if s=="":
            break
        b=True
        for i in range(0,size_deck):
            if deck[i][j]==s:
                print("("+str(i+1)+") "+deck[i][0]+" - "+deck[i][1])
                s=" "*len("("+str(i)+") ")
                print(s+str(nhits[i])+"/"+str(nnum[i])+" "+str(divp(nhits[i],nnum[i]))+"%")
                b=False
        if b:
            print("'"+s+"' not found .....")
        x=input()
        
def view_decks():
    v = os.listdir(os.getcwd()+'/data')
    os.system(clear_comand)
    print("**************************")
    print("id -> name of deck")
    print("**************************")
    print("---------------------------------------")
    for i in range(0,len(v)):
        print(str(i)+" -> "+v[i])
    print("---------------------------------------")
    x=input()
    return v
    
def select_deck():
    global path, new_cards
    v = view_decks()
    size = len(v)
    while True:
        try:
            os.system(clear_comand)
            x = int(input())
            if ((x>=0) and (x<size)):
                path = v[x]
                new_cards=dict()
                break
            else:
                print("Invalid Deck ...")
                x=input()
        except:
            print("Error ..............")
            x=input()

def delete_deck():
    global path, new_cards
    if path!="standard":
        while True:
            try:
                os.system(clear_comand)
                print("---------------------------------------")
                print('You want delete Deck \''+path+'\' ?')
                print('1 - Yes')
                print('2 - No')
                print("---------------------------------------")
                op = int(input())
                if op==1:
                    pth = os.getcwd()+'/data/'+path
                    os.remove(pth+"/deck/front.txt")
                    os.remove(pth+"/deck/back.txt")
                    os.remove(pth+"/deck/nhits.txt")
                    os.remove(pth+"/deck/nnum.txt")
                    os.remove(pth+"/error/front.txt")
                    os.remove(pth+"/error/back.txt")
                    os.remove(pth+"/statistic/hits.txt")
                    os.remove(pth+"/statistic/size_deck.txt")
                    os.remove(pth+"/statistic/time.txt")
                    os.rmdir(pth+"/deck")
                    os.rmdir(pth+"/error")
                    os.rmdir(pth+"/statistic")
                    os.rmdir(pth)
                    new_cards=dict()
                    path = "standard"
                    print("Deck deleted.")
                    x=input()
                    break
                elif op==2:
                    print("You don\'t delete deck.")
                    x=input()
                    break
                else:
                    raise
            except:
                print("Error ..............")
                x=input()
    else:
        os.system(clear_comand)
        print("You can\'t delete 'standard' deck.")
        x=input()
            
    
def create_deck():
    v = os.listdir(os.getcwd()+'/data')
    pth = os.getcwd()+'/data'
    while True:
        os.system(clear_comand)
        s = str(input("write name of deck : "))
        if s not in v:
            pth += '/'+s
            os.mkdir(pth)
            os.mkdir(pth+'/deck')
            os.mkdir(pth+'/error')
            os.mkdir(pth+'/statistic')
            fp = open(pth+"/deck/front.txt",'w',encoding="utf-8")
            fp.close()
            fp = open(pth+"/deck/back.txt",'w',encoding="utf-8")
            fp.close()
            fp = open(pth+"/deck/nhits.txt",'w',encoding="utf-8")
            fp.close()
            fp = open(pth+"/deck/nnum.txt",'w',encoding="utf-8")
            fp.close()
            fp = open(pth+"/error/front.txt",'w',encoding="utf-8")
            fp.close()
            fp = open(pth+"/error/back.txt",'w',encoding="utf-8")
            fp.close()
            fp = open(pth+"/statistic/hits.txt",'w')
            fp.close()
            fp = open(pth+"/statistic/size_deck.txt",'w')
            fp.close()
            fp = open(pth+"/statistic/time.txt",'w')
            fp.close()
            break
        else:
            print('There\'s a directory with this name ....')
            x=input()
    
def menu_see():
    while True:
        try:
            os.system(clear_comand)
            print("---------------------------------------")
            print(" 1 - See Deck")
            print(" 2 - See Errors")
            print(" 3 - See Statistics")
            print(" 4 - See New Cards")
            print(" 5 - See Cards by Rate")
            print(" 6 - Back")
            print("---------------------------------------")
            op=int(input())
            if op==1:
                list_deck("/deck")
            elif op==2:
                list_error()
            elif op==3:
                list_statistics()
            elif op==4:
                list_newcards()
            elif op==5:
                x = int(input("minimum rate = "))
                y = int(input("maximum rate = "))
                list_deck_lim(x,y)
            elif op==6:
                break
            else:
                raise
        except:
            print("Error........")
            x=input()
            
def menu_path():
    while True:
        try:
            os.system(clear_comand)
            print("---------------------------------------")
            print(" 1 - Set Path")
            print(" 2 - See Path")
            print(" 3 - Back")
            print("---------------------------------------")
            op=int(input())
            if op==1:
                set_path()
            elif op==2:
                get_path()
            elif op==3:
                break
            else:
                raise
        except:
            print("Error........")
            x=input()

def menu_card():
    while True:
        try:
            os.system(clear_comand)
            print("---------------------------------------")
            print(" 1 - Add Card")
            print(" 2 - Edit Card")
            print(" 3 - Delete Card")
            print(" 4 - Back")
            print("---------------------------------------")
            op=int(input())
            if op==1:
                add_card()
            elif op==2:
                edit_card()
            elif op==3:
                delete_card()
            elif op==4:
                break
            else:
                raise
        except:
            print("Error........")
            x=input()
            
def menu_search():
    while True:
        try:
            os.system(clear_comand)
            print("---------------------------------------")
            print(" 1 - Search by Id")
            print(" 2 - Search by Front")
            print(" 3 - Search by Back")
            print(" 4 - Back")
            print("---------------------------------------")
            op=int(input())
            if op==1:
                busca_indice()
            elif op==2:
                busca_elem(0)
            elif op==3:
                busca_elem(1)
            elif op==4:
                break
            else:
                raise
        except:
            print("Error........")
            x=input()

def menu_deck():
    while True:
        try:
            os.system(clear_comand)
            print("---------------------------------------")
            print(" 1 - Create New Deck")
            print(" 2 - View all Decks")
            print(" 3 - Select Deck")
            print(" 4 - Sort Deck")
            print(" 5 - Delete Deck")
            print(" 6 - Back")
            print("---------------------------------------")
            op=int(input())
            if op==1:
                create_deck()
            elif op==2:
                view_decks()
            elif op==3:
                select_deck()
            elif op==4:
                sort_deck()
            elif op==5:
                delete_deck()
            elif op==6:
                break
            else:
                raise
        except:
            print("Error........")
            x=input()

def menu_main():
    while True:
        try:
            os.system(clear_comand)
            print("---------------------------------------")
            print(" 1 - Play")
            print(" 2 - Deck")
            print(" 3 - Card")
            print(" 4 - View")
            print(" 5 - Search")
            print(" 6 - Path")
            print(" 7 - Quit")
            print("---------------------------------------")
            op=int(input())
            if op==1:
                play_options()
            elif op==2:
                menu_deck()
            elif op==3:
                menu_card()
            elif op==4:
                menu_see()
            elif op==5:
                menu_search()
            elif op==6:
                menu_path()
            elif op==7:
                break
            else:
                raise
        except:
            print("Error........")
            x=input()

def load_conf():
    global path
    fp=open("conf/path.txt",'r')
    path=fp.read()
    fp.close()

if __name__=="__main__":
    clear_comand=""
    new_cards = dict()
    if platform.system()=="Windows":
        clear_comand='cls'
    elif platform.system()=="Linux":
        clear_comand='clear'
    load_conf()
    menu_main()
