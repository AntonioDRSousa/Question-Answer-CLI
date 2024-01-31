import random
import math
import time
import os

def load_deck(path, merge_same):
    fp1 = open("data"+"/"+path+"/front.txt",'r',encoding="utf-8")
    fp2  = open("data"+"/"+path+"/back.txt",'r',encoding="utf-8")
    front = fp1.readlines()
    back = fp2.readlines()
    fp1.close()
    fp2.close()

    ncards = len(back)
    
    for i in range(0,ncards):
        back[i] = back[i].strip('\n')
        front[i] = front[i].strip('\n')

    tmp  = list(zip(front,back))

    if merge_same:
        tmp.sort()
        j=""
        d=dict()
        for i in tmp:
            if j==i[0]:
                d[j]=d[j]+" "+i[1]
            else:
                d[i[0]]=i[1]
                j=i[0]
        deck = list(d.items())
    else:
        deck=tmp
        
    size_deck = len(deck)
    
    return deck,ncards,size_deck

def play_options():
    while True:
        print("------------------------------------")
        print("1 - Play with all cards")
        print("2 - Play with a specific number of cards")
        print("3 - Play with back error cards")
        print("4 - Quit")
        print("------------------------------------")
        op=int(input())
        if op==1:
            deck, ncards, size_deck = load_deck(path+"/deck",True)
        elif op==2:
            deck, ncards, size_deck = load_deck(path+"/deck",True)
            size_deck=int(input("n = "))
        elif op==3:
            deck, ncards, size_deck = load_deck(path+"/error",True)
        elif op==4:
            break
        else:
            continue
        
        random.shuffle(deck)
        deck = deck[0:size_deck]
        test_deck(deck,size_deck)
    


def test_deck(deck,size_deck):

    error_f = []
    error_b = []
    acertos=size_deck

    start_time = time.time()
    for i in range(0,size_deck):
        print(str(i+1)+"/"+str(size_deck)+" - "+deck[i][0]+" : ",end="")
        s=str(input())
        print(s==deck[i][1])
        if s!=deck[i][1]:
            error_f.append(deck[i][0]+"\n")
            error_b.append(deck[i][1]+"\n")
            acertos = acertos - 1
        print()
    elapsed_time = time.time() - start_time

    print("----------------------------------------")
    for i in range(0,size_deck-acertos):
        print(str(error_f[i].strip('\n'))+" - "+str(error_b[i].strip('\n')))
    print()
    print("hits = "+str(acertos)+"/"+str(size_deck))
    print("hit rate = "+str((acertos/size_deck)*100)+" % ")
    print("time = "+str(elapsed_time))
    print("velocity = "+str(size_deck/elapsed_time))
    print("----------------------------------------")

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

    

def list_deck(arg):
    deck, ncards, size_deck = load_deck(path+arg,False)
    for i in range(0,size_deck):
        print("("+str(i+1)+") "+deck[i][0]+" - "+deck[i][1])
    print()
    print("number of cards = "+str(ncards))
    print("size of deck = "+str(size_deck))

def list_statistics():
    fp1 = open("data/"+path+"/statistic/hits.txt")
    fp2 = open("data/"+path+"/statistic/size_deck.txt")
    fp3 = open("data/"+path+"/statistic/time.txt")
    l1 = fp1.readlines()
    l2 = fp2.readlines()
    l3 = fp3.readlines()

    size = len(l1)

    print("----------------------------------------")
    for i in range(0,size):
        acertos = int(l1[i])
        size_deck = int(l2[i])
        time = float(l3[i])
        print(str(i+1)+" - "+str(acertos)+"/"+str(size_deck)+"  "+str((acertos/size_deck)*100)+" %  "+str(time)+" s  "+str(size_deck/time)+" r/s")
    print("----------------------------------------")
    
def set_path():
    global path
    fp=open("conf/path.txt",'w')
    fp.truncate(0)
    path=str(input("path = "))
    fp.write(path)
    fp.close()

def get_path():
    global path
    print(path)

def get_front_back():
    fp1 = open("data/"+path+"/deck/front.txt",'r+',encoding="utf-8")
    fp2 = open("data/"+path+"/deck/back.txt",'r+',encoding="utf-8")
    front = fp1.readlines()
    back = fp2.readlines()
    fp1.truncate(0)
    fp2.truncate(0)
    fp1.close()
    fp2.close()
    return front,back

def sort_file(front,back):
    tmp  = list(zip(front,back))
    tmp.sort()
    front=list(map(lambda x: x[0], tmp))
    back=list(map(lambda x: x[1], tmp))
    fp1 = open("data/"+path+"/deck/front.txt",'w',encoding="utf-8")
    fp2 = open("data/"+path+"/deck/back.txt",'w',encoding="utf-8")
    fp1.writelines(front)
    fp2.writelines(back)
    fp1.close()
    fp2.close()
    

