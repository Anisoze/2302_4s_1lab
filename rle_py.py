import symbol
import sys
import os
from tkinter import W
import turtle



def ask(num1,num2):
    while(True):
        f=(input())
        if(len(f)==0 or ord(f)<ord(str(num1)) or ord(f)>ord(str(num2))):
            print("\nwrong input\n")
        else:
            return int(f)


def ask_block():
    while(True):
        f=input()
        try:
            f=int(f)
        except:
            print("\nwrong input\n")
        else:
            if(f<1):
                print("\nwrong input\n")
            else:
                return f


def compress():         #RLE
    print("\nchoose open:\n1 - usual in_RLE.txt\n2 - file named saved_raw\n3 - out_Move-to-front.txt\n4 - other\n")
    f2=ask(1,4)
    if(f2==1):
        name="in_RLE.txt"
    elif(f2==2):
        name="saved_raw"
    elif(f2==3):
        name="out_Move-to-front.txt"
    elif(f2==4):
        print("enter name\n")
        name=input() 
    
    print("\nchoose out:\n1 - out_RLE.txt\n2 - file named compressed\n3 - other\n")
    f2=ask(1,3)
    if(f2==1):
        name2="out_RLE.txt"
    elif(f2==2):
        name2="compressed"
    elif(f2==3):
        print("enter name\n")
        name2=input() 
    
    print("\nchoose type:\n1 - r\n2 - rb\n")
    f2 = ask(1,2)
    if(f2==1):
        b=False
    elif(f2==2):
        b=True
    
    if(b):          #открыть файлы для байтов
        file=open(name, "rb")
        file2 = open(name2, "wb")


        
    else:       #открыть файлы для txt
        file = open(name, "r", encoding="utf-8")
        file2 = open(name2, "w", encoding="utf-8")
        

    if(b==False):               #текстовая строка
        data = file.read()
        data2=""
        #print(data)
        k = 1
    
        for i in range(len(data)-1):      
            if (data[i]==data[i+1]):
                k+=1
            elif(k!=1):           
                file2.write(str(k))
                data2+=str(k)
                if(ord(data[i])>47 and ord(data[i])<58):
                    file2.write(chr(96))
                    data2+=chr(96)
                file2.write(str(data[i]))
                data2+=str(data[i])
                k=1
            else:
                if(ord(data[i])>47 and ord(data[i])<58):
                    file2.write(chr(96))
                    data2+=chr(96)
                file2.write(str(data[i]))
                data2+=str(data[i])
        if(k!=1):
            file2.write(str(k))      
            data2+=str(k)
            if(ord(data[i])>47 and ord(data[i])<58):
                    file2.write(chr(96))
                    data2+=chr(96)
            file2.write(str(data[-1]))
            data2+=str(data[-1])
        else:
            file2.write(str(data[-1]))
            data2+=str(data[-1])
        #print(data2)     
        file.close()
        file2.close()
    




    else:       #байтовая строка
        data=file.read()
        data2=bytearray(b'')
        #print(data)
        k = 1        #совпадения
        q=0 #счетчик последовательности
        dt=bytearray()          #временная запись обычных
        for i in range(len(data)-1):    
            if (data[i]==data[i+1] and k<127):          #строка повтора
                if(q!=0):           #переход от обычной
                    data2.append(int('0b'+bin(q|128)[2:],2))
                    for j in dt:
                        data2.append(j)
                    q=0
                    dt=bytearray()
                k+=1
                
            elif(k!=1):         #конец стороки повтора \перебор
                data2.append(int('0b'+bin(k)[2:],2))
                data2.append(data[i])
                k=1
            else:               #обычная строка
                if(q<127):      
                    q+=1
                    dt.append(data[i])
                    g=chr(data[i])
                else:           #перебор
                    data2.append(int('0b'+bin(q|128)[2:],2))
                    for j in dt:
                        data2.append(j)
                    q=1
                    dt=bytearray()
                    dt.append(data[i])
        if(k!=1):                           #проверка в конце файла - если осталась строка повтора

            data2.append(int('0b'+bin(k)[2:],2))
            data2.append(data[-1])
        else:                                         #если осталась обычная строка
            if(q<127):
                q+=1
            data2.append(int('0b'+bin(q|128)[2:],2))
            for j in dt:
                data2.append(j)
            if(q==127):
                q=1
                data2.append(int('0b'+bin(q|128)[2:],2))
            data2.append(data[-1])
         
        file2.write(data2)  
        file.close()
        file2.close()







def decompress():           #decode RLE
  
    print("choose open:\n1 - out_RLE.txt\n2 - file named compressed\n3 - other\n")
    f2 = ask(1,3)
    if(f2==1):
        name="out_RLE.txt"
    if(f2==2):
        name="compressed"
    elif(f2==3):
        print("enter name\n")
        name=input()  

    print("choose out:\n1 - back_RLE.txt\n2 - file named decompressed\n3 - other\n")
    f2 = ask(1,3)
    if(f2==1):
        name2="back_RLE.txt"
    if(f2==2):
        name2="decompressed"
    elif(f2==3):
        print("enter name\n")
        name2=input()  
    
    print("\nchoose type:\n1 - r\n2 - rb\n")
    f2=ask(1,2)
    if(f2==1):
        b = False
    elif(f2==2):
        b = True    
            

    if (b==False):          #текстовая строка    
        file = open(name, "r", encoding="utf-8")
        file2 = open(name2, "w", encoding="utf-8")        
        data=file.read()
        data2=""
        nums=""
        for i in range(len(data)-1):
            if(ord(data[i])>47 and ord(data[i])<58 and (i==0 or data[i-1]!=chr(96))):
                nums+=str(data[i])
            elif (len(nums)!=0 and data[i]!=chr(96)):
                for j in range(int(nums)):
                    file2.write(str(data[i]))
                    data2+=str(data[i])
                nums=""
            elif(data[i]!=chr(96)):
                file2.write(data[i])
                data2+=str(data[i])
                
        if(len(nums)!=0 and data[-1]!=chr(96)):
            for j in range(int(nums)):
                file2.write(str(data[-1]))
                data2+=str(data[-1])
        elif(data[-1]!=chr(96)):
                file2.write(data[-1])
                data2+=str(data[-1])    

       
        


    else:       #байтовая строка
        file=open(name, "rb")
        file2 = open(name2, "wb")
            
        data=file.read()
        data2=bytearray(b'')
        i=0
        while(i<len(data)):
            bn=data[i]
            if((bn>>7) & 1 == 0):  #строка повтора
                i+=1
                for j in range(bn):
                    data2.append(data[i])
                i+=1
            else:  #обычная строка
                bn=bn&127
                i+=1
                for j in range(bn):
                    data2.append(data[i])
                    i+=1
                
        file2.write(data2)   
    file.close()
    file2.close()











