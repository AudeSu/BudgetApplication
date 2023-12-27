import application


def display_menu():
    print("1. Register")
    print("2. Login")
    print("3. Exit")


def main_menu():
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            application.register_user()
        elif choice == '2':
            application.login_user()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")


def logged_in_menu(user_id):
    while True:
        print("========================================")
        application.get_total_income(user_id)
        application.get_total_expense(user_id)
        application.get_total_expense_by_category(user_id)
        print("========================================")
        print("1. View all incomes")
        print("2. View all expenses")
        print("3. View all expenses for a category")
        print("4. Add income")
        print("5. Add expense")
        print("6. Edit income")
        print("7. Edit expense")
        print("8. Delete income")
        print("9. Delete expense")
        print("10. Export data to CSV")
        print("11. Sign out")

        choice = input("Enter your choice: ")

        if choice == '1':
            application.view_all_incomes(user_id)
        elif choice == '2':
            application.view_all_expenses(user_id)
        elif choice == '3':
            application.view_all_expenses_by_selected_category(user_id)
        elif choice == '4':
            application.add_income(user_id)
        elif choice == '5':
            application.add_expense(user_id)
        elif choice == '6':
            application.edit_income(user_id)
        elif choice == '7':
            application.edit_expense(user_id)
        elif choice == '8':
            application.delete_income(user_id)
        elif choice == '9':
            application.delete_expense(user_id)
        elif choice == '10':
            application.export_data_to_csv(user_id)
        elif choice == '11':
            break
        else:
            print("Invalid choice. Please try again.")
