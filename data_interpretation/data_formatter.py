class DataFormatter:
    # Performs complete cleaning of the given line
    @staticmethod
    def clean_line(line: str) -> str:
        result = ""

        # Delete end line symbol
        line = line.replace("\n", "")

        # Only letter characters should stay in the line
        for letter in line:
            if letter != "-":
                result += letter

        return result.lower().strip()

    # Performs formatting for the line which represents field of an entity
    @staticmethod
    def format_field_line(line: str) -> (str, str):
        line = line.replace("\"", "")
        line = line.replace("\n", "")
        split_line = tuple(line.split("="))

        return split_line


