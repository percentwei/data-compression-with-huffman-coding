class Node:
    def __init__(self,freq):
        self.left = None
        self.right = None
        self.father = None
        self.freq = freq
    def isLeft(self):
        return self.father.left == self
    
#create nodes
def createNodes(freqs):
    return [Node(freq) for freq in freqs]

#create Huffman-Tree
def createHuffmanTree(nodes):
    queue = nodes[:]
    while len(queue) > 1:
        queue.sort(key=lambda item:item.freq)
        node_left = queue.pop(0)
        node_right = queue.pop(0)
        node_father = Node(node_left.freq + node_right.freq)
        node_father.left = node_left
        node_father.right = node_right
        node_left.father = node_father
        node_right.father = node_father
        queue.append(node_father)
    queue[0].father = None
    return queue[0]

#Huffman
def huffmanEncoding(nodes,root):
    codes = [''] * len(nodes)
    for i in range(len(nodes)):
        node_tmp = nodes[i]
        while node_tmp != root:
            if node_tmp.isLeft():
                codes[i] = '0' + codes[i]
            else:
                codes[i] = '1' + codes[i]
            node_tmp = node_tmp.father
    return codes
    
# The previous code is reference from https://www.itread01.com/content/1546575863.html

def frequency_table(codes):
    W_file=open('frequency.txt','w')
    for i in range(256):
        W_file.write(str(codes[i])+'\n')
    W_file.close()  

def compression(filename):
    count=[0 for i in range(256)]
    I_file=open(filename,"rb")
    O_file=open("output.txt","wb")
    text=I_file.read()
    for i in text:
        count[i]+=1

    nodes = createNodes([item for item in count])
    root = createHuffmanTree(nodes)
    codes = huffmanEncoding(nodes,root)
    for i in range(256):
        codes[i]='1'+codes[i]
    frequency_table(codes)
    
    encoder=""
    for i in text:
        encoder+=codes[i]
    if len(encoder)%8 !=0:
        num=(8-len(encoder)%8)
        encoder+='0'*num
    O_file.write(bytearray([int(encoder[i:i + 8],2)for i in range(0, len(encoder), 8)]))

    print("Original bytes =",len(text))
    print("Compressed bytes =",len(encoder)/8)
    print("Saved",round(len(encoder)/8/len(text)*100,2),"% of memory")
    I_file.close()
    O_file.close()

def decompression(filename):
    F_binary=[]
    I_file=open(filename,"rb")
    F_file=open('frequency.txt','r')
    O_file=open("output.txt","wb")
    
    for line in F_file.readlines():
        F_binary.append(line[:-1])
    text=""    
    for i in I_file.read():
        text+='0'*(8-len(bin(i)[2:]))+bin(i)[2:]
    tmp=""
    for i in text:
        if tmp+i in F_binary:
            O_file.write(bytes([int(F_binary.index(tmp+i))]))
            tmp=""
        else:
            tmp+=i
    
    I_file.close()
    F_file.close()
    O_file.close()

if __name__ == '__main__':
    filename=input("Type the name of the file to process:\n")
    enter=input("Type 1 to compress and 2 to decompress:\n")
    if(enter=='1'):
        compression(filename)
    else:
        decompression(filename)
    