def BWT(data, sign, b):        #BWT use part 
    lst=[]
    if(b==False):       #not bytes
        if (sign):      #специальный знак
            data=data+'\0'
        for i in range(len(data)):
            lst.append(data[i:]+data[:i])
        lst.sort()
        data2="".join([lst[i][-1] for i in range(len(data))])
        
        if (sign==False):
            ind=lst.index(data)
            
        if(sign):       #специальный знак
            return data2
        else:
            return[data2, ind]
        
    else:       #bytes
        for i in range(len(data)):
            lst.append(data[i:]+data[:i])
        lst.sort()
        data2=bytearray()
        ind=lst.index(data)
        if(ind<256):
            data2.append(0)
            data2.append(ind)
        elif(ind<65536):
            y=ind.to_bytes(2, "big")
            data2.append(int.from_bytes(y[0:1], byteorder="big"))
            data2.append(int.from_bytes(y[1:2], byteorder="big"))
        else:
            print("\nproblem with length\n")
            return
        for i in range(len(data)):
            data2.append(lst[i][-1])
        return data2




def useBWT(N, sign):        #BWT 
    print("\nchoose open:\n1 - in_BWT.txt\n2 - enwik7\n3 - other\n")
    f2=ask(1,3)
    if(f2==1):
        name="in_BWT.txt"
    elif(f2==2):
        name="enwik7"
    elif(f2==3):
        print("enter name\n")
        name=input() 
        
    print("\nchoose type:\n1 - r\n2 - rb\n")    
    f2=ask(1,2)
    if(f2==1):
        b=False
        file=open(name, "r", encoding="utf-8")
        file2 = open("out_BWT.txt", "w", encoding="utf-8")
        
    else:
        b=True
        file=open(name, "rb")
        file2 = open("out_BWT.txt", "wb")

    L=os.path.getsize(name)

    for i in range(0,L,N):
        data=file.read(N)
        if (data!=""):
            
            if (sign==False):       #без знака, не битовый (старая не эффективная версия)
                data2, ind = BWT(data, False, False)
                file2.write(data2)
                file2.write(chr(94))
                file2.write(str(ind))
                file2.write(chr(94))
                    
            else:                           #со знаком
                data2 = BWT(data, True, b)
                file2.write(data2)

                    

    file.close()
    file2.close()








def deBWT(data, file, sign):    #decode part 
    lst=[]  
    if (sign==False):   #без знака
        ind=[]
        st=""
        i=0
        while(data[i]!=chr(94)):
            lst.append(data[i])
            i+=1
        tmp=file.read(1)
        if (tmp==""):
            i+=1
            while(i<len(data)-1):
                    ind.append(data[i])
                    i+=1
            ind=int("".join(ind))
        else:
            while(tmp!=chr(94) and tmp!=""):
                st=st+tmp
                tmp=file.read(1)
            ind=int(st)
        lst.sort()
        i=0
        while(data[i+1]!=chr(94)):
            j=0
            while(data[j]!=chr(94)):
                lst[j]=data[j]+lst[j]
                j+=1
            lst.sort()
            i+=1
        return lst[ind]
    
    else:                           #со знаком
        for i in range(len(data)):
            lst.append(data[i])
        lst.sort()
        for i in range(len(data)-1):
            for j in range(len(data)):
                lst[j]=data[j]+lst[j]
            lst.sort()
        return lst[0][1:]



def unBWT(N, sign):         #decode BWT
    print("\nchoose open:\n1 - out_BWT.txt\n2 - back_Move-to-front.txt\n3 - other\n")
    f2=ask(1,3)
    if(f2==1):
        name="out_BWT.txt"
    elif(f2==2):
        name="back_Move-to-front.txt"
    elif(f2==3):
        print("enter name\n")
        name=input() 
    

    L=os.path.getsize(name)
    file=open(name, "r", encoding="utf-8")
    file2 = open("back_BWT.txt", "w", encoding="utf-8")  
    for i in range(0,L,N):       
        data=file.read(N+1)
        if (data!=""):
            data2=deBWT(data, file, sign)
            file2.write(data2)
    file.close()
    file2.close()


    







def use_BWT_permutation(data, b):
    if(b):
        pl=data[0]<<8
        pl+=data[1]
        data=data[2:]
        if(pl>65535):
            print("\nproblem with first byte\n")
            return
    L=[(data[i], i) for i in range(len(data))]
    

        

    L.sort(key=lambda x:x[0])
    P=list(zip(*L))[1]
    inv_P=[0 for i in range(len(P))]
    for i in range(len(P)):
        inv_P[P[i]]=i
        
    
    if(b==False):       #not bytes
        S=""
        ind=0
        for j in range(len(data)):
            S=data[ind]+S
            ind=inv_P[ind]
        return(S[1:])
    
    else:           #bytes
        ind=pl
        S=bytearray()
        for j in range(len(data)):
            S.insert(0, data[ind])
            ind=inv_P[ind]
        return(S)





def unBWT_permutation(N):               #decode BWT with permutations
    print("\nchoose open:\n1 - out_BWT.txt\n2 - back_Move-to-front.txt\n3 - other\n")
    f2=ask(1,3)
    if(f2==1):
        name="out_BWT.txt"
    elif(f2==2):
        name="back_Move-to-front.txt"
    elif(f2==3):
        print("enter name\n")
        name=input() 
        
    print("\nchoose out:\n1 - back_BWT.txt\n2 - other\n")
    f2=ask(1,2)
    if(f2==1):
        name2="back_BWT.txt"
    elif(f2==2):
        print("enter name\n")
        name2=input() 
    
    print("\nchoose type:\n1 - r\n2 - rb\n")
    f2=ask(1,2)
    if(f2==1):
        b=False
        file=open(name, "r", encoding="utf-8")
        file2 = open(name2, "w", encoding="utf-8")  
    elif(f2==2):
        b=True
        file=open(name, "rb")
        file2 = open(name2, "wb")  
    
    L=os.path.getsize(name)
    
    for i in range(0,L,N):  
        if(b):
            data=file.read(N+2)
        else:
            data=file.read(N+1)
        if (data!=""):
            data2=use_BWT_permutation(data, b)
            file2.write(data2)
    file.close()
    file2.close()















def average_length(name):       #average length of repeat line in BWT
    file=open(name, "r", encoding="utf-8")
    data=file.read()
    amount=0
    all_len=0
    num=1
    for i in range(len(data)-1):
        a=data[i]
        b=data[i+1]
        if a==b:
            num+=1
            if(num==3):
                amount+=1
        else:
            if(num>=3):
                all_len+=num
            num=1
    if(num>3):
        all_len+=num
            
    print("\namount of repeat lines = "+str(amount) +"\ntotal length of repeat lines = "+str(all_len))
    if(amount!=0):
        print("average length of a repeat line = " + str(all_len/amount))
    if(len(data)!=0):
        print("efficiency of compressing = "+str((all_len-2*amount)/len(data)))










