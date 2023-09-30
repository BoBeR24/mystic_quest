from data_parser import DataFormatter
import mysql.connector

class DataInserter:

    def get_dictionary_name(jsonified_data, dictionary):
        name = dictionary.get("entity_name")
        return name

    def iterator(jsonified_data):

        for dictionary in jsonified_data:
            name = jsonified_data.get_dictionary_name(dictionary)

            if name == "npc":
                table_name = "npcs"
            elif name == "enemy":
                table_name = "fightable_characters"
            # elif name == "vendors":
            elif name == "guildname":
                table_name == "quilds"
            elif name == "event":
                table_name == "events"
            # elif name == "questions"
            elif name == "team":
                table_name == "teams"
            elif name == "item":
                table_name == "items"
            elif name == "character":
                table_name == "players"

            jsonified_data.insert_data_into_table(dictionary, table_name)

    def insert_data_into_table(data, table_name):
        try:
            db = mysql.connector.connect(
                host="your_host",
                user="your_user",
                password="your_password",
                database="your_database"
            )
            cursor = db.cursor()

            insert_query = f"INSERT INTO {table_name} ("
            insert_query += ", ".join(data.keys()) + ") VALUES ("
            insert_query += ", ".join(['%s'] * len(data)) + ")"

            data_values = tuple(data.values())

            cursor.execute(insert_query, data_values)

            db.commit()
            cursor.close()
            db.close()

            print(f"Data inserted into '{table_name}' successfully.")

        except Exception as e:
            print(f"Error inserting data into '{table_name}': {e}")