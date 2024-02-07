from .. import socketio

selected_id = None
selected_title = None

# handle title 
@socketio.on('selected_title')
def handle_console_log_id(message):
    global selected_title
    if 'title' in message:
        selected_title = message['title']
        print(f'this is your item title: \n{selected_title}\n')
    else:
        print('invalid message format')
    return selected_title

# handle ID 
@socketio.on('selected_id')
def handle_console_log_id(message):
    global selected_id
    if 'value' in message:
        selected_id = message['value']
        print(f'this is your item id: \n{selected_id}\n')
    if 'indexnum' in message:
        tab_index = message['indexnum']
        print(f'this is your item INDEX: \n{tab_index}\n')

    else:
        print('invalid message format')
    return selected_id

@socketio.on('my event')
def handle_message(data):
    print('received message: ' + data)