def RAW(img):               #work with RAW of image
    
    print("\nchoose action:\n1 - save raw\n2 - open raw\n")               
    f = ask(1,2)
                
    if (f==1):      #save raw
        #print("choose save:\n1 - txt (not effective)\n2 - NPY\n")                    
        #f2 = ask(1,2)
        print("\nchoose out:\n1 - saved_raw\n2 - other\n")        
        f2=ask(1,2)
        if(f2==1):
            name="saved_raw"
        else:
            print("\nenter name\n")
            name=input()
            
        print("\nchoose mode:\n1 - RGB\n2 - L\n")
        f2=ask(1,2)
        if(f2==1):
            rgb=True
        else:
            rgb=False
            
        f2=2           
        if (f2==1):                           #save raw as txt
            file = open(name, "w", encoding="utf-8")
            obj=img.load()
            file.write(str(img.height) + ',' + str(img.width) +',')
            for i in range(img.height):
                for j in range(img.width):
                    file.write(str(obj[j,i][0]))
                    file.write(",")
                    file.write(str(obj[j,i][1]))
                    file.write(",")
                    file.write(str(obj[j,i][2]))
                    file.write(",")
            file.close()
                    
            return img
                        
        else:                   #save raw as array
            if(rgb):    #rgb
                obj=img.load()
                B=np.zeros([img.height,img.width, 3], dtype=np.uint8)
                #data2=bytearray()                
                for i in range(img.height):
                    for j in range(img.width):
                        for c in range (3):
                            B[i,j, c]=obj[j, i][c]
                            #data2.append(obj[j, i][c])
                file=open(name,"wb")
                np.save(file, B)
                file.close()
                

            else:   #not rgb
                obj=img.load()
                B=np.zeros([img.height,img.width], dtype=np.uint8)
                for i in range(img.height):
                    for j in range(img.width):
                        B[i,j]=obj[j, i]
                file=open(name,"wb")
                np.save(file, B)
                file.close()
                
            return img
                    
                    

    else:           #open raw
        #print("choose open:\n1 - txt\n2 - NPY\n")                    
        #f2 = ask(1,2)
        f2=2
        if (f2==1):     #open from txt
            file = open("raw.txt", "r", encoding="utf-8")
            data=file.read()
            s=""
            size_=[0,0]
            c=0
            for i in data:
                if(i!=','):
                    s+=i
                else:
                    size_[c] = int(s)
                    c+=1
                    s=""
                    if (c==2):
                        break
                   
            c=0
            j=0
            l=0
            A=np.zeros([size_[0],size_[1], 3], dtype=np.uint8)
                    
            for i in data[(len(str(size_[0]))+len(str(size_[1]))+2):]:
                if(i!=','):
                    s+=i
                else:
                    if (c==0):
                        A[l,j,c]=int(s)
                        s=""
                        c+=1
                    elif(c==1):
                        A[l,j,c]=int(s)
                        s=""
                        c+=1
                    elif(c==2):
                        A[l,j,c]=int(s)
                        s=""
                        c=0
                        j+=1
                        if(j==size_[1]):
                            j=0
                            l+=1
                            if (l==size_[0]):
                                break

            img=Image.fromarray(A, mode="RGB")
            return img
       

        elif(f2==2):       #open from NPY
            while(True):
                print("\nchoose open:\n1 - saved_raw\n2 - w_and_b_raw\n3 - grayscale_raw\n4 - color_raw\n5 - other\n")
                f2=ask(1,5)
                if(f2==1):
                    name="saved_raw"  
                elif(f2==2):
                    name="w_and_b_raw"
                elif(f2==3):
                    name="grayscale_raw"
                elif(f2==4):
                    name="color_raw"
                else:
                    print("\nenter name\n")
                    name=input()
                    
                file=open(name,"rb")
                A=np.load(file)
                file.close()
                
                print("\nchoose mode:\n1 - RGB\n2 - L\n")
                f2=ask(1,2)
                if(f2==1):
                    img=Image.fromarray(A, mode="RGB")
                    #img=Image.frombytes('RGB', )
                    return img
                else:
                    img=Image.fromarray(A, mode="L")
                    return img
         
                
     










            

def Move_to_front():            #Move-to-front 
    print("\nchoose open:\n1 - in_Move-to-front.txt\n2 - out_BWT.txt\n3 - other\n")      #выбор файлов
    f2=ask(1,3)
    if(f2==1):
        name="in_Move-to-front.txt"
    elif(f2==2):
        name="out_BWT.txt"
    elif(f2==3):
        print("\nenter name\n")
        name=input()
        
    print("\nchoose open type:\n1 - r (not effective)\n2 - rb\n")
    f2=ask(1,2)
    if(f2==1):
        file = open(name, "r", encoding="utf-8")
        b=False
    elif(f2==2):
        b=True
        file = open(name, "rb")
        
    print("\nchoose out:\n1 - out_Move-to-front.txt\n2 - file named coded_MtF\n3 - other\n")
    f2=ask(1,3)
    if(f2==1):
        if(b):
            file2 = open("out_Move-to-front.txt", "wb")
        else:
            file2 = open("out_Move-to-front.txt", "w", encoding="utf-8")
    elif(f2==2):
        file2 = open("coded_MtF", "wb")
    elif(f2==3):
        print("\nenter name\n")
        name2=input()
        if(b):
            file2 = open(name2, "wb")
        else:
            file2 = open(name2, "w", encoding="utf-8")
    


    if(b==False):           #текстовая строка
        data=file.read().encode("utf-8")
        dictionary = list(range(256))
        data2=[]
        num=0
    
        for i in data:
            num=dictionary.index(i)
            data2.append(num)
            dictionary.pop(num)
            dictionary.insert(0,i)

        data2=",".join(str(i) for i in data2)
        data2+=","





    else:           #байты
        data=file.read()
        dictionary = list(range(256))
        data2=bytearray(b'')
        num=0
    
        for i in data:
            num=dictionary.index(i)
            data2.append(num)
            dictionary.pop(num)
            dictionary.insert(0,i)


    file2.write(data2)
    file.close()
    file2.close()






