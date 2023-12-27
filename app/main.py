import database
import menu

if __name__ == '__main__':
    database.create_database()
    database.create_test_user()
    menu.main_menu()
    database.close_database()
