nhits = [0]*252
nnum = [0]*252

fp1=open("nhits.txt","w")
fp2=open("nnum.txt","w")

for i in range(0,252):
    fp1.write(str(nhits[i])+"\n")
    fp2.write(str(nnum[i])+"\n")

fp1.close()
fp2.close()