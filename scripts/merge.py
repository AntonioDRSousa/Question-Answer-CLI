f1=open("front.txt",'r',encoding="utf-8")
f2=open("back.txt",'r',encoding="utf-8")
r1=f1.readlines()
r2=f2.readlines()
f1.close()
f2.close()

f=open("merge.txt",'w',encoding="utf-8")
for i in range(len(r1)):
    s1 = r1[i].strip('\n')
    s2 = r2[i].strip('\n')
    s = s1+" - "+s2+"\n"
    f.write(s)