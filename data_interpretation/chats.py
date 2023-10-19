import sys

sys.path.append('')

import mysql.connector


def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="bober",
        password="2211",
        database="mystic_quest",
        port="2211",
    )


def create_private_chat(player1, player2):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO private_chats (player1, player2) VALUES (%s, %s)",
        (player1, player2)
    )

    chat_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return chat_id


def create_group_chat(chat_name):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO group_chats (chat_name) VALUES (%s)",
        (chat_name,)
    )
    chat_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return chat_id


def get_group_chat(target_chat) -> int:
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT chat_id FROM group_chats WHERE chat_name=%s", (target_chat,)
    )
    chat = cursor.fetchone()
    conn.close()

    while chat is None:
        answer = input("Chat with such name doesn't exist. Do you want to create one?(Y/n): ")
        if answer == "Y":
            # If chat with such name doesn't exist - create it
            return create_group_chat(target_chat)
        elif answer == "n":
            return -1
        else:
            print("Invalid input. Please try again")
    else:
        # otherwise return id of the chat
        return chat[0]


def get_private_chat(user_name: str, target_name: str):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM private_chats WHERE (player1=%s AND player2=%s) OR (player1=%s AND player2=%s)", (user_name,
                                                                                                         target_name,
                                                                                                         target_name,
                                                                                                         user_name)
    )

    chat = cursor.fetchone()
    conn.close()

    if chat is None:
        # If chat with such name doesn't exist - create it
        return create_private_chat(user_name, target_name)
    else:
        # otherwise return id of the chat
        return chat[0]


def send_message(sender: str, message_text: str, chat_id: int, receiver="NULL"):
    conn = connect_to_database()
    cursor = conn.cursor()

    # If receiver exists(which might be the case for private messages) we use fill it, otherwise - write NULL
    cursor.execute(
        "INSERT INTO chat_messages (sender, message_text, chat_id, receiver) VALUES (%s, %s, %s, %s)",
        (sender, message_text, chat_id, receiver)
    )
    conn.commit()
    conn.close()


def receive_messages(chat_id: int):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sender, message_text, timestamp FROM chat_messages WHERE chat_id = %s ORDER BY timestamp",
        (chat_id,)
    )
    messages = cursor.fetchall()
    conn.close()
    return messages


def receive_all_private_messages(user_name: str):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sender, message_text, timestamp FROM chat_messages WHERE receiver=%s ORDER BY timestamp",
        (user_name, )
    )
    messages = cursor.fetchall()
    conn.close()
    return messages


def main():
    # Session loop
    while True:
        user = input("Enter your username: ").strip()
        skip = False

        # Choose chat type
        while not skip:
            print("1. Private chats")
            print("2. Group chats")
            print("3. Back")
            choice = input("Enter your choice: ")

            if choice == '1':
                chat_type = "private"
                target_player = input("Enter targets player name: ")
                if target_player == user:
                    print("You can't text yourself. Try again")
                    continue

                chat_id = get_private_chat(user, target_player)
                break
            elif choice == '2':
                chat_type = "group"
                target_chat = input("Enter chat name: ")

                output = get_group_chat(target_chat)

                # output is -1 - go back and ask again(continue current loop)
                if output == -1:
                    continue

                chat_id = output
                break
            elif choice == '3':
                skip = True
                break
            else:
                # Don't proceed unless correct input is given
                print("Invalid choice. Please try again.")

        # Choose interaction option
        while not skip:
            print("1. Send Message")
            print("2. Receive Messages")
            if chat_type == "private":
                print("3. Get all incoming messages")

            print("4. Back")
            sub_choice = input("Enter your choice: ")

            if sub_choice == '1':
                message_text = input("Enter your message: ")
                if chat_type == "private":
                    send_message(user, message_text, chat_id, receiver=target_player)

                send_message(user, message_text, chat_id)

            elif sub_choice == '2':
                messages = receive_messages(chat_id)

                for message in messages:
                    sender, message_text, timestamp = message
                    print(f"{timestamp} - {sender}: {message_text}")
            elif sub_choice == '3' and chat_type == "private":
                messages = receive_all_private_messages(user)

                for message in messages:
                    sender, message_text, timestamp = message
                    print(f"{timestamp} - {sender}: {message_text}")
            elif sub_choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
