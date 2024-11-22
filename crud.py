import sqlite3

#connecting to the database and returning variables for connecting and cursor
def connect_to_db():
    con = sqlite3.connect("bike_inventory.db")
    cur = con.cursor()

    yield con
    yield cur


#menu to interact with the database
def display_menu(con, cur):
    #while loop to continue until the user quits the program
    while True:
        #printing the menu
        print("Welcome to my database program!")
        print("Menu:")
        print("Enter S to create a new database")
        print("Enter C to create a new row")
        print("Enter R to retrieve data")
        print("Enter U to update a row")
        print("Enter D to delete a row")
        print("Enter Q to quit the program")
        menu_choice = input("Enter your choice: ").upper()
        #elif statement to use functions based on the action the user selects
        if menu_choice == "S":
            drop_table(cur)
            create_table(cur)
        elif menu_choice == "C":
            insert_row(cur)
            con.commit()
        elif menu_choice == "R":
            select_row(cur)
        elif menu_choice == "U":
            update_row(cur)
            con.commit()
        elif menu_choice == "D":
            delete_row(cur)
            con.commit()
        elif menu_choice == "Q":
            quit_program(con)
        else:
            print("That command doesn't exist, try again")



#function to create table and print confirmation message
def create_table(cur):
    cur.execute("CREATE TABLE bikes (bike_id INTEGER PRIMARY KEY,"
                "brand TEXT,"
                "frame TEXT,"
                "year INTEGER,"
                "wheels TEXT,"
                "groupset TEXT,"
                "price REAL)")
    print("Database created")


#function to drop table when creating new table
def drop_table(cur):
    cur.execute("DROP TABLE IF EXISTS bikes")


#function to insert a new row to the table
def insert_row(cur):
    #Inputs for each column of the database
    bike_id = input("Enter an id: ")
    brand = input("Enter the brand: ")
    frame = input("Enter the frame: ")
    year = int(input("Enter the model year of the frame: "))
    wheels = input("Enter the wheels: ")
    groupset = input("Enter the groupset: ")
    price = float(input("Enter the price: "))
    cur.execute(f"INSERT INTO bikes VALUES(?, ?, ?, ?, ?, ?, ?)", (bike_id, brand, frame, year, wheels, groupset, price))


#function to select all the rows from the table
def select_all(cur):
    data = cur.execute("SELECT * FROM bikes")
    data = cur.fetchall() #Retrieve all rows
    print(data)


def select_row(cur):
    key = input("Enter the id of the row you would like to retrieve, or type 'all' to retrieve all rows: ").upper()
    if key == "ALL":
        select_all(cur)
    else:
        try:
            key = int(key)
            cur.execute("SELECT * FROM bikes WHERE bike_id = ?", (key,))
            data = cur.fetchone() #Retrieve a single row.
            if data:
                print(data)
            else:
                print("No row found with the given id.")
        except ValueError:
            print("Invalid input. Please enter a valid bike ID or 'all'.")


#function to update a row using the bike_id as the primary key
def update_row(cur):
    key = int(input("Enter the id of the bike you would like to update: "))
    brand = input("Enter the brand: ")
    frame = input("Enter the frame: ")
    year = int(input("Enter the model year of the frame: "))
    wheels = input("Enter the wheels: ")
    groupset = input("Enter the groupset: ")
    price = float(input("Enter the price: "))
    cur.execute(f"UPDATE bikes "
                f"SET brand = '{brand}', frame = '{frame}', year = '{year}', wheels = '{wheels}', groupset = '{groupset}', price = '{price}' "
                f"WHERE bike_id = {key}")


#function to delete a row using the bike_id as a key
def delete_row(cur):
    key = input("Enter the id of the of the row you would like to delete: ")
    cur.execute(f"DELETE FROM bikes WHERE bike_id = {key}")


#function to close the database and quit the program
def quit_program(con):
    con.close()
    quit()


#main function
def main():
    connection = connect_to_db()

    con = next(connection)
    cur = next(connection)

    display_menu(con, cur)


main()