import pandas as pd
import csv

def write_csv(filename,data):
    """function to create and write into a csv file

    Args:
        filename (string): name to be given to file
        data (list): list of lists of strings etc
    """ 
    with open(filename, 'w',encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)



def iswebsite(l,outlist):
    """function to validate if website is working or not, possible outcomes- YES, MAYBE or NO.

    Args:
        l (list): list of websites to be checked
        outlist (string): name of file where output is to be stored, output includes:- '(link,statuscode,result)'

    Returns:
        list: returns list of links that are not working
    """
    import requests
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15","Accept-Language": "en-gb","Accept-Encoding":"br, gzip, deflate","Accept":"test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Referer":"http://www.google.com/"}
    cnt_work=0 #count of links working
    cnt_nt=0   #count of links not working
    cnt_total=len(l) #count of total no of links
    cnt=0  #counts no of iterations
    print(cnt_total)
    exli=[] #list of strings for outlist
    wnt_list=[] #list of URLs that dont work
    for i in l:
        #writes to file every 500 iterations so as to ensure logs
        if cnt%500==0:
            write_csv(outlist,exli)
        try:
            request = requests.get(i,headers=headers,verify=False)
            xyz=request.status_code
            print(xyz)
            if request.status_code == 200:
                print(cnt,'Web site exists')
                cnt_work+=1
                cnt+=1
                exli.append((i,xyz,"YES"))
            elif request.status_code == 403:
                print("forbidden")
                cnt+=1
                cnt_work +=1
                exli.append((i,xyz,"MAYBE"))
                
            elif request.status_code == 503:
                print("server not able to handle request")
                cnt+=1
                cnt_work+=1
                wnt_list.append((i,xyz))
                exli.append((i,xyz,"MAYBE"))
            
            elif request.status_code == 302 or request.status_code == 303 or request.status_code ==301:
                
                r=requests.get(i,headers=headers,verify=False)
                r1=r.url
                print(r1)
                req=requests.head(r1,headers=headers,verify=False)
                
                if req.status_code == 200:
                    print(cnt,'Web site exists(redirected)')
                    cnt_work+=1
                    cnt+=1
                    exli.append((i,xyz,"YES"))
                else:
                    print(cnt,'Web site does not exist(redirected)')
                    print("error",req.status_code)
                    wnt_list.append((i,req.status_code))
                    cnt_nt+=1
                    cnt+=1
                    exli.append((i,req.status_code,"MAYBE"))

                
                
            else:
                
                print(cnt,'Web site does not exist') 
                print(request.status_code)
                cnt_nt+=1
                wnt_list.append((i,xyz))
                cnt+=1
                exli.append((i,xyz,"MAYBE"))
                
        except:
            
            print(cnt,"error")
            cnt+=1
            exli.append((i,xyz,"MAYBE"))
    write_csv(outlist,exli)        
    if cnt_work+cnt_nt==cnt_total:
        w=True
    else:
        w=False
    print("\n working : ",cnt_work,"\n not working : ",cnt_nt,"\n total websites : ",cnt_total,"\n check sum :",w)
    return wnt_list



def batch_process(filename):
    """function to convert the output from iswebsite() function into a proper table format.
        Saves the new file by same name as input + 'processed' at the end in the same directory.

    Args:
        filename (string): name of file from which input is to be taken(outlist arg from iswebsite() function)
    """
    
    df=pd.read_csv(filename,header=None)
    
    df=df.transpose()
    
    
    link_list=[]
    status_code=[]
    work=[]
    success=[]

    for i in range(len(df)):
        str1=str(df.iloc[i,0])
        str1=str1[1:]
        str1=str1[:-1]
        str1=str1.replace("'","")
        try:
    
            link,status,wrk=str1.split(",")
            link_list.append(link)
            status_code.append(status)
            work.append(wrk)
            success.append("done")
        
        except:
        
            link_list.append(str1[:-10])
            status_code.append(str1[-9:-5])
            work.append(str1[-4:])
            success.append("maybe")
            
            
            
        
    df1=pd.DataFrame()
    df1["n.name"]=link_list
    df1["statuscode"]=status_code
    df1["iswork?"]=work
    df1["success"]=success
    
    temp=str(filename)
    temp.replace(".csv","")
    df1.to_csv(temp+"processed.csv")
    