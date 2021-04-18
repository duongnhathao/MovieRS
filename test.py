import pandas as pd
import constant
import json
from mlxtend.preprocessing import TransactionEncoder
import csv
import unicodecsv
from mlxtend.frequent_patterns import apriori, fpmax, fpgrowth
import os

def show_input_table(df):
    print("<div class='d-flex justify-content-center py-5'>")
    print("<div class='title-table-input'>Data import from file after format")
    print("</div>")
    print("</div>")
    print("<div class='container'>")
    print("<div class='table-responsive table-detail'>")
    print("<table class='table' id='table-detail'>")
    print("<thead class='thead-light'>")
    print("<tr>")
    print("<th scope='col'></th>")
    array = []
    for x in df.columns:
        print("<th scope='col'>")
        print(x)
        array.append(x)
        print("</th>")
    with open('json/product.json', 'w+') as f:
        json.dump(array, f)
    print("<tbody>")
    for x in range(len(df)):
        print('<tr>')
        print('<th scope="row">',x,"</td>")
        for j in df.iloc[x]:
            print("<td>")
            print(j,end="</td>")
        print('</tr>')
    print("</tbody>")
    print("</table>")
    print("</div>")
    print("</div>")
    return 0


def str_append(s, n):
    output = ''
    i = 0
    while i < n:
        output += s
        i = i + 1
    return output

def show_frequent_itemsets(df):
    frequent_itemsets = fpmax(df, min_support=constant.Min, use_colnames=True)
    print("<div class='d-flex justify-content-center py-5'>")
    s = "<div class='title-table-input'>Data frequent itemsets with Min Support : "+ str(constant.Min)
    print(s)
    print("</div>")
    print("</div>")
    print("<div class='container'>")
    print("<div class='table-responsive table-detail'>")
    print("<table class='table' id='table-result'>")
    print("<thead class='thead-light'>")
    print("<tr>")
    print("<th scope='col'></th>")
    for x in frequent_itemsets.columns:
        print("<th scope='col'>")
        print(x)
        print("</th>")
    print("<tbody>")
    itemset_json = []
    for x in range(len(frequent_itemsets)):
        print('<tr>')
        print('<th scope="row">',x,"</td>")
        for j in frequent_itemsets.iloc[x]:
            if(type(j)  is frozenset):
                print('<td>(')
                if(len(list(frequent_itemsets.iloc[x]["itemsets"]))>1):
                    sets=frequent_itemsets.iloc[x]
                    a =[]
                    a.append({"Support":sets["support"]})
                    a.append(list(sets["itemsets"]))
                    itemset_json.append({"itemsets":a})

                print(*frequent_itemsets.iloc[x]["itemsets"], sep=',')
                print(')</td>')
            else:
                print("<td>")
                print(j,end="</td>")
        print('</tr>')
    with open('json/itemset.json', 'w+') as f:
            json.dump(itemset_json, f)
    print("</tbody>")
    print("</table>")
    print("</div>")
    print("</div>")
    return 0




def print_data_input_information(df,df2):
    print("<div class='container py-5 print_data_input_information'>")
    print("<ul class='list-group'>")

    #Title
    print("<li class='list-group-item custom-list-group list-group-item-success title-ul' >")
    print("<div class='title-data-information '>Input detail </div>")
    print("<div class='upload-button'><a href='javascript:;' class='btn btn-success ' data-toggle='modal' data-target='#modalSettingForm'><i class='fas fa-cog'></i></a></div>")
    print("</li>")

    #Filename
    print("<li class='list-group-item custom-list-group list-group-item-white'>")
    print("<div class='title-data-information'>File Name: </div>")
    print(constant.File_name)
    print("</li>")

    #Row total
    print("<li class='list-group-item custom-list-group list-group-item-white' >")
    print("<div class='title-data-information'>Row total: </div>")
    print(len(df2))
    print("</li>")

    #Row use
    print("<li class='list-group-item custom-list-group list-group-item-white' >")
    print("<div class='title-data-information'>Row limit to use: </div>")
    print(constant.limit_row)
    print("</li>")


    #Min support
    print("<li class='list-group-item custom-list-group list-group-item-white' >")
    print("<div class='title-data-information'>Min support: </div>")
    print(constant.Min)
    print("</li>")



    print("</ul>")
    print("</div>")






def main1():
    dir = str(constant.direct)+"/"+str(constant.File_name)

    with open(dir, newline='') as csvfile:
        data = list(csv.reader(csvfile))

        dataset = [['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
               ['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
               ['Milk', 'Apple', 'Kidney Beans', 'Eggs'],
               ['Milk', 'Unicorn', 'Corn', 'Kidney Beans', 'Yogurt'],
               ['Corn', 'Onion', 'Onion', 'Kidney Beans', 'Ice cream', 'Eggs']]
    count = 0
    for i in data:
      i = [x for x in i if x != '']
      data[count] =  i
      count +=1
    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)

    df2 = pd.DataFrame(te_ary, columns=te.columns_)
    DF2_LEN = len(df2)
    if(constant.limit_row!=''or constant.limit_row!=None):
        df = df2.head(constant.limit_row)
    else:
        df= df2


    print("<div class='row'>")
    print("<div class='col-6'>")
    show_input_table(df)
    print_data_input_information(df,df2)
    print("</div>")

    print("<div class='col-6'>")
    show_frequent_itemsets(df)
    show_setting()
    print("</div>")

    print("</div>")

def show_setting():
    print("<div class='container py-5 print_data_input_information'>")
    print("<div class='row'>")

#list file name
    print("<div class='col-6'>")
    arr = os.listdir('./file_upload')
    print("<ul class='list-group' id='list-group-filename'>")
    #title
    print("<li class='list-group-item sticky-top custom-list-group list-group-item-success title-ul' >")
    print("<div class='title-data-information '>Upload File Folder <span class='badge badge-secondary'>")
    print(len(arr))
    print("</span></div>")
    print("<div class='upload-button'><a href='javascript:;' class='btn btn-success' data-toggle='modal' data-target='#modalLoginForm'><i class='fa fa-upload' data-toggle='tooltip' data-placement='bottom' title='Upload file to folder' aria-hidden='true'></i></a></div>")

    print("</li>")

    #filename - item
    for i in arr:
        print("<li class='list-group-item custom-list-group list-group-item-white title-ul' >")
        print("<div class=''>")
        print(i)
        print("</div>")
        print("</li>")
    print("</div>")
    print("<div class='col-6'>")

    print("<div class='row'>")

    print("</div>")

    print("<div class='row'>")
    print("</div>")


    print("</div>")



    print("</div>")
    print("</div>")

if __name__ == '__main__':
    main1()


