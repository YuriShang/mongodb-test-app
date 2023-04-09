from datetime import datetime
from app.db.database import collection
from app.utils.time_range import time_range


async def data_handler(dt_from, dt_upto, group_type):
    result = {
        "dataset": [],
        "labels": []
    }
    result["labels"] = time_range(dt_from, dt_upto, group_type, result["labels"])
    result["labels"].append(datetime.isoformat(dt_upto))

    pipeline = [{'$match': {'dt': {'$gte': dt_from, '$lt': dt_upto}}},
                {'$sort': {'dt': 1}}]

    cursor = collection.aggregate(pipeline)
    documents = await cursor.to_list(None)

    if documents:
        for date in result["labels"][1:]:
            val = 0
            count = 0
            for document in documents:
                if document["dt"] < datetime.fromisoformat(date):
                    val += document["value"]
                    count += 1
                else:
                    documents = documents[count:]
                    result["dataset"].append(val)
                    break
    else:
        return "На эти даты данных нет"

    result["dataset"].append(val)
    result["labels"].pop(-1)

    return str(result)

    t = {"dataset": [0, 0, 0, 195028, 190610, 193448, 203057, 208605, 191361, 186224, 181561, 195264, 213854, 194070,
                     208372, 184966, 196745, 185221, 196197, 200647, 196755, 221695, 189114, 204853, 194652, 188096,
                     215141,
                     185000, 206936, 200164, 188238, 195279, 191601, 201722, 207361, 184391, 203336, 205045, 202717,
                     182251,
                     185631, 186703, 193604, 204879, 201341, 202654, 183856, 207001, 204274, 204119, 188486, 191392,
                     184199,
                     202045, 193454, 198738, 205226, 188764, 191233, 193167, 205334],
         "labels": ["2022-10-01T00:00:00", "2022-10-02T00:00:00", "2022-10-03T00:00:00", "2022-10-04T00:00:00",
                    "2022-10-05T00:00:00", "2022-10-06T00:00:00", "2022-10-07T00:00:00", "2022-10-08T00:00:00",
                    "2022-10-09T00:00:00", "2022-10-10T00:00:00", "2022-10-11T00:00:00", "2022-10-12T00:00:00",
                    "2022-10-13T00:00:00", "2022-10-14T00:00:00", "2022-10-15T00:00:00", "2022-10-16T00:00:00",
                    "2022-10-17T00:00:00", "2022-10-18T00:00:00", "2022-10-19T00:00:00", "2022-10-20T00:00:00",
                    "2022-10-21T00:00:00", "2022-10-22T00:00:00", "2022-10-23T00:00:00", "2022-10-24T00:00:00",
                    "2022-10-25T00:00:00", "2022-10-26T00:00:00", "2022-10-27T00:00:00", "2022-10-28T00:00:00",
                    "2022-10-29T00:00:00", "2022-10-30T00:00:00", "2022-10-31T00:00:00", "2022-11-01T00:00:00",
                    "2022-11-02T00:00:00", "2022-11-03T00:00:00", "2022-11-04T00:00:00", "2022-11-05T00:00:00",
                    "2022-11-06T00:00:00", "2022-11-07T00:00:00", "2022-11-08T00:00:00", "2022-11-09T00:00:00",
                    "2022-11-10T00:00:00", "2022-11-11T00:00:00", "2022-11-12T00:00:00", "2022-11-13T00:00:00",
                    "2022-11-14T00:00:00", "2022-11-15T00:00:00", "2022-11-16T00:00:00", "2022-11-17T00:00:00",
                    "2022-11-18T00:00:00", "2022-11-19T00:00:00", "2022-11-20T00:00:00", "2022-11-21T00:00:00",
                    "2022-11-22T00:00:00", "2022-11-23T00:00:00", "2022-11-24T00:00:00", "2022-11-25T00:00:00",
                    "2022-11-26T00:00:00", "2022-11-27T00:00:00", "2022-11-28T00:00:00", "2022-11-29T00:00:00",
                    "2022-11-30T00:00:00"]}

    # t = {"dataset": [5906586, 5515874, 5889803, 6092634], "labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00", "2022-11-01T00:00:00", "2022-12-01T00:00:00"]}

    print(result, sum(result["dataset"]))
    print(t, sum(t["dataset"]))

    print(t["dataset"] == result["dataset"])
    for i, j in zip(t["dataset"], result["dataset"]):
        print(i, j, i == j)

    """for i in range(len(result["labels"])-1):
        fr = datetime.fromisoformat(result["labels"][i])
        to = datetime.fromisoformat(result["labels"][i+1])

        pipeline = [
            {'$match': {'dt': {'$gte': fr, '$lte': to}}},
            {'$group': {
                '_id': 'null',
                'total': {'$sum': '$value'}}}
        ]

        cursor = collection.aggregate(pipeline)
        doc = await cursor.to_list(None)
        print(doc)
        result["dataset"].append(*doc)

    result["labels"].pop(-1)
    print(result)
    """
