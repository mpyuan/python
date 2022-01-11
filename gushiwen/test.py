import requests,time
from threading import Thread
import json


global_list = []
def parse_dict_txt():

    with open('1.txt','r',encoding='utf-8') as f:
        data = f.readlines()

        for line in data:
            line=line.strip('\n')
            global_list.append(parse_list(line,0).pop())

    f.close()
    with open('2.txt', 'w', encoding='utf-8') as f1:
        json.dump(parse_unique(global_list),f1,ensure_ascii=False)
    f1.close()





def parse_dict(line,n):
    if len(line) <= n:
        return line
    return {line[n]:parse_dict(line,n+1)}
def parse_unique(list1):

    for i in range(0,len(list1)):

        for j in range(i+1, len(list1)):
            pass
            try:

                if list1[i].get('name')==list1[j].get('name'):
                    list1[i].update({'child':parse_unique(list1[i].get('child')+list1[j].get('child'))})
                    del list1[j]
            except Exception as e:
                pass



    return list1




def parse_list(line,n):
    if len(line) <= n:
        return [line]
    return [{'name':line[n],'child':parse_list(line,n+1)}]



if __name__ == '__main__':
    pass
    parse_dict_txt()
    # print(global_list)