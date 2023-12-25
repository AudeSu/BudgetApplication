class Expense:
    def __init__(self, id, user_id, amount, category, description):
        self.__id = id
        self.__user_id = user_id
        self.__amount = amount
        self.__category = category
        self.__description = description
