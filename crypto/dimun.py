from datetime import datetime
import hashlib
import binascii
import rsa
import sys
import os

# gets the hash of a file; from https://stackoverflow.com/a/44873382
def hashFile(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

# given an array of bytes, return a hex reprenstation of it
def bytesToString(data):
    return binascii.hexlify(data)

# given a hex reprensetation, convert it to an array of bytes
def stringToBytes(hexstr):
    return binascii.a2b_hex(hexstr)

# Load the wallet keys from a filename
def loadWallet(filename):
    with open(filename, mode='rb') as file:
        keydata = file.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)
    pubkey = rsa.PublicKey.load_pkcs1(keydata)
    return pubkey, privkey

# save the wallet to a file
def saveWallet(pubkey, privkey, filename):
    # Save the keys to a key format (outputs bytes)
    pubkeyBytes = pubkey.save_pkcs1(format='PEM')
    privkeyBytes = privkey.save_pkcs1(format='PEM')
    # Convert those bytes to strings to write to a file (gibberish, but a string...)
    pubkeyString = pubkeyBytes.decode('ascii')
    privkeyString = privkeyBytes.decode('ascii')
    # Write both keys to the wallet file
    with open(filename, 'w') as file:
        file.write(pubkeyString)
        file.write(privkeyString)
    return

def name():
    print("dimun")

def main():
    if sys.argv[1] == "name":
        name()
    if sys.argv[1] == "genesis":
        genesis()
    if sys.argv[1] == "generate":
        generate(sys.argv[2])
    if sys.argv[1] == "address":
        print(address(sys.argv[2]))
    if sys.argv[1] == "fund":
        fund(sys.argv[2], sys.argv[3], sys.argv[4])
    if sys.argv[1] == "transfer":
        transfer(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    if sys.argv[1] == "balance":
        print(balance(sys.argv[2]))
    if sys.argv[1] == "verify":
        verify(sys.argv[2], sys.argv[3])
    if sys.argv[1] == "mine":
        mine(sys.argv[2])
    if sys.argv[1] == "validate":
        validate()

def genesis():
    with open("block_0.txt","w") as f:
        f.write("      __________________\n"\
                "    .-'  \ _.-''-._ /  '-.\n"\
                "  .-/\   .'.      .'.   /\-.\n"\
                " _'/  \.'   '.  .'   './  \\'_\n"\
                ":======:======::======:======:\n"\
                " '. '.  \     ''     /  .' .'\n"\
                "   '. .  \   :  :   /  . .'\n"\
                "     '.'  \  '  '  /  '.'\n"\
                "       ':  \:    :/  :'\n"\
                "         '. \    / .'\n"\
                "           '.\  /.'\n"\
                "             '\/'")
    print("Genesis block created in 'block_0.txt'")

def generate(filename):
    (pubkey, privkey) = rsa.newkeys(1024)
    saveWallet(pubkey, privkey, filename)
    pubkeyBytes = pubkey.save_pkcs1(format='PEM')
    h = hashlib.sha256()
    h.update(pubkeyBytes)
    tag = h.hexdigest()[0:16]
    print("New wallet generated in '" + filename + "' with tag " + tag)

def address(filename):
    pubkey = loadWallet(filename)[0]
    pubkeyBytes = pubkey.save_pkcs1(format='PEM')
    h = hashlib.sha256()
    h.update(pubkeyBytes)
    return h.hexdigest()[0:16]

def tranline(sender, receiver, amount, time):
    if sender != "king":
        sender = str(address(sender))
    with open("mempool.txt","a") as f:
        f.write(sender + " transferred " + amount + " to " + receiver + " on " + time + "\n")

def transtate(sender, receiver, amount, time, filename, privkey=None):
    if sender != "king":
        sender = str(address(sender))
    with open(filename,"w") as f:
        f.write("From: " + sender + "\n")
        f.write("To: " + receiver + "\n")
        f.write("Amount: " + amount + "\n")
        f.write("Date: " + time + "\n")
    if privkey is not None:
        with open(filename, 'rb') as f:
            signature = rsa.sign(f, privkey, 'SHA-256')
        with open(filename, "a") as f:
            f.write(bytesToString(signature).decode('utf-8'))

def fund(receiver, amount, filename):
    time = str(datetime.now())
    transtate("king", receiver, amount, time, filename)
    print("Funded wallet " + receiver + " with " + amount + " dimun on " + time)

def transfer(sender, receiver, amount, filename):
    time = str(datetime.now())
    privkey = loadWallet(sender)[1]
    transtate(sender , receiver, amount, time, filename, privkey)
    print("Transferred " + amount + " from " + sender + " to " + receiver + " and the statement to " + filename + " on " + time)

def balance(filename):
    tag = filename
    block = 1
    count = 0
    while os.path.isfile("block_"+str(block)+".txt"):
        file = open("block_"+str(block)+".txt", "r")
        lines = file.readlines()
        for line in lines[1:-1]:
            values = line.split()
            if values[0] == tag:
                count -= int(values[2])
            if values[4] == tag:
                count += int(values[2])
        block += 1
    try:
        file = open("mempool.txt")
        lines = file.readlines()
        for line in lines:
            values = line.split()
            if values[0] == tag:
                count -= int(values[2])
            if values[4] == tag:
                count += int(values[2])
    except:
        pass

    return count

def verify(sender, statement):
    file = open(statement, "r")
    lines = file.readlines()
    with open("nosig.txt", "w") as f:
        for l in range(len(lines) - 1):
            f.write(lines[l])

    if address(sender) == lines[1].split()[1]:
        print("Any funding request (i.e., from king) is considered valid; written to mempool")
        tranline("king", lines[1].split()[1], lines[2].split()[1], (lines[3].split()[1] + " " + lines[3].split()[2]))
    
    else:
        with open("nosig.txt", "rb") as f:
            try:
                if rsa.verify(f, stringToBytes(lines[4]), loadWallet(sender)[0]) == "SHA-256" and int(lines[2].split()[1]) <= balance(address(sender)):
                    print("The transaction in file '" + statement + "' with wallet '" + sender + "' is valid, and was written to the mempool")
                    tranline(sender, lines[1].split()[1], lines[2].split()[1], (lines[3].split()[1] + " " + lines[3].split()[2]))
            
            except:
                pass

def mine(prefix):
    file = open("mempool.txt", "r")
    lines = file.readlines()
    block = 0
    while os.path.isfile("block_"+str(block)+".txt"):
        block += 1

    hash = int(prefix) * '1'
    nonce = 0
    while hash[0:int(prefix)] != int(prefix)*'0':
        nonce += 1
        with open("block_"+str(block)+".txt", "w") as f:
            f.write(hashFile("block_"+str(block - 1)+".txt") + "\n")
            for l in lines:
                f.write(l)
            f.write("nonce: " + str(nonce))
        hash = hashFile("block_"+str(block)+".txt")

    os.remove("mempool.txt")
    print("Mempool trasaction moved to block_"+str(block)+".txt and mined with difficulty " + str(prefix) + " and nonce " + str(nonce))

def validate():
    valid = True
    block = 1
    while os.path.isfile("block_"+str(block)+".txt"):
        file = open("block_"+str(block)+".txt", "r")
        lines = file.readlines()
        if lines[0].strip() != hashFile("block_"+str(block - 1)+".txt"):
            valid = False
        block += 1
    print(valid)

if __name__ == '__main__':
	main()
