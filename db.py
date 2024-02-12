import sqlite3


class Database:
    def __init__(self, file):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id):
        with self.connection:
            return self.connection.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def create_table(self):
        with self.connection:
            return self.connection.execute(
                f"CREATE TABLE IF NOT EXISTS users (`id` INTEGER PRIMARY KEY, `user_id` INTEGER, `ball` INTEGER DEFAULT 0, `tasks` INTEGER DEFAULT 0 , `date` TEXT, `date_test` TEXT)")

    def get_ball(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `ball` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return result[0][0]

    def get_num_rating(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `ball`, `user_id` FROM `users`").fetchall()
            result = [i[1]
                      for i in sorted(result, key=lambda x: x[0], reverse=True)]
            return int(result.index(user_id)+1)

    def get_date(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `date` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return result[0][0]

    def get_date_test(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `date_test` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return result[0][0]

    def get_users_id(self):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `user_id` FROM `users`").fetchall()
            return result

    def get_db_data(self):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `users`").fetchall()
            return result

    def update_date(self, user_id, date):
        with self.connection:
            return self.connection.execute("UPDATE `users` SET `date` = ? WHERE `user_id` = ?", (date, user_id))

    def update_date_test(self, user_id, date):
        with self.connection:
            return self.connection.execute("UPDATE `users` SET `date_test` = ? WHERE `user_id` = ?", (date, user_id))

    def update_ball(self, user_id, ball):
        with self.connection:
            return self.connection.execute("UPDATE `users` SET `ball` = `ball`+ ? WHERE `user_id` = ?", (ball, user_id))

    def close(self):
        self.connection.close()


db = Database('users.db')
