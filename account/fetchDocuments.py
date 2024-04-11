import psycopg2
from django.conf import settings

def fetchdocument(tag, username):
    conn = psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
        )
    cursor = conn.cursor()
    newpaths=[]
    try:
        # Execute your SQL query
        query1 = "SELECT newfilename, extension FROM account_uploadeddocuments WHERE username_id = '"+username +"' AND tags LIKE '"+'%'+ tag+"%';" 
        cursor.execute(query1)
        documents = cursor.fetchall()
        if documents:
            for doc in documents:
                newrecord = 'efs/userData/'+username+'/'+doc[0] 
                path, ext = doc
                print('path', path)
                print('ext', ext)
                newpaths.append(newrecord)
                if 'pdf' in ext:
                    foundext = 1
                elif ext in ['png', 'jpeg', 'jpg', 'webp', 'heic', 'heif']:
                    foundext = 2
                elif ext in ['mp4', 'ogg', 'webm']:
                    foundext = 3
                elif 'mp3' in ext:
                    foundext = 4
        else:
            print(f"No documents found with '{tag}' tag.")
    finally:
            # Clean up by closing cursor and connection
        cursor.close()
        conn.close()
        fetchinfo = [foundext, newpaths]
        return fetchinfo