def decodeMtF():            #decode Move-to-Front
    print("\nchoose open:\n1 - out_Move-to-front.txt\n2 - file named coded_MtF\n3 - back_Huffman.txt\n4 - other")      #выбор файлов
    f2=ask(1,4)
    if(f2==1):
        name="out_Move-to-front.txt"
    elif(f2==2):
        name="coded_MtF"
    elif(f2==3):
        name="back_Huffman.txt"
    elif(f2==4):
        print("\nenter name\n")
        name=input()
        
    print("\nchoose open type:\n1 - r\n2 - rb\n")
    f2=ask(1,2)
    if(f2==1):
        file = open(name, "r", encoding="utf-8")
        b=False
    elif(f2==2):
        b=True
        file = open(name, "rb")
        
    print("\nchoose out:\n1 - back_Move-to-front.txt\n2 - file named decoded_MtF\n3 - other\n")
    f2=ask(1,3)
    if(f2==1):
        if(b):
            file2 = open("back_Move-to-front.txt", "wb")
        else:
            file2 = open("back_Move-to-front.txt", "w", encoding="utf-8")
    elif(f2==2):
        file2 = open("decoded_MtF", "wb")
    elif(f2==3):
        print("\nenter name\n")
        name2=input()
        if(b):
            file2 = open(name2, "wb")
        else:
            file2 = open(name2, "w", encoding="utf-8")    

    
    if(b==False):               #текстовая строка
        data0 = file.read()
        dictionary = list(range(256))
        data=[]
        data2=[]
        sr=""
    
        for i in data0:
            if(i!=','):
                sr+=i
            else:
                data.append(int(sr))
                sr=""
    
        for i in data:
            data2.append(dictionary[i])
            d=dictionary.pop(i)
            dictionary.insert(0,d)

        data2=bytes(data2).decode("utf-8")
        



    else:                       #байты
        data = file.read()
        dictionary = list(range(256))
        data2=bytearray(b'')
    
        for i in data:
            data2.append(dictionary[i])
            d=dictionary.pop(i)
            dictionary.insert(0,d)

    file2.write(data2)
    file.close()
    file2.close()









def count_probability(data):            #find probability for Arithmetic coding
    num=0
    sr=""
    dictionary=[]
    for i in data:
        if(sr.count(i)==0):
            k=data.count(i)
            num+=k
            dictionary.append((i, k))
            sr+=i
    dictionary.sort(key=lambda x:x[1], reverse=True)
        
    probability=[]
    indices={}
    k=0
    
    for i in range(len(dictionary)):
        probability.append(dictionary[i][1]/num)
        indices[dictionary[i][0]]=k
        k+=1

   

    print("send to Arithmetic_probability.txt:\n1 - yes\n2 - no")       #save to txt
    f2 = ask(1,2)
    if(f2==1):
        file=open("Arithmetic_probability.txt", "w", encoding="utf-8")
        file.write("total="+str(num)+chr(2))
        for i in range(len(dictionary)):
            file.write(dictionary[i][0]+'='+str(dictionary[i][1])+chr(2))
        file.close()

    
    return probability, indices




def read_probability(decode):         
    file=open("Arithmetic_probability.txt", "r", encoding="utf-8")            #get probability from txt
    data=file.read()
    probability=[]
    indices={}
    sr=""
    for i in data[6:]:
        if(i!=chr(2)):
            sr+=i
        else:
            break
    num=int(sr)
    ln=len(sr)
    sr=""
    n=False        
    k=0
    sym=''

    for i in data[7+ln:]:
        if(i=='='):
            n=True
        elif(i!=chr(2) and n):
            sr+=i
        elif(i==chr(2)):
            n=False
            probability.append(int(sr)/num)
            sr=""
            if(decode):
                indices[k]=sym
                k+=1
        else:
            if(decode):
                sym=i
            else:               
                indices[i]=k
                k+=1
    return probability, indices




def arithmetic():                #Arithmetic coding for double
    file=open("in_Arithmetic.txt","r", encoding="utf-8")
    file2=open("out_Arithmetic.txt","w", encoding="utf-8")
    data=file.read()
    
          
    print("choose probability:\n1 - use count_probability\n2 - read Arithmetic_probability.txt\n")  #get probability
    f2 = ask(1,2)
    if(f2==1):
            probability, indices=count_probability(data)
    elif(f2==2):
            probability, indices=read_probability(False)

        
                
    intervals=[sum(probability[:i]) for i in range(len(probability)+1)]
    Left= 0
    Right = 1
    length=Right-Left
    num=0
    double_list=[]
    num_list=[]
    
    print("")
    i = 0
    while i < len(data):
        length=Right-Left
        Left, Right=Left+intervals[indices[data[i]]]*length, Left+intervals[indices[data[i]]+1]*length
        print(str(num)+" "+str(Left)+" "+str(Right))
        for j in range(len(indices)):
            L, R=Left+intervals[j]*length, Left+intervals[j+1]*length
            if (L==R):
                print("Error may occur")
                double_list.append(tmp)
                Left=0
                Right=1
                num_list.append(num)
                num=-1          
                i-=1
                break
        i+=1
        num+=1
        tmp=(Left+Right)/2
    double_list.append((Left+Right)/2)
    num_list.append(num)
    print("\n")
    for i in range(len(double_list)):
        print(str(num_list[i])+" "+str(double_list[i]))
        file2.write(str(num_list[i])+","+str(double_list[i])+",")
    file.close()
    file2.close()
    
    

   




def decode_arithmetic():                    
    file=open("out_Arithmetic.txt","r", encoding="utf-8")           #decode Arithmetic coding
    file2=open("back_Arithmetic.txt","w", encoding="utf-8")
    
    probability, indices=read_probability(True)
    sr=""
    double_list=[]
    num_list=[]
    data=file.read()
    
    nm=True
    for i in data:
        if(i!=","):
            sr+=i
        elif(nm):
            num_list.append(int(sr))
            sr=""
            nm=False
        else:
            double_list.append(Decimal(sr))
            sr=""
            nm=True
            
    intervals=[sum(probability[:i]) for i in range(len(probability)+1)]
    data2=""
    for c in range(len(double_list)):
        Left=0
        Right=1
        number=double_list[c]
        num=num_list[c]
        j=0
        changing_intervals=intervals
    
        while(Left!=Right and j<num):
            index_interval=sum([number>i for i in changing_intervals])-1
            data2=data2+indices[index_interval]
            Left = changing_intervals[index_interval]
            Right = changing_intervals[index_interval+1]
            length=Right-Left
            changing_intervals=[Left+length*intervals[i] for i in range(len(intervals))]
            print(changing_intervals)
            j+=1
            
    print("\n"+data2)
    file2.write(data2)
    file.close()
    file2.close()
    







