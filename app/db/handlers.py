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

    pipeline = [{'$match': {'dt': {'$lte': dt_upto, '$gte': dt_from}}},
                {'$sort': {'dt': 1}}]

    cursor = collection.aggregate(pipeline)
    documents = await cursor.to_list(None)
    last_date = documents[0]["dt"]

    if documents:
        for date in result["labels"][1:]:
            val = 0
            count = 0

            # проверяем, чтобы дата всегда была больше предыдущей
            if documents[0]["dt"] >= last_date:
                for document in documents:
                    if document["dt"] < datetime.fromisoformat(date) or document["dt"] == datetime.fromisoformat(result["labels"][-1]):
                        count += 1
                        val += document["value"]
                        if last_date < document["dt"]:
                            last_date = document["dt"]
                    else:
                        documents = documents[count:]
                        break
            result["dataset"].append(val)
    else:
        return "На указанные даты данных нет"

    result["labels"].pop(-1)
    str_result = str(result).replace("'", '"')
    return str_result
