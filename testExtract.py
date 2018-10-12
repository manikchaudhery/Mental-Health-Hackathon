# from extractEmail import extract
# from dateutil.parser import parse
from exportToExcel import exportToExcel
import base64
import os
import time

def extractEmail(fname):
    with open(fname, "rb") as f:
        lines = f.readlines()
        data = {}
        data["Date"] = lines[0][6:].decode("utf-8")[:-2]
        # data["datetime"] = parse(data["Date"])
        data["From"] = lines[4][6:].decode("utf-8")[:-2]
        data["To"] = lines[5][4:].decode("utf-8")[:-2]

        # try:
        index = 10
        for i in range(6, len(lines)):
            if lines[i].startswith(b"--MIME_Boundary"):
                index = i
                break
        body = []
        for i in lines[index+5:]:
            if i.startswith(b"--MIME_Boundary"): break
            body.append(i.decode("utf-8")[:-2])
        # body = [s.decode("utf-8")[:-2] for s in lines[14:-1]]
        body = "".join(body)
        body = base64.b64decode(body).decode("utf-8")
        # except Exception:
        #     print(fname)
            # print(body)
            # raise
        return data, body

def parseEmail(args):
    data, body = args
    # print(body)
    lines = body.split("\n")
    #"Nickname",
    required = ["Gender", "Age", "Province", "Community", "Community Other"]
    for i in range(len(lines)):
        if lines[i][:len(required[0])] == required[0]:
            for j in range(len(required)):
                data[required[j]] = lines[i+j][len(required[j])+2:]
            break
    return data

def speed_test():

    start = time.time()
    for i in range(1000):
        # extractEmail("./20160101000207617_1_p2p.eml")
        parseEmail(extractEmail("./Test-Emails/20160101000207617_1_p2p.eml"))
        # extractEmail("./20170101000452297_1_p2p.eml")
        parseEmail(extractEmail("./Test-Emails/20170101000452297_1_p2p.eml"))
    end = time.time()
    print((end-start)*1000)

def processEmails(mini=False):
    start = time.time()
    datalist = []
    directories = os.listdir("../Data/skypearchiving.kidshelp.ca")
    directories = [d for d in directories if d[0] != "."]
    for d in directories:
        subdirectories = os.listdir("../Data/skypearchiving.kidshelp.ca/"+d)
        if mini:
            subdirectories = ["2017"]
        for sd in subdirectories:
            files = os.listdir("../Data/skypearchiving.kidshelp.ca/"+d+"/"+sd)
            for file in files:
                datalist.append(parseEmail(extractEmail("../Data/skypearchiving.kidshelp.ca/"+d+"/"+sd+"/"+file)))

    exportToExcel(datalist)
    end = time.time()
    print(end-start)


# processEmails()
print(parseEmail(extractEmail("./Test-Emails/20160101000207617_1_p2p.eml")))
# speed_test()