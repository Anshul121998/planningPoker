import uuid

dataStorage = {}

def room_creator(json_data):
    if json_data['uuid'] == '':
        my_uuid = str(uuid.uuid4())
        while json_data['uuid'] in dataStorage:
            my_uuid = str(uuid.uuid4())
        dataStorage[my_uuid] = {
            'polling' : False,
            'attendees' : [],
            'creator' : json_data['name'],
            'topPeople' : [],
            'datetime' : json_data['datetime'],
            'topEstimate' : '',
            'topEstimateNumber' : -1
        }
        return {
            'uuid' : my_uuid,d
            'polling' : False
        }
    else:
        if json_data['uuid'] in dataStorage:
            return {
                'uuid' : json_data['uuid'],
                'polling' : dataStorage[json_data['uuid']]['polling']
            }
    return {
        'uuid' : '1',
        'polling' : False
    }

def enter_room(json_data):
    if json_data['uuid'] in dataStorage:
        exists = False
        loc = -1
        for i in range(0, len(dataStorage[json_data['uuid']]['attendees'])):
            if(dataStorage[json_data['uuid']]['attendees'][i]['name'] == json_data['name']):
                exists = True
                loc = i
                break
        if dataStorage[json_data['uuid']]['polling'] and exists:
            dataStorage[json_data['uuid']]['attendees'][loc]['estimate'] = json_data['estimate']
            store_top_estimate(json_data['uuid'], json_data['estimate'], dataStorage[json_data['uuid']]['attendees'][loc]['name'])
            return 1
        elif dataStorage[json_data['uuid']]['polling'] and not exists:
            dataStorage[json_data['uuid']]['attendees'].append({'name' : json_data['name'], 'estimate' : json_data['estimate']})
            store_top_estimate(json_data['uuid'], json_data['estimate'], json_data['name'])
            return 1
        elif not dataStorage[json_data['uuid']]['polling'] and not exists:
            dataStorage[json_data['uuid']]['attendees'].append({'name' : json_data['name'], 'estimate' : -1})
            return 0
        else:
            return 0
    else:
        return -1
    
def store_top_estimate(data_uuid, val, name):
    if val == 'Infinity':
        if 'Infinity' != dataStorage[data_uuid]['topEstimate']:
            dataStorage[data_uuid]['topEstimateNumber'] = 1000
            dataStorage[data_uuid]['topEstimate'] = val
            dataStorage[data_uuid]['topPeople'] = []
    else:
        if float(val) > dataStorage[data_uuid]['topEstimateNumber']:
            dataStorage[data_uuid]['topEstimateNumber'] = float(val)
            dataStorage[data_uuid]['topEstimate'] = val
            dataStorage[data_uuid]['topPeople'] = []
    if val == dataStorage[data_uuid]['topEstimate'] and name not in dataStorage[data_uuid]['topPeople']:
        dataStorage[data_uuid]['topPeople'].append(name)

def toggle_polling(json_data):
    if json_data['uuid'] in dataStorage:
        if json_data['polling']:
            dataStorage[json_data['uuid']]['attendees'] = []
            dataStorage[json_data['uuid']]['topEstimateNumber'] = -1
            dataStorage[json_data['uuid']]['topEstimate'] = ''
            dataStorage[json_data['uuid']]['topPeople'] = []
            dataStorage[json_data['uuid']]['polling'] = json_data['polling']
            return 1
        else:
            dataStorage[json_data['uuid']]['polling'] = False
            return dataStorage[json_data['uuid']]
    else:
        return 0

def check_participants(json_data):
    if json_data['uuid'] in dataStorage:
        user_list = []
        for i in dataStorage[json_data['uuid']]['attendees']:
            user_list.append(i['name'])
        return user_list
    else:
        return 0
