from data_formatter import DataFormatter


class DataParser:
    # Method to parse .txt file with generated entities to easy-to-work format.
    # Returns list with dictionaries where each dictionary is an entry
    @staticmethod
    def parse_file_to_dict(path_to_file: str) -> [{str, str}]:
        with open(path_to_file, 'r') as file:
            text = file.readlines()

            # List in which we are going to write all entities, where entity will be separate dictionary with fields as
            # arguments
            jsonified_data = []

            # Run through all lines in generated text
            for line in text:
                # If line starts with special symbol - it is a blank line, so we can skip it
                if line.startswith("\n"):
                    continue

                # If line starts with --- that means it creates new entity, so we create new dictionary for it
                if line.startswith("---"):
                    jsonified_data.append({"entity_name": DataFormatter.clean_line(line)})
                    continue

                # otherwise line represents field for the last created entity
                field = DataFormatter.format_field_line(line)
                jsonified_data[-1][field[0]] = field[1]

            return jsonified_data


# To print all generated dictionaries uncomment this and specify your path to the file you want to parse:
path = "C:\\PythonWorkspace\\DatabasesPY\\mystic_quest\\generated_entities.txt"
print(*DataParser.parse_file_to_dict(path), sep="\n")
