# consume.py
def consume(request):
    path = request['data']['path']
    content = request['data']['content']
    print("Replacing {path}".format(
        path=path))

def onopen(service):
   print('Opened: {}'.format(service.service))
   service.impl["Mix/Consume"] = consume

def onclose(service):
    print('Closed: {}'.format(service.service))