def probability_Huffman(data, rd, b):          #probability_Huffman
    
    if(rd==False):  #count
        dictionary=[]
        if(b):              #bytes
            
            sr=bytearray()
            i=0
            for i in data:
                if(sr.count(i) == 0):
                    k=data.count(i)
                    dictionary.append((i, k))
                    sr.append(i)
                    
        else:           #not bytes
            sr=""
            num=0
            for i in data:
                if(sr.count(i)==0):
                    k=data.count(i)
                    num+=k
                    dictionary.append((i, k))
                    sr+=i
        dictionary.sort(key=lambda x: (x[1], x[0]))
  

        print("send to Huffman_probability.txt:\n1 - yes\n2 - no\n")       #save to txt
        f2 = ask(1,2)
        if(f2==1):
            if(b):      #bytes
                data2=bytearray()
                file=open("Huffman_probability.txt", "wb")
                for i in range(len(dictionary)):
                    data2.append(dictionary[i][0])
                    t=math.ceil(dictionary[i][1].bit_length()/8)
                    data2.append(t)
                    if(t==3):
                        y=dictionary[i][1].to_bytes(3, "big")
                        data2.append(int.from_bytes(y[0:1], byteorder="big"))
                        data2.append(int.from_bytes(y[1:2], byteorder="big"))
                        data2.append(int.from_bytes(y[2:3], byteorder="big"))
                    elif(t==2):
                        y=dictionary[i][1].to_bytes(2, "big")
                        data2.append(int.from_bytes(y[0:1], byteorder="big"))
                        data2.append(int.from_bytes(y[1:2], byteorder="big"))
                    elif(t==1):                      
                        data2.append(dictionary[i][1])
                    else:
                        print("\n\nproblem in probability_Huffman\n\n")
                        return
                file.write(data2)
                    
            else:       #not bytes
                file=open("Huffman_probability.txt", "w", encoding="utf-8")
                file.write("total="+str(num)+chr(2))
                for i in range(len(dictionary)):
                    file.write(dictionary[i][0]+'='+str(dictionary[i][1])+chr(2))
            file.close()
    



    else:       
        if(b):      #bytes
            file=open("Huffman_probability.txt", "rb")            #get probability from txt
            data=file.read()
            i=0
            sr=bytearray()
            dictionary=[]

            while(i<len(data)):
                sym=data[i]
                i+=1
                while(i<len(data) and data[i]!=0):
                    sr.append(data[i])
                    i+=1
                n=0
                for j in range(len(sr)):
                    n+=sr[j]<<(8*(len(sr)-j-1))
                dictionary.append((sym, n))
                i+=1
                sr=bytearray()
                
        else:   #not bytes
            file=open("Huffman_probability.txt", "r", encoding="utf-8")            #get probability from txt
            data=file.read()
            i=0
        
            while(data[i]!=chr(2)):
                i+=1
        
            i+=1
            sr=""
            dictionary=[]

            while(i<len(data)):
                sym=data[i]
                i+=2
                while(i<len(data) and data[i]!=chr(2)):
                    sr+=data[i]
                    i+=1
                dictionary.append((sym, int(sr)))
                i+=1
                sr=""


    print(dictionary)
    return dictionary








def Huffman():
    print("\nchoose open:\n1 - in_Huffman.txt\n2 - out_Move-to-front.txt\n3 - out_RLE.txt\n4 - other\n")
    f2=ask(1,4)
    if(f2==1):
        name="in_Huffman.txt"
    elif(f2==2):
        name="out_Move-to-front.txt"
    elif(f2==3):
        name="out_RLE.txt"
    elif(f2==4):
        print("\nenter name\n")
        name=input()
    
    print("\nchoose out:\n1 - out_Huffman.txt\n2 - other\n")
    f2=ask(1,2)
    if(f2==1):
        name2="out_Huffman.txt"
    elif(f2==2):
        print("\nenter name\n")
        name2=input()
    
    print("\nchoose open type:\n1 - r\n2 - rb\n")
    f2=ask(1,2)
    if(f2==1):
        b=False
    elif(f2==2):
        b=True
    
    if(b):
        file=open(name, "rb")
    else:
        file=open(name, "r", encoding="utf-8")   
    file2=open(name2, "wb")
    
    data=file.read()
    data2=bytearray()
    print("\nchoose probability\n1 - count with probability_Huffman\n2 - read from Huffman_probability.txt\n")
    f2=ask(1,2)
    if(f2==1):
        dictionary=probability_Huffman(data, False, b)
    else:
        dictionary=probability_Huffman(data, True, b)
    
    A=list(list(zip(*dictionary))[1])
    
    #формирование внутренних узлов

    s=0
    r=0
    n=len(A)
    for t in range(n-1):
        #выбираем первый узел потомок
        if((s>n-1) or (r<t and A[r]<A[s])):
            #выбираем внутренний узел
            A[t]=A[r]
            A[r]=t+1
            r+=1
        else:
            #выбираем лист
            A[t]=A[s]
            s+=1
            
        #выбираем втором потомок
        if((s>n-1) or (r<t and A[r]<A[s])):
            #внутренний
            A[t]=A[t]+A[r]
            A[r]=t+1
            r+=1
        else:
            #лист
            A[t]=A[t]+A[s]
            s+=1


    #преобразование индексов родительских узлов в значения глубин каждого узла
    A[n-1]=-1
    A[n-2]=0
    t=n-2
    while(t>-1):
        A[t]=A[A[t]-1]+1
        t-=1
        
    #преобразование значения глубины внутренних узлов в значения глубины листьев (длин кодов)
    a=0
    u=0
    d=0
    t=n-2
    x=n-1
    while(True):
        #определяем количество узлов с глубиной d
        while(t>=0 and A[t]==d):
            u+=1
            t-=1
        #назначаем листьями узлы, которые не являются внутренними
        while(a>u):
            A[x]=d
            x-=1
            a-=1
        #переходми к следующему значению глубины
        a=2*u
        d+=1
        u=0
        if(a<=0):
            break
        
    print(A)
    
    Dt={}

       
    m=[0 for i in range(n)]          #подсчитываем число символов с одинаковой длиной кода
    Base=[0 for i in range(A[0]+1)]
    
    for i in range(n):
        m[A[i]]=m[A[i]]+1

        #вычисляем значение base для каждой длины кода
    s=0
    for k in range(A[0],0,-1):
        Base[k]=s>>(A[0]-k)
        s=s+(m[k]<<(A[0]-k))

        #вычисляем коды для каждого символа входного алфавита
    p=0
    B=[0 for i in range(n)]
    for i in range(n):
        if(p!=A[i]):
            j=0
            p=A[i]
        B[i]=j+Base[A[i]]
        j+=1

        
    print('')
    sr=""

    
    if(b):
        for i in range(n):
            b_=bin(B[i])[2:]
            sr+=str(dictionary[i][0])+' '+(A[i]-len(b_))*'0'+b_+'\n'
            Dt[dictionary[i][0]]=(A[i]-len(b_))*'0'+b_
    else:      
        for i in range(n):
            b_=bin(B[i])[2:]
            sr+=dictionary[i][0]+' '+(A[i]-len(b_))*'0'+b_+'\n'
            Dt[dictionary[i][0]]=(A[i]-len(b_))*'0'+b_

    print(sr)
    file3=open("dictionary_Haffman.txt", "w", encoding="utf=8")
    file3.write(sr)



    sr=""
    for i in data:
        sr+=Dt[i]
    i=0
    s=""
    k=0
    for i in sr:
        s+=i
        k+=1
        if(k==8):
            data2.append(int('0b'+s,2))
            s=""   
            k=0
    if(len(s)>0):       
        data2.append(int('0b'+s,2))
    data2.append(len(s))
      
    file2.write(data2)
    file.close()
    file2.close()
    file3.close()
    
    