def add_card():
    front, back = get_front_back()
    while True:
        f = str(input("front = "))
        if f=="":
            break
        b = str(input("back = "))
        front.append(f+"\n")
        back.append(b+"\n")
        for i in range(0,len(front)):
            if front[i]==(f+"\n"):
                print("("+str(i+1)+") "+front[i]+" - "+back[i])
        print()
    sort_file(front,back)
      
def edit_card():  
    front, back = get_front_back()
    while True:
        s = str(input("row = "))
        if s=="":
            break
        i = int(s)
        print("("+str(i)+") "+str(front[i-1])+" - "+str(back[i-1]))
        c = str(input("edite, not edit or stop (y/n/s) ? "))
        if c=="y":
            front[i-1] = str(input("front = "))+"\n"
            back[i-1] = str(input("back = "))+"\n"   
        elif c=="n":
            continue
        elif c=="s":
            break
        else:
            continue
    sort_file(front,back)

def delete_card():  
    front, back = get_front_back()
    while True:
        s = str(input("row = "))
        if s=="":
            break
        i = int(s)
        print("("+str(i)+") "+str(front[i-1])+" - "+str(back[i-1]))
        c = str(input("delete, not delete or stop (y/n/s) ? "))
        if c=="y":
             front.pop(i-1)
             back.pop(i-1)
        elif c=="n":
            continue
        elif c=="s":
            break
        else:
            continue
    sort_file(front,back)
    
def sort_deck():
    front, back = get_front_back()
    sort_file(front,back)

def busca_indice():
    deck, ncards, size_deck = load_deck(path+"/deck", False)
    while True:
        s=str(input("id = "))
        if s=="":
            break
        i=int(s)
        print("("+str(i)+") "+str(deck[i-1][0])+" - "+str(deck[i-1][1]))

def busca_elem(j):
    deck, ncards, size_deck = load_deck(path+"/deck", False)
    while True:
        s=str(input("element = "))
        if s=="":
            break
        for i in range(0,size_deck):
            if deck[i][j]==s:
                print("("+str(i+1)+") "+deck[i][0]+" - "+deck[i][1])
        print()
        
def view_decks():
    v = os.listdir(os.getcwd()+'/data')
    print("**************************")
    print("id -> name of deck")
    print("**************************")
    print("---------------------------------------")
    for i in range(0,len(v)):
        print(str(i)+" -> "+v[i])
    print("---------------------------------------")
    return v
    
def select_deck():
    global path
    v = view_decks()
    size = len(v)
    while True:
        try:
            x = int(input())
            if ((x>0) and (x<size)):
                path = v[x]
                break
            else:
                print("Invalid Deck ...")
        except:
            print("Error ..............")

def delete_deck():
    global path
    if path!="standard":
        while True:
            try:
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
                    os.remove(pth+"/error/front.txt")
                    os.remove(pth+"/error/back.txt")
                    os.remove(pth+"/statistic/hits.txt")
                    os.remove(pth+"/statistic/size_deck.txt")
                    os.remove(pth+"/statistic/time.txt")
                    os.rmdir(pth+"/deck")
                    os.rmdir(pth+"/error")
                    os.rmdir(pth+"/statistic")
                    os.rmdir(pth)
                    path = "standard"
                    print("Deck deleted.")
                    break
                elif op==2:
                    print("You don\'t delete deck.")
                    break
                else:
                    raise
            except:
                print("Error ..............")
            
    
def create_deck():
    v = os.listdir(os.getcwd()+'/data')
    pth = os.getcwd()+'/data'
    while True:
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
    
def menu_see():
    while True:
        try:
            print("---------------------------------------")
            print(" 1 - See Deck")
            print(" 2 - See Errors")
            print(" 3 - See Statistics")
            print(" 4 - Back")
            print("---------------------------------------")
            op=int(input())
            if op==1:
                list_deck("/deck")
            elif op==2:
                list_deck("/error")
            elif op==3:
                list_statistics()
            elif op==4:
                break
            else:
                raise
        except:
            print("Error........")
            
def menu_path():
    while True:
        try:
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

def menu_card():
    while True:
        try:
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
            
def menu_search():
    while True:
        try:
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

def menu_deck():
    while True:
        try:
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

def menu_main():
    while True:
        try:
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

def load_conf():
    global path
    fp=open("conf/path.txt",'r')
    path=fp.read()
    fp.close()

load_conf()
menu_main()
