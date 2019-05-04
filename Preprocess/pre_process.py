import couchdb
# from collections import Counter

server = couchdb.Server('http://admin:123456@localhost:5984/')
db = server['apr_by_suburb']
suburb_text_dict = {}

for doc_id in db:
    suburb = db[doc_id]['suburb']
    text = db[doc_id]['doc']['doc']['text']
    if suburb not in suburb_text_dict.keys():
        text_list = []
        suburb_text_dict.update({
            suburb: text_list
        })
    else:
        text_list = suburb_text_dict.get(suburb)
    text_list.append(text)

suburb_info_list = []
total_num = 0
for suburb in suburb_text_dict.keys():
    text_list = suburb_text_dict.get(suburb)
    print(suburb + ": " + str(len(text_list)))
    suburb_info_list.append({
        suburb: len(text_list)
    })
    total_num += len(text_list)

print(total_num)

processed_db = server.create('processed_data')
for suburb_info in suburb_info_list:
    processed_db.save(suburb_info)