def decode_Huffman():
    print("\nchoose out:\n1 - back_Huffman.txt\n2 - other\n")
    f2=ask(1,2)
    if(f2==1):
        name="back_Huffman.txt"
    elif(f2==2):
        print("\nenter name\n")
        name=input()
    print("\nchoose out type\n1 - w\n2 - wb\n")
    f2=ask(1,2)
    if(f2==1):
        bt=False
        file2=open(name,"w", encoding="utf-8")
        data2=""
    else:
        bt=True
        file2=open(name,"wb")
        data2=bytearray()
    file=open("out_Huffman.txt","rb")
    file3=open("dictionary_Haffman.txt","r", encoding="utf-8")
    data=file.read()
    data3=file3.read()

    if(bt):         #bytes
        sym=""
        sr=""
        Dt={}
        i=0
        while(i<len(data3)):
            while(data3[i]!=' '):
                sym+=data3[i]
                i+=1
            i+=1            
            while(i<len(data3) and data3[i]!='\n'):
                sr+=data3[i]
                i+=1
            Dt[sr]=int(sym)
            sym=""
            i+=1
            sr=""
    
        sr=""
        i=0
        q=data[-1]
        while(i<len(data)-1):
            b=bin(data[i])[2:]
            if(len(b)<8 and i!=len(data)-2):
                b=(8-len(b))*'0'+b  
            if(i!=len(data)-2):
                for j in b:
                    sr+=j
                    if(sr in Dt):
                        data2.append(Dt[sr])
                        sr=""
            else:
                if(len(b)<q):
                    b=(q-len(b))*'0'+b
                for j in b:
                    sr+=j
                    if(sr in Dt):
                        data2.append(Dt[sr])
                        sr=""
            i+=1        

    else:           #not bytes
        sym=''
        sr=""
        Dt={}
        i=0
        while(i<len(data3)):
            sym=data3[i]
            i+=2
            while(i<len(data3) and data3[i]!='\n'):
                sr+=data3[i]
                i+=1
            Dt[sr]=sym
            i+=1
            sr=""
    
        sr=""
        i=0
        q=data[-1]
        while(i<len(data)-1):
            b=bin(data[i])[2:]
            if(len(b)<8 and i!=len(data)-2):
                b=(8-len(b))*'0'+b
            if(i!=len(data)-2):
                for j in b:
                    sr+=j
                    if(sr in Dt):
                        data2+=Dt[sr]
                        sr=""
            else:
                if(len(b)<q):
                    b=q-len(b)*'0'+b
                for j in b:
                    sr+=j
                    if(sr in Dt):
                        data2+=Dt[sr]
                        sr=""
            i+=1
            




    file2.write(data2)
    file.close()
    file2.close()
    file3.close()
                
    
    






def canonical_codes(mode):              #canonical codes for Huffman

    if(mode==False):
        file=open("in_Huffman_codes_normal.txt","r", encoding="utf-8")      
    else:
        file=open("in_Huffman_codes_length.txt","r", encoding="utf-8")  
    file2=open("out_Huffman_codes.txt","w", encoding="utf-8")
    data=file.read()
    data2=""
    codes=[]
    

    i=0
    while(i<len(data)):
        sim=data[i]
        sr=""
        i+=1
        while(i<len(data) and data[i]!='\n'):
            sr+=data[i]
            i+=1
        i+=1
        if(mode):
            codes.append((sim, int(sr)))
        else:
            codes.append((sim, len(sr)))
       

    codes.sort(key=lambda x: (x[1], x[0]))
    print(codes)

    sr=""
    n=0
    bn=0
    for i in range(len(codes)):
        if(i!=0):
            bn+=1
        if(codes[i][1]>n):
            bn=bn<<(codes[i][1]-n)
            n=codes[i][1]        
        codes[i]=(codes[i][0], bin(bn)[2:])
    print('')
    for i in range(len(codes)):
        data2+=codes[i][0]+codes[i][1]+'\n'
    print(data2)
    file2.write(data2)
    











def basic_suffix(name, out):                    #suffix array for string
    file=open(name, "r", encoding="utf-8")
    data=file.read()
    data+='\0'
    data2=[]
    data3=""
    A={}
    for i in range(len(data)):
        A[data[i:]]=i
    for i in sorted(A.items()):
        data2.append(i[1])
        data3+=str(i[1])+','
    data3=data3[:-1]
    print('')
    print(data3)
    if(out):
        file2=open("out_basic_suffix", "w", encoding="utf-8")
        file2.write(data3)
        file2.close()
    file.close()
    return (data, data2)
   











def suffix_column(data):                #last column for BWT
    data2=""
    file=open("out_suffix_column.txt", "w", encoding="utf-8")
    for i in range(len(data[0])):
        data2+=data[0][data[1][i]-1]
    print(data2)
    file.write(data2)
    file.close()










def S_and_L():          #S and L string from string
    file=open("in_S_and_L.txt", "r", encoding="utf-8")
    file2=open("out_S_and_L.txt", "w", encoding="utf-8")
    data=file.read()
    
    A="S"
    for i in range(len(data[:-2]),-1,-1):
        if(ord(data[i])<ord(data[i+1])):
            A='S'+A
        elif(ord(data[i])>ord(data[i+1])):
            A='L'+A
        else:
            A=A[0]+A
    print('\n'+A)
    file2.write(A)
    file.close()
    file2.close()
    










def entropy():
    print("\nchoose open:\n1 - in_entropy.txt\n2 - enwik7\n3 - other\n")
    f2=ask(1,3)
    if(f2==1):
        name="in_entropy.txt"
    elif(f2==2):
        name="enwik7"
    elif(f2==3):
        print("\nenter name\n")
        name=input()
    
    print("\nchoose type:\n1 - r\n2 - rb\n")
    f2=ask(1,2)
    if(f2==1):
        b=False
        file=open(name, "r", encoding="utf-8")
        #file2=open("probability.txt", "w", encoding="utf-8")
        sr=""
        
    else:
        b=True
        file=open(name, "rb")
        #file2=open("probability.txt", "wb")
        sr=bytearray()
        
    
    data=file.read()
    Dt={}
    S=0
    if(b==False):
        for i in data:
            if(i in sr):
                Dt[i]+=1
            else:
                sr+=i
                Dt[i]=1
    
    else:
        for i in data:
            if(i in sr):
                Dt[i]+=1
            else:
                sr.append(i)
                Dt[i]=1

    S=0
    ln=len(data)
    for i in Dt:
        S+=Dt[i]/ln*math.log2(Dt[i]/ln)
    print("\nentropy = " +str(-S) + "\nlen data = " +str(ln) +"\ncompressed = " + str(ln*(-S)/8))
    








