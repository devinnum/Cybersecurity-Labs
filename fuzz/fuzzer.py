# Fuzzer skeleton code

import args, urllib.request

def fuzz(args):
    """Fuzz a target URL with the command-line arguments specified by ``args``."""
    # your code here...
    meth = (args.method).upper()
    h = args.headers
    hd = {}
    for i in h:
        j = i.split(":")
        hd[j[0]] = j[1]
    d = None
    if args.data != None:
        d = bytes(args.data, "utf-8")
    mc = args.match_codes
    c = []
    with open(args.wordlist) as f:
        while True:
            x = f.readline().strip()
            if x == '':
                break       
            c.append(x)
    urls = []
    for i in c:
        urls.append(args.url.replace("FUZZ", i))
    for i in urls: 
        try:
            x = urllib.request.urlopen(urllib.request.Request(i, method=meth, headers=hd, data=d)).status
            for j in mc:
                if x == j:
                    print(str(x) + " " + i)
        except:
            pass
    for i in args.extensions:
        for j in urls:
            try:
                x = urllib.request.urlopen(urllib.request.Request(j + i, method=meth, headers=hd, data=d)).status
                for y in mc:
                    if x == y:
                        print(str(x) + " " + j + i)
            except:
                pass


# do not modify this!
if __name__ == "__main__":
    arguments = args.parse_args()
    fuzz(arguments)
