"""
第50章: 数据处理与CSV/JSON
=============================

数据传输格式.
- CSV
- JSON
- XML
- pickle
"""

import json
import csv
import io


def json_demo():
    """JSON"""
    data = {"name": "Alice", "age": 30}
    s = json.dumps(data)
    print(f"dumps: {s}")
    print(f"loads: {json.loads(s)}")


def json_indent():
    """格式化JSON"""
    data = {"user": {"name": "Bob", "id": 1}}
    print(json.dumps(data, indent=2))


def csv_demo():
    """CSV"""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Age"])
    writer.writerow(["Alice", "30"])
    print(output.getvalue())


def csv_reader():
    """CSV读取"""
    data = "Name,Age\nAlice,30\nBob,25"
    reader = csv.DictReader(io.StringIO(data))
    for row in reader:
        print(f"row: {row}")


def pickle_demo():
    """pickle"""
    import pickle
    data = {"key": "value"}
    pickled = pickle.dumps(data)
    unpickled = pickle.loads(pickled)
    print(f"unpickled: {unpickled}")


def base64_demo():
    """base64"""
    import base64
    data = b"hello"
    encoded = base64.b64encode(data)
    print(f"encoded: {encoded}")
    print(f"decoded: {base64.b64decode(encoded)}")


if __name__ == "__main__":
    print("=" * 50)
    print("50. 数据处理")
    print("=" * 50)
    json_demo()
    print()
    json_indent()
    print()
    csv_demo()
    csv_reader()
    pickle_demo()
    base64_demo()
    print("=" * 50)