def LZ77():                                         #LZ77
    print("\nchoose open:\n1 - in_LZ77.txt\n2 - enwik7\n3 - other\n")
    f2=ask(1,3)
    if(f2==1):
        name="in_LZ77.txt"
    elif(f2==2):
        name="enwik7"
    elif(f2==3):
        print("\nenter name\n")
        name=input()
    
    print("\nchoose out:\n1 - out_LZ77.txt\n2 - other\n")
    f2=ask(1,2)
    if(f2==1):
        name2="out_LZ77.txt"
    elif(f2==2):
        print("\nenter name\n")
        name2=input()
        
    file=open(name, "rb")
    

    file2=open(name2, "wb")
        
  
    #print("\nchoose mode:\n1 - with byte use\n2 - normal\n")
    #mode=ask(1,2)
    mode=1
    data=file.read()
    if(mode==1):
        data2=bytearray()
        data3=bytearray()
    else:
        data2=""
        
    print("\nenter buffer size\n")
    while(True):
        buff_size=ask_block()
        if(buff_size>32767):
            print("\nchoose a smaller buffer (max 32767)\n")
        else:
            break
    buff=""
    list_of_turples=[]
    i=0
    k=0
    q=0
    dt=bytearray()

    while(i<len(data)):
        buff=data[max(i-buff_size,0):i]
        L=0
        start=len(buff)
        while(True):
            s=data[i:i+L+1]
            if(buff.find(s)>=0 and i+L < len(data)):
                start=buff.find(s)
                L+=1
            else:
                break
            
        if(mode==1):    #use bytes
            if(L>0):        #turple
                if(q>0):        #single not empty
                    data2.append(int('0b'+bin(q|128)[2:],2))
                    q=0
                    for j in data3:
                        data2.append(j)
                    data3=bytearray()
                elif(k==127):                               #out of range
                    data2.append(int('0b'+bin(k)[2:],2))
                    for j in list_of_turples:
                        if(j[0]>127):                            #takes 2 bytes  
                            y=j[0].to_bytes(2, "big")
                            data2.append(int.from_bytes(y[0:1], byteorder="big"))
                            data2.append(int.from_bytes(y[1:2], byteorder="big"))
                        else:                                       #takes 1 byte
                            data2.append(int('0b'+bin(j[0]|128)[2:],2))
                        if(j[1]>127):                              
                            y=j[1].to_bytes(2, "big")
                            data2.append(int.from_bytes(y[0:1], byteorder="big"))
                            data2.append(int.from_bytes(y[1:2], byteorder="big"))
                        else:
                            data2.append(int('0b'+bin(j[1]|128)[2:],2))
                    k=0
                    list_of_turples=[]
                substring_turple=(len(buff)-start,L)
                list_of_turples.append(substring_turple)
                i+=L-1
                k+=1
            


            else:       #single
                if(k>0):        #turple not empty
                    data2.append(int('0b'+bin(k)[2:],2))
                    for j in list_of_turples:
                        if(j[0]>127):                            #takes 2 bytes  
                            y=j[0].to_bytes(2, "big")
                            data2.append(int.from_bytes(y[0:1], byteorder="big"))
                            data2.append(int.from_bytes(y[1:2], byteorder="big"))                           
                        else:                                       #takes 1 byte
                            data2.append(int('0b'+bin(j[0]|128)[2:],2))
                        if(j[1]>127):                              
                            y=j[1].to_bytes(2, "big")
                            data2.append(int.from_bytes(y[0:1], byteorder="big"))
                            data2.append(int.from_bytes(y[1:2], byteorder="big"))
                        else:
                            data2.append(int('0b'+bin(j[1]|128)[2:],2))
                    k=0
                    list_of_turples=[]
                elif(q==127):           #out of range
                    data2.append(int('0b'+bin(q|128)[2:],2))
                    q=0
                    for j in data3:
                        data2.append(i)
                    data3=bytearray()
                q+=1
                data3.append(data[i])
            i+=1
            

        else:   #normal  не используется
            if(i+L+1<len(data)):
                if(L>0):
                    substring_turple=(len(buff)-start,L)
                else:                   
                    substring_turple=(len(buff)-start,L, data[i+L])
            else:
                if(L>0):
                    substring_turple=(len(buff)-start,L)
                else:
                    substring_turple=(len(buff)-start,L, "")
            list_of_turples.append(substring_turple)
            if(L>0):
                i+=L
            else:
                i+=1
            

    if(mode==1):    #bytes
        if(k>0):        #left turple
            data2.append(int('0b'+bin(k)[2:],2))
            for j in list_of_turples:
                if(j[0]>127):                            #takes 2 bytes  
                    y=j[0].to_bytes(2, "big")
                    data2.append(int.from_bytes(y[0:1], byteorder="big"))
                    data2.append(int.from_bytes(y[1:2], byteorder="big"))
                    dt.append(int.from_bytes(y[0:1], byteorder="big"))
                    dt.append(int.from_bytes(y[1:2], byteorder="big"))
                else:                                       #takes 1 byte
                    data2.append(int('0b'+bin(j[0]|128)[2:],2))
                if(j[1]>127):                              
                    y=j[0].to_bytes(2, "big")
                    data2.append(int.from_bytes(y[0:1], byteorder="big"))
                    data2.append(int.from_bytes(y[1:2], byteorder="big"))
                else:
                    data2.append(int('0b'+bin(j[1]|128)[2:],2))
        else:       #left single
            data2.append(int('0b'+bin(q|128)[2:],2))
            for j in data3:
                data2.append(j)
    
    else:       #normal     не используется
        for i in list_of_turples:
            if(i[1]>0):
                data2+=str(i[0])+','+str(i[1])+','
            else:
                data2+=str(i[0])+','+str(i[1])+','+i[2]+','
    
    file2.write(data2)
    file.close()
    file2.close()


















def decode_LZ77():                  #decode LZ77
    #print("\nchoose mode:\n1 - with bytes\n2 - normal\n")
    #mode=ask(1,2)
    mode=1
    print("\nchoose open:\n1 - out_LZ77.txt\n2 - other\n")
    f2=ask(1,2)
    if(f2==1):
        name="out_LZ77.txt"
    elif(f2==2):
        print("\nenter name\n")
        name=input()
    
    print("\nchoose out:\n1 - back_LZ77.txt\n2 - other\n")
    f2=ask(1,2)
    if(f2==1):
        name2="back_LZ77.txt"
    elif(f2==2):
        print("\nenter name\n")
        name2=input()
        
    file=open(name, "rb")
    
    file2=open(name2, "wb")
   
    
    data=file.read()
    #if(b1):
    data2=bytearray()
    #else:
        #data2=""

    
    i=0
    if(mode==1):        #with bytes
        while(i<len(data)):
            if((data[i]>>7) & 1 == 0):       #turple
                k=data[i]
                i+=1
                for j in range(k):
                    if((data[i]>>7) &1 == 1):       #takes 1 byte
                        shift=data[i]&127
                        i+=1
                    else:       #takes 2 bytes
                        shift=data[i]<<8
                        i+=1
                        shift+=data[i]
                        i+=1
                        
                    if((data[i]>>7) &1 == 1):      
                        L=data[i]&127
                    else:    
                        L=data[i]<<8
                        i+=1
                        L+=data[i]
                    dt=data2.copy()
                    p=1
                    while(True):
                        data2.append(dt[-1-shift+p])
                        yy=dt[-1-shift+p]
                        p+=1
                        if(p>L):
                            break
                    i+=1
                
            else:           #single
                k=data[i]&127
                i+=1
                for j in range(k):               
                    data2.append(data[i])
                    i+=1
                    

    else:   #normal     не используется
        A=[0,0]
        k=0
        while(i<len(data)):
            sr=""
            while(i<len(data) and data[i]!=(',')):
                  sr+=data[i]
                  i+=1            
            A[k]=int(sr)
            k+=1
            i+=1
            if(k==2):
                if(A[1]>0):
                    data2+=data2[-1-A[0]+1:-1-A[0]+A[1]]
                    #dt=data2.copy()
                    #p=1
                    #while(True):
                        #data2.append(dt[-1-A[0]+p])
                        #p+=1
                        #if(p>A[1]):
                           #break
                else:
                    data2+=data[i]
                    i+=2
                    #while(i<len(data) and data[i]!=ord(',')):
                        #data2.append(data[i])
                        #i+=1
                    #i+=1
                k=0
                    
           


    file2.write(data2)
    file.close()
    file2.close()


























