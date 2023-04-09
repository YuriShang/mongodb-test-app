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
        return "На указанные даты данных нет"

    result["dataset"].append(val)
    result["labels"].pop(-1)

    return str(result)
