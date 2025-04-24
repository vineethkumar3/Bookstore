import psycopg2

class Database:

    @staticmethod
    def connection():
        # Connection details
        host = "54.221.191.221"
        database = "flaskdb"
        user = "postgres"
        password = "12345"
        port = 5432

        try:
            conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port
            )
            cursor = conn.cursor()
            return cursor, conn
        except Exception as e:
            print("❌ Error:", e)
            return None, None

    def insert_user(self, name, email, password):
        cursor, conn = self.connection()  # Use self here
        if not cursor or not conn:
            print("⚠️ Connection failed. Cannot insert data.")
            return

        try:
            insert_query = '''
            INSERT INTO employee (name, email, password)
            VALUES (%s, %s, %s);
            '''
            cursor.execute(insert_query, (name, email, password))
            conn.commit()
            print("✅ Data inserted successfully.")
        except Exception as e:
            print("❌ Insert error:", e)
        finally:
            cursor.close()
            conn.close()

    def get_user_by_name(self,name):
        cursor, conn = Database.connection()
        if not cursor or not conn:
            print("⚠️ Connection failed. Cannot fetch data.")
            return None

        try:
            query = "SELECT * FROM employee WHERE name = %s;"
            cursor.execute(query, (name,))
            user = cursor.fetchone()  # fetch one matching row
            if user:
                print("✅ User found:", user)
                return user
            else:
                print("⚠️ No user found with that name.")
                return None
        except Exception as e:
            print("❌ Fetch error:", e)
            return None
        finally:
            cursor.close()
            conn.close()