from PIL import Image           #start
from io import BytesIO
import numpy as np
from decimal import Decimal
import math



f=0
f2=0
p=False
sign=0
while(True):        #main cycle    
    print("\nchoose action:\n1 - RLE\n2 - BWT\n3 - work with Image\n4 - Move-to-front\n5 - Arithmetic coding\n6 - Huffman\n7 - suffix and entropy\n8 - LZ77\n9 - exit program\n")   #main options
    f = ask(1,9)
    print("")

    if (f==1):      #RLE
        print("choose action:\n1 - compress RLE\n2 - decompress RLE\n3 - exit menu\n")    
        f2=ask(1,3)
        
        if (f2==1):     #compress
            compress()    
           
        elif(f2==2):        #decompress
            decompress() 

            



    elif (f==2):        #BWT
        print("choose action:\n1 - use BWT\n2 - decode BWT\n3 - average length\n4 - exit menu\n")
        f2=ask(1,4)
        

        if(f2==1):      #use
            print("\ninput block size\n")   
            N = ask_block()
                       
            p = True
            print("\nchoose version:\n1 - use index\n2 - use sign $ (or bytes)\n")  
            sign = ask(1,2)
            if(sign==1):
                sign=False
            else:
                sign=True
            useBWT(N, sign)
        



        elif(f2==2):        #decode
            if (sign==0):
                print("\nchoose mode:\n1 - use index (old)\n2 - use sign $ (or bytes)\n")  
                sign = ask(1,2)                                        

            if(p==False):
                print("\ninput block size\n")   
                N = ask_block()
                p = True
                
            print("\nchoose version\n1 - basic (old)\n2 - permutations (only with sign or bytes)\n")
            f2=ask(1,2)
            if(f2==1):
                unBWT(N, sign)
            else:
                unBWT_permutation(N)


        elif(f2==3):       #average length
            print("choose file:\n1 - out_BWT.txt\n2 - other\n")
            f2 = ask(1,2)                   
            name ="out_BWT.txt"              
            if (f2==2):
                print("enter name\n")
                name=input()
                
            average_length(name)

                        
                    
                




    

    elif(f==3):         #work with image         
        print("\nchoose Image:\n1 - white_and_black_bin.png\n2 - grayscale.jpeg\n3 - color.jpeg\n4 - other\n") #choose image
        im = ask(1,4)
        
        if (im==1):
            filename="white_and_black_bin.png"
        elif(im==2):
            filename="grayscale.jpeg"
        elif(im==3):
            filename="color.jpeg"
        elif(im==4):
            print("\ninput name\n")
            filename = input()
        
        with Image.open(filename) as img:
            img.load()
       
        im=0
        while(True):
            print("\nchoose action:\n1 - show\n2 - change size\n3 - save Image\n4 - work with raw\n5 - exit\n")       #choose action
            im = ask(1,5)
            
            if (im==1):         #show image and it's info
                while(True):        
                    print("\nchoose action:\n1 - show Image\n2 - show mode\n3 - show size\n4 - show format\n5 - show bands\n6 - exit\n")
                    im = ask(1,6)
                 
                    if(im==1):
                        img.show()            
                    elif(im==2):
                        print(img.mode)                            
                    elif(im==3):
                        print(img.size)               
                    elif(im==4):
                        print(img.format)               
                    elif(im==5):
                        print(img.getbands())
                    elif(im==6):
                        break


             
            elif(im==2):        #change size
                print("\ninput new width\n")
                width = ask_block()
                print("\ninput new hight\n")
                hight = ask_block()
                img=img.resize((width,hight))
                

            elif(im==3):        #save image
                print("\ninput name\n")
                name = input()
                img.save(name)
            

            elif(im==4):        #work with raw
                img=RAW(img)
                

            elif(im==5):        #exit menu
                break
            
             
                





                
    elif(f==4):         #Move-to-front
        print("\nchoose action:\n1 - use Move-to-front\n2 - decode Move-to-front\n3 - exit menu\n")
        f2=ask(1,3)
        if(f2==1):
            Move_to_front()
        elif(f2==2):
            decodeMtF()










    elif(f==5):         #Arithmetic coding
        print("choose action:\n1 - use arithmetic coding\n2 - decode arithmetic coding\n3 - exit menu\n")
        f2=ask(1,3)
        if(f2==1):
            arithmetic()
        elif(f2==2):
            decode_arithmetic()



  
  
            

             #Huffman

    elif(f==6):
        print("\nchoose action\n1 - use Huffman coding\n2 - decode Huffman coding\n3 - canonical codes\n4 - exit menu\n")          
        f2=ask(1,4)
        
        if(f2==1):
            Huffman()
            
        elif(f2==2):
            decode_Huffman()
            
        elif(f2==3):
            print("\nchoose action\n1 - canonical from normal\n2 - canonical from length\n")
            f2=ask(1,2)
            if(f2==1):
                canonical_codes(False)
            else:
                canonical_codes(True)








    elif(f==7):     #suffix
        print("\nchoose action:\n1 - make basic suffix array\n2 - last column of BWT\n3 - S and L\n4 - entropy\n5 - exit menu\n")         #other 
        f2 = ask(1,4)
        
        if(f2==1):
            basic_suffix("in_basic_suffix.txt", True)
            
        elif(f2==2):
            suffix_column(basic_suffix("in_suffix_column.txt", False))
            
        elif(f2==3):
            S_and_L()
            
        elif(f2==4):
            entropy()







    elif(f==8):     #LZ77
        print("\nchoose action:\n1 - use LZ77\n2 - decode LZ77\n3 - exit menu\n")         #other 
        f2 = ask(1,3)
        
        if(f2==1):
            LZ77()
            
        elif(f2==2):
            decode_LZ77()
            


    elif(f==9):     #exit program       
        break
    