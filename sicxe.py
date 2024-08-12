file = open("inSICXE.txt", "r")



label = []
inst = []
ref = []
loc= []
objectcode = []

for line in file:
    
   
    x = line.split(' ')
    if len(x)==3:
        label.append(x[0])
        inst.append(x[1])
        ref.append(x[2])
      

    elif len(x)==2:
        label.append("     ")
        inst.append(x[0])
        ref.append(x[1])

    elif len(x)==1:
        label.append("     ")
        inst.append(x[0])
        ref.append("")
      


def passone():
    count = int(ref[0])
    loc.append(count)
    loc.append(count)
    for i in range(1, len(inst)):
        count = int(loc[-1])
        if '+' in inst[i]:
            loc.append(count+4)
        elif '+' not in inst[i]:
            if inst[i] == 'FIX' or inst[i] == 'FLOAT' or inst[i] == 'HIO' or inst[i] == 'NORM' or inst[i] == 'SIO' or inst[i] == 'TIO':
                loc.append(count+1)
            elif inst[i] == 'ADDR' or inst[i] == 'CLEAR' or inst[i] == 'COMPR' or inst[i] == 'DIVR' or inst[i] == 'MULR' or inst[i] == 'RMO' or inst[i] == 'SHIFTL' or inst[i] == 'SHIFTR' or inst[i] == 'SUBR' or inst[i] == 'SVC' or inst[i] == 'TIXER':
                loc.append(count+2)
            elif inst[i] == 'BASE':
                loc.append(count)
                print(count)
                
                
            elif inst[i] == 'resw':
                tot = int(ref[i]) *3
                tot3 = hex(tot)
                loc.append(count + tot3)
            elif inst[i] == 'resb':
                tot = int(ref[i], base=16)
                loc.append(count+tot)
            elif inst[i] == 'byte':
                num = ref[i]
                if num[0] == 'C':
                    size = (len(num) - 3)
                    loc.append(count + size)
                elif num[0] == 'x':
                    size = (len(num-3))/2
                    loc.append(count + size)
            elif inst[i] == 'END':
                break
            else:
                loc.append(count+3)
    
    for x in range(len(loc)):
         loc[x] = hex(int(loc[x])).replace('0x', '')
    length = int(loc[-1], 16) - int(loc[0], 16)
    print("Program Length = ", hex(length).replace('0x', ''))
    print("pc", "  " , "label" , "  " , "inst" , "  " , "ref")
    print("\n")
    for i in range(len(inst)):
        print("" if i >=len(loc) else loc[i], "|" ,"" if i >=len(label) else label[i] , "|" , "" if i >=len(inst) else inst[i] , "|" , "" if i >=len(ref) else ref[i] )
        

opcode = [["FIX", "1", "C4"] ,["FLOAT", "1", "C0"] ,["HIO", "1", "F4"],["NORM", "1", "C8"],["SIO", "1", "F0"],["TIO", "1", "F8"],["ADDR", "2", "90"],["CLEAR", "2", "B4"],["COMPR", "2", "A0"],["DIVR", "2", "9C"],["MULR", "2", "98"],["RMO", "2", "AC"],["SHIFTL", "2", "A4"],["SHIFTR", "2", "A8"],["SUBR", "2", "94"],["SVC", "2", "B0"],["TIXR", "2", "B8"],["ADD", "3", "18"],["ADDF", "3", "58"],["AND", "3", "40"],["COMP", "3", "28"],["COMPF", "3", "88"],["DIV", "3", "24"],["DIVF", "3", "64"],["J", "3", "3C"],["JEQ", "3", "30"],["JGT", "3", "34"],["JLT", "3", "38"],["JSUB", "3", "48"],["LDA", "3", "00"],["LDB", "3", "68"],["LDCH", "3", "50"],["LDF", "3", "70"],["LDL", "3", "08"],["LDS", "3", "6C"],["LDT", "3", "74"],["LDX", "3", "04"],["LPS", "3", "D0"],["MUL", "3", "20"],["MULF", "3", "60"],["OR", "3", "44"],["RD", "3", "D8"],["RSUB", "3", "4C"],["SSK", "3", "EC"],["STA", "3", "0C"],["STB", "3", "78"],["STCH", "3", "54"],["STF", "3", "80"],["STI", "3", "D4"],["STL", "3", "14"],["STS", "3", "7C"],["STSW", "3", "E8"],["STT", "3", "84"],["STX", "3", "10"],["SUB", "3", "1C"],["SUBF", "3", "5C"],["TD", "3", "E0"],["TIX", "3", "2C"],["WD", "3", "DC"]]    
    
