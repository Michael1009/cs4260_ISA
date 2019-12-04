from elasticsearch import Elasticsearch

es = Elasticsearch(['es'])

print("Starting view_updater.py", flush=True)
while True:
    view_dict = {}

    # Open file and count up views per Jersey
    f = None
    try:
        f = open("/app/batch/view_count.log", "r")
        f_lines = f.readlines()
        for line in f_lines:
            line_data = line.split(",")
            user_id = line_data[0]
            jersey_id = int(line_data[1])

            if jersey_id not in view_dict.keys():
                view_dict[jersey_id] = 1
            else:
                view_dict[jersey_id] += 1
        f.close()

        for jersey_id in view_dict.keys():
            if es.indices.exists(index="jersey_index"):
                try:
                    es.update(
                        index='jersey_index',
                        doc_type='jersey',
                        id=jersey_id,
                        body={'script': 'ctx._source.views =' +
                              str(view_dict[jersey_id])}
                    )
                except Exception:
                    continue
    except FileNotFoundError:
        f = open("/app/batch/view_count.log", "w")
        f.write()
        f.close()
