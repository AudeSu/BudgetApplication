import application

if __name__ == '__main__':
    application.create_database()
    application.conn.close()
