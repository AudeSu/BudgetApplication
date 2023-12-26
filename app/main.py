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
        application.get_income_overview(user_id)
        application.get_expense_overview(user_id)
        view_expense_by_category(user_id)
        print("1. View all incomes")
        print("2. View all expenses")
        print("3. View all expenses for a category")
        print("4. Add income")
        print("5. Add expense")
        print("6. Edit income")
        print("7. Edit expense")
        print("8. Delete income")
        print("9. Delete expense")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            view_all_incomes(user_id)
        elif choice == '2':
            view_all_expenses(user_id)
        elif choice == '3':
            view_all_expenses_category(user_id)
        elif choice == '4':
            add_income(user_id)
        elif choice == '5':
            add_expense(user_id)
        elif choice == '6':
            edit_income(user_id)
        elif choice == '7':
            edit_expense(user_id)
        elif choice == '8':
            delete_income(user_id)
        elif choice == '9':
            delete_expense(user_id)
        elif choice == '10':
            break
        else:
            print("Invalid choice. Please try again.")


def view_expense_by_category(user_id):
    expense_by_category = application.get_expense_by_category(user_id)
    print("Expense by Category:")
    for category, amount in expense_by_category:
        print(f"{category}: {amount}")


def view_all_expenses_category(user_id):
    # Get all unique categories for the user
    categories = set(expense[3] for expense in application.get_all_expenses_category(user_id))

    print("Expense Categories:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")

    # Ask the user to choose a category
    category_choice = input("Choose a category (enter the corresponding number): ")

    try:
        category_index = int(category_choice) - 1
        chosen_category = list(categories)[category_index]
        view_expenses_for_category(user_id, chosen_category)
    except (ValueError, IndexError):
        print("Invalid choice. Please try again.")


def view_expenses_for_category(user_id, category):
    expenses_for_category = application.get_expenses_for_category(user_id, category)
    print(f"All Expenses for {category}:")
    for expense in expenses_for_category:
        print(expense)


def add_income(user_id):
    amount = float(input("Enter the income amount: "))
    description = input("Enter a description for the income: ")
    application.add_income(user_id, amount, description)
    print("Income added successfully!\n")


def add_expense(user_id):
    amount = float(input("Enter the expense amount: "))
    category = input("Enter the expense category: ")
    description = input("Enter a description for the expense: ")
    application.add_expense(user_id, amount, category, description)
    print("Expense added successfully!\n")


def view_all_incomes(user_id):
    all_incomes = application.get_all_incomes(user_id)
    print("All Incomes:")
    for income in all_incomes:
        print(income)


def view_all_expenses(user_id):
    all_expenses = application.get_all_expenses(user_id)
    print("All Expenses:")
    for expense in all_expenses:
        print(expense)


def view_all_expenses_category(user_id):
    all_expenses_category = application.get_all_expenses_category(user_id)
    print("All Expenses by Category:")
    for expense in all_expenses_category:
        print(expense)


def edit_income(user_id):
    view_all_incomes(user_id)

    expense_id = input("Enter the ID of the income you want to delete: ")


def edit_expense(user_id):
    view_all_expenses(user_id)

    expense_id = input("Enter the ID of the expense you want to edit: ")


def delete_income(user_id):
    view_all_incomes(user_id)

    expense_id = input("Enter the ID of the income you want to delete: ")


def delete_expense(user_id):
    view_all_expenses(user_id)

    expense_id = input("Enter the ID of the expense you want to delete: ")


if __name__ == '__main__':
    application.create_database()
    main_menu()
    application.conn.close()
