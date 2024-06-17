import uuid

def handle_uploaded_file(f):  
    file_extension = f.name.split('.')[-1]
    filename = str(uuid.uuid4()) + '.' + file_extension
    with open('static/upload/' + filename, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  
    return 'static/upload/' + filename