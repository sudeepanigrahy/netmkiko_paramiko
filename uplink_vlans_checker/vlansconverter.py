def converter(string, listt):
    if "-" in string and "," not in string:
        l = string.split("-")
        ret_list = [x for x in listt if int(x) in range(int(l[0]),int(l[-1])+1)]
        ret_list.sort()
        return ret_list
    elif "-" in string and "," in string:
        l = string.split(",")
        l = [z.strip() for z in l]
        v=[]
        dash=[]
        for i in l:
            if "-" in i:
                xx = i.split("-")
                v.extend(xx)
                dash.append(i)
                xxx = (int(xx[-1]) - int(xx[0]))-1
                if xxx==0:
                    continue
                else:
                    for j in range(xxx):
                        v.append(str(int(xx[0])+int(j)+1))
            else: continue
        [l.append(x) for x in v]
        [l.remove(x) for x in dash] 
        ret_list = [x for x in listt if x in l]
        ret_list.sort()
        return ret_list
    elif "," not in string and "-" not in string:
        l = []
        l.append(string)
        ret_list = [x for x in listt if x in l]
        return ret_list
    elif "," in string:
        l = string.split(",")
        l = [z.strip() for z in l]
        ret_list = [x for x in listt if x in l]
        ret_list.sort()
        return ret_list
    else: return ''