def passtwo():
    n=0
    i=0
    x=0
    b=0
    p=0
    e=0
    for i in range(len(inst)):
           if inst[i] == 'START' or inst[i] == 'END':
            objectcode.append('**')
           for j in opcode:
             if inst[i] in j:
                  obj= (bin(int (i[2]),16)).replace("0b"," ")
                
                  obj=obj[0:-2]
                  e=0
                  if "#" in ref[i]:
                       n=0
                       i=1
                  elif '@' in ref[i]:
                        n =0
                        i= 1   
    
                  elif ',X' in ref[i]:
                      n = 0
                      i = 0
                      x = 1
                  elif '#' not in ref[i] and '@' not in ref[i] and ',x' not in ref[i]:
                        n = 1
                        i= 1
           index = 0    
           for z in label:
             if ref[i] == z:
                        index = label.index(x)
           TA=int(loc[index], 16)
           disp=TA -loc
           if int(disp<2048 ,disp>-2048):
            p=1
            b=0
           else:
            p=0
            b=1
           part1 =hex( obj +str(n+i+x+b+p+e)+ bin(disp).replace("0b" ,""))
           objectcode.append(part1.replace('0x', ''))
           if "+" in inst[i]:
               for j in opcode:
                if inst[i] in j:
                  obj=  (bin(int (i[2]),16).replace("0b"," "))
                  obj=obj[0:-2]
                  e=1
                if "#" in ref[i]:
                       n=0
                       i=1
                elif '@' in ref[i]:
                        n =0
                        i= 1   
    
                elif ',X' in ref[i]:
                      n = 0
                      i = 0
                      x = 1
                elif '#' not in ref[i] and '@' not in ref[i] and ',x' not in ref[i]:
                        n = 1
                        i= 1
                for z in label:
                    if ref[i] == z:
                        index = label.index(x)
                TA=int(loc[index], 16)
                disp=TA -loc
                if int(disp<2048 ,disp>-2048):
                    p=1
                    b=0
                else:
                     p=0
                     b=1       
                part2 =hex( obj +str(n+i+x+b+p+e)+ bin(disp).replace("0b ","" ))
                objectcode.append(part2.replace('0x', ''))
               
           if inst[i] == 'ADDR' or inst[i] == 'CLEAR' or inst[i] == 'COMPR' or inst[i] == 'DIVR' or inst[i] == 'MULR' or inst[i] == 'RMO' or inst[i] == 'SHIFTL' or inst[i] == 'SHIFTR' or inst[i] == 'SUBR' or inst[i] == 'SVC' or inst[i] == 'TIXER':
            for j in opcode:
              if inst[i] in j:
                  obj= (bin(int (i[2]),16)).replace("0b"," ")
                  obj=obj[0:-2]
                  reg1=0
                  reg2=0
                  if "A" == ref[i] :
                      reg1=0
                      reg2=0
                  if "X" == ref[i] :  
                      
                     reg1=1
                     reg2=0
                  if "B" == ref[i] :  
                      
                     reg1=4
                     reg2=0
                  if "S" == ref[i] :  
                      
                     reg1=5
                     reg2=0
                  if "T" == ref[i] :  
                     reg1=6
                     reg2=0 
                  if "F" == ref[i] :  
                     reg1=7
                     reg2=0 
    
           part3=obj+reg1+reg2
           objectcode.append(part3)
           if inst[i] == 'FIX' or inst[i] == 'FLOAT' or inst[i] == 'HIO' or inst[i] == 'NORM' or inst[i] == 'SIO' or inst[i] == 'TIO':
                for J in opcode:
                    if inst[i] in J:
                        objectcode.append(J[2])                              
           elif inst[i] == "BASE":
                objectcode.append("**")
           elif inst[i] == 'BYTE':
                if"x" in ref[i]:
                    objectcode.append(ref[2:-1])
                elif "c"in inst[i]:
                    ascii=ascii(ref[i])
                    objectcode.append(ascii)
                elif inst[i] == 'WORD':
                 objectcode.append (hex(int(ref[i])).replace('0x', ''))
                elif inst[i] == 'RESW' or inst[i] == 'RESB':
                   objectcode.append('**')    
def HTE(): 
 H= str(label[0]+00+ref[0]+program_length)
 T=str(00+ref[0]+objectcode[9]+objectcode[9]-objectcode[0])
 E=ref[0]


passone()
passtwo()







    
    