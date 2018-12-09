import json, sqlite3


def get_department_name(id, cur):
    result = cur.execute("SELECT department_id FROM artwork__department WHERE artwork_id = \""+id+"\"").fetchone()

    department_id = result[0]
    
    result = cur.execute("SELECT name FROM department WHERE id = \""+department_id+"\"").fetchone()

    return result[0]

def get_creator_info(id, cur):
    result = cur.execute("SELECT creator_id FROM artwork__creator WHERE artwork_id=\""+id+"\"").fetchall()
    # if no creator we have to check
    if len(result) == 0: 
        return [] 
    else:
        #some cases there is more than one creator
        creators_roles = list() 
        for r in result:
            result = cur.execute("SELECT role, description FROM creator WHERE id = \""+r[0]+"\"").fetchone()
            if result:
                n = '{"role": "'+result[0].replace('"','\\"')+'", "description":"'+result[1].replace("'","’").replace('"','”')+'"}'
                creators_roles.append(json.loads(n))
        return creators_roles

def convert(input, output, department_file):
    # making connection with the sqlite file
    connection = sqlite3.connect(input) 
    cur = connection.cursor()

  
    
    # "w+" means if not existed create one and if Overwrites the existing file 
    f = open(output, "w+", encoding='utf-8') 
    f.close()
    
    # "a" means that we will keep adding to the existing data every time we call f.write("some text")
    f = open(output, "a", encoding='utf-8')
    #start of array
    f.write("[") 


    result = cur.execute("SELECT * FROM artwork").fetchall()

    # list(array) which will contain the json objects
    rows = list() 
    for row in result:
        
        
        id = row[0].replace('"','\\"')                
        accession_number = row[1].replace('"','\\"')  
        title = row[2].replace('"','\\"')             
        tombstone = row[3].replace('"','\\"')        
        department = get_department_name(id, cur)  
        creators = str(get_creator_info(id, cur)).replace("'",'"')     

       
        rows.append('{"id":"'+id+'", "accession_number": "'+accession_number+'", "title": "'+title+'", "tombstone": "'+tombstone+'", "department": "'+department+'", "creators": '+creators+'}')                
    
    #writing to the json file and sperate them with "," and  "\n" ( not be in the same line).
    f.write(",\n".join(rows))

    #end of the array
    f.write("]")

    f.close()
    # department file

    f = open(department_file, "w+", encoding='utf-8') 
    f.close()
    
    f = open(department_file, "a", encoding='utf-8')
    t = list()
    result = cur.execute("SELECT * FROM department").fetchall()
    for r in result:
        t.append(r[1])
    f.write(str(t).replace("'",'"'))
    f.close()

#creating two JSON files
if __name__ == "__main__":
    sqlite3_file = "./cma-artworks.db"
    json_file = "./example.json"
    department_file = "./departments.json"
    convert(sqlite3_file, json_file, department_file)
    


