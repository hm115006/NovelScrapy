# coding: utf-8
import types
def dictget(dict1,obj,default=None):
    for k,v in dict1.items():
        if k == obj:
            print(v)
        else:
            if type(v) is dict:
                re=dictget(v,obj)
                if re is not default:
                    print(re)


data2 ={ "chapter_1":{"chapter_name" : "第一章：穿越","chapter_content":"算了吧"},"chapters_2":{"two": "第二章退婚"},"chapter_content":"算了吧"}
a = "第一章：穿越"
data3 ={ "chapter_1":{"chapter_name" : a,"chapter_content":"算了吧"},"chapters_2":{"two": "第二章退婚"},"chapter_content":"算了吧"}

print(isinstance(data2, dict))
dictget(data3,'chapter_name')
dictget()
print('data3.chapter_1.one')