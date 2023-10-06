from data_formatter import DataFormatter
from data_parser import DataParser
import mysql.connector


class DataInserter:
    @staticmethod
    def get_dictionary_name(dictionary):
        name = dictionary.get("entity_name")
        return name

    @staticmethod
    def iterator(jsonified_data):
        placeholders = ["enemy"]

        for dictionary in jsonified_data:
            name = DataInserter.get_dictionary_name(dictionary)

            if name not in placeholders:
                DataInserter.insert_data_into_table(dictionary, name)

    @staticmethod
    def insert_data_into_table(data, table_name):
        try:
            db = mysql.connector.connect(
                host="127.0.0.1",
                user="bober",
                password="2211",
                database="mystic_quest",
                port="2211"
            )
            cursor = db.cursor()

            data_to_insert = data.copy()
            del data_to_insert["entity_name"]

            insert_query = f"INSERT INTO {table_name} ("
            insert_query += ", ".join(data_to_insert.keys()) + ") VALUES ("
            insert_query += ", ".join(['%s'] * len(data_to_insert)) + ")"

            data_values = tuple(data_to_insert.values())

            # if table_name not in ["fightable_characters"]:
            #     return

            cursor.execute(insert_query, data_values)

            db.commit()
            cursor.close()
            db.close()

            print(f"Data inserted into '{table_name}' successfully.")

        except Exception as e:
            print(f"Error inserting data into '{table_name}': {e}")
            # raise e


path = "C:\\PythonWorkspace\\DatabasesPY\\mystic_quest\\entities_creation\\generated_entities.txt"
# print(*DataParser.parse_file_to_dict(path), sep="\n")
data = DataParser.parse_file_to_dict(path)

DataInserter.iterator(data)