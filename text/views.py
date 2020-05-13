from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def index(request):
    return render(request, "index.html")

# Generate matrix function
def matrix(x,y,initial):
    return [[initial for i in range(x)] for j in range(y)]

"""# Location of symbol finder funtion"""
def locindex(my_matrix,c): #get location of each character
    loc=list()
    for i ,j in enumerate(my_matrix):
        for k,l in enumerate(j):
            if c==l:
                loc.append(i)
                loc.append(k)
                return loc

"""# Playfair key funtion"""
def playfair_key(key1):
    result=list()
    for c in key1: #storing key
        if c not in result:
            result.append(c)
    for i in range(45,126): #storing other character
        if chr(i) not in result:
            result.append(chr(i))
    k=0
    my_matrix=matrix(9,9,0) #initialize matrix
    for i in range(0,9): #making matrix
        for j in range(0,9):
            #print(result[k])
            my_matrix[i][j]=result[k]
            k+=1

    return my_matrix

"""# Playfair Encrypt"""
def encrypt(key1,msg):  #Encryption
    my_matrix = playfair_key(key1)
    #global msg
    i=0
    for s in range(0,len(msg)+1,2):
        if s<len(msg)-1:
            if msg[s]==msg[s+1]:
                msg=msg[:s+1]+'X'+msg[s+1:]
    if len(msg)%2!=0:
        msg=msg[:]+'X'
    #global cipher
    cipher=""
    while i<len(msg):
        loc=list()
        loc=locindex(my_matrix,msg[i])
        loc1=list()
        loc1=locindex(my_matrix,msg[i+1])
        if loc[1]==loc1[1]:
            cipher=cipher+ str("{}{}".format(my_matrix[(loc[0]+1)%9][loc[1]],my_matrix[(loc1[0]+1)%9][loc1[1]]))
        elif loc[0]==loc1[0]:
            cipher=cipher+ str("{}{}".format(my_matrix[loc[0]][(loc[1]+1)%9],my_matrix[loc1[0]][(loc1[1]+1)%9]))
        else:
            cipher=cipher+ str("{}{}".format(my_matrix[loc[0]][loc1[1]],my_matrix[loc1[0]][loc[1]]))
        i=i+2

    return cipher

"""# Playfair Decrypt"""
def decrypt(key1,msg):  #decryption
    my_matrix = playfair_key(key1)
    i=0
    #global plain
    plain=""
    while i<len(msg):
        loc=list()
        loc=locindex(my_matrix,msg[i])
        loc1=list()
        loc1=locindex(my_matrix,msg[i+1])
        if loc[1]==loc1[1]:
            plain=plain+str("{}{}".format(my_matrix[(loc[0]-1)%9][loc[1]],my_matrix[(loc1[0]-1)%9][loc1[1]]))
        elif loc[0]==loc1[0]:
            plain=plain+str("{}{}".format(my_matrix[loc[0]][(loc[1]-1)%9],my_matrix[loc1[0]][(loc1[1]-1)%9]))
        else:
            plain=plain+str("{}{}".format(my_matrix[loc[0]][loc1[1]],my_matrix[loc1[0]][loc[1]]))
        i=i+2

    if plain[len(msg)-1]=='X':
        return plain[:-1]
    else:
        return plain

"""# XOR encrypt decrypt funtion"""
def encryptDecrypt(inpString):

    return inpString

    # Define XOR key
    # Any character value will work
    xorKey = 'P';

    # calculate length of input string
    length = len(inpString);

    # perform XOR operation of key
    # with every caracter in string
    for i in range(length):
        inpString = (inpString[:i] + chr(ord(inpString[i]) ^ ord(xorKey)) + inpString[i + 1:]);
        #print(inpString[i], end = "");

    return inpString

#Encrypt message
def serve_request(request):
    key1=request.POST["key"]
    option = request.POST["option"]

    if option=="encrypt":
        msg = request.POST["message"]
        cipher = encrypt(key1,msg)
        c_cipher = encryptDecrypt(cipher)
        output = c_cipher

        return render(request, "output.html",{'output':output,'first':cipher,'input':msg})

    else:
        c_cipher = request.POST["message"]
        d_cipher = encryptDecrypt(c_cipher)
        real_msg = decrypt(key1,d_cipher)
        output = real_msg

        return render(request, "output.html",{'output':output,'first':d_cipher,'input':c_cipher})

