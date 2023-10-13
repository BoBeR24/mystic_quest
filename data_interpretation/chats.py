import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",  # 127.0.0.1
        user="artur",
        password="1234",
        database="mystic_quest",
        # port="3306"
    )

def create_one_on_one_chat(player1, player2):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO one_on_one_chats (player1, player2) VALUES (%s, %s)",
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

def send_message(sender, message_text, chat_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_messages (sender, message_text, chat_id) VALUES (%s, %s, %s)",
        (sender, message_text, chat_id)
    )
    conn.commit()
    conn.close()

def receive_messages(chat_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sender, message_text, timestamp FROM chat_messages WHERE chat_id = %s",
        (chat_id,)
    )
    messages = cursor.fetchall()
    conn.close()
    return messages

def main():
    while True:
        print("1. One-on-One Chat")
        print("2. Group Chat")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            player1 = input("Enter your username: ")
            player2 = input("Enter the other player's username: ")
            chat_id = create_one_on_one_chat(player1, player2)
        elif choice == '2':
            chat_name = input("Enter the chat group name: ")
            chat_id = create_group_chat(chat_name)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

        while True:
            print("1. Send Message")
            print("2. Receive Messages")
            print("3. Back")
            sub_choice = input("Enter your choice: ")

            if sub_choice == '1':
                sender = player1;
                message_text = input("Enter your message: ")
                send_message(sender, message_text, chat_id)
            elif sub_choice == '2':
                messages = receive_messages(chat_id)
                for message in messages:
                    sender, message_text, timestamp = message
                    print(f"{timestamp} - {sender}: {message_text}")
            elif sub_choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()



