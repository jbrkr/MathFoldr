

import psycopg2

connection = psycopg2.connect(
    host="xxxxxxxxx",
    database="postgres", 
    user="postgres",
    password="XXXXXXX",
)
#connection.autocommit = True
cur = connection.cursor()


def wiki_content_func(list_of_wiki_content):
    wc_pre = "INSERT INTO wiki_content(title, parent_link,content, document_id) VALUES "
    
    for ct in list_of_wiki_content:
        coun = 0
        conList = []
        for i in range(len(ct['content'])):
            concon = ct['content'][i].replace('"','')
            concon = concon.replace("'",'')
            concon = concon.replace('"','')
            concon = ''.join([str(i) for i in range(len(concon)) if i != '"'])
            concon = ''.join([str(i) for i in range(len(concon)) if i != "'"])
            
            url = ct['url'][24:]
            url = url.replace("'",'%27')
            url = url.replace('"','')
            
            title = ct['title']
            title = title.replace('"','')
            title = title.replace("'",'')
            
    
            content = [title, url, concon, coun]
            coun += 1
            conList.append(tuple(content))

        qwc = wc_pre + ', '.join([str(i) for i in conList])    + ';'
        cur.execute(qwc)
        connection.commit()


def wiki_list_func(list_of_wiki_content):
    wl_pre = "INSERT INTO wiki_links(parent_link,child_link) VALUES "
    
    for ct in list_of_wiki_content:

        conList = []
        for i in range(len(ct['links'])):
            lin = ct['links'][i]
            
            lin = lin.replace("'",'%27')
            lin = lin.replace('"','')
            
            url = ct['url'][24:]
            url = url.replace("'",'%27')
            url = url.replace('"','')
            
            
            content = [url, lin]
            conList.append(tuple(content))
    
        qwl = wl_pre + ', '.join([str(i) for i in conList])    + ';'
        cur.execute(qwl)
        connection.commit()