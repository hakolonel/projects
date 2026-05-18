    def convertToBinary(num,size):
    num = int(num)
    size = int(size)
    binary = bin(num)
    binary = binary[2:]
    if len(binary)<size:
        for i in range (size-len(binary)):
            binary = '0'+binary
    return binary
def convertToNegative(binary,size):
    negative = ""
    binary = convertToBinary(binary,size)
    for bit in binary:
        if bit=='1':
            negative = negative+'0'
        elif bit == '0':
            negative = negative+'1'
        else:
            print("not a valid number")
    negative = int(negative,2)+1
    negative = convertToBinary(negative,size)
    return negative 
        
num = input("enter a number: ")
size = input("enter the how many bits: ")
print("the number in decimal: "+num)
print("binary form: " + convertToBinary(num,size))
print("negative binary form: " + convertToNegative(num,size))