import json, unittest
from datetime import datetime, timezone

with open("./data-1.json") as f:
    jsonData1 = json.load(f)
with open("./data-2.json") as f:
    jsonData2 = json.load(f)
with open("./data-result.json") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1(jsonObject):
    parts = jsonObject["location"].split("/")
    return {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": {
            "country": parts[0],
            "city": parts[1],
            "area": parts[2],
            "factory": parts[3],
            "section": parts[4]
        },
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    }


def convertFromFormat2(jsonObject):
    dt = datetime.strptime(jsonObject["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
    dt = dt.replace(tzinfo=timezone.utc)
    return {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": int(dt.timestamp() * 1000),
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },
        "data": {
            "status": jsonObject["data"]["status"],
            "temperature": jsonObject["data"]["temperature"]
        }
    }


def main(jsonObject):
    if jsonObject.get("device") is None:
        return convertFromFormat1(jsonObject)
    return convertFromFormat2(jsonObject)


class TestSolution(unittest.TestCase):
    def test_sanity(self):
        self.assertEqual(json.loads(json.dumps(jsonExpectedResult)), jsonExpectedResult)

    def test_dataType1(self):
        self.assertEqual(main(jsonData1), jsonExpectedResult, "Converting from Type 1 failed")

    def test_dataType2(self):
        self.assertEqual(main(jsonData2), jsonExpectedResult, "Converting from Type 2 failed")


if __name__ == "__main__":
    unittest.main()