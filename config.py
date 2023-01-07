import os, json
import psycopg2

class Config:
    # store all user input
    def __init__(self):
        self.data_path = None
        self.pg_config = None
        self.sort_by_match_strength = False

    def run(self):
        """Completes new config process or uses an existing one. Dumps new data into a JSON file if it is generated, and returns either an old instance of `Config` or the new one as `self`"""
        if os.path.exists("./config.json"):
            prev_config = self.handle_prev_config()
            if prev_config is not None:
                return prev_config
            else:
                self.get_data_path()
                self.set_pg_config()
                self.output_formatting()
                with open("./config.json", "w") as outfile:
                    json.dump(self.__encode(), outfile)
                return self
        else:
            self.get_data_path()
            self.set_pg_config()
            self.output_formatting()
            with open("./config.json", "w") as outfile:
                json.dump(self.__encode(), outfile)
            return self

    # if a config file already exists, offer to use it instead
    def handle_prev_config(self):
        """Receives user input and attempts to locate existing config file."""
        response_for_prev_config = input("Use existing configuration file? y/n " ).lower()
        
        if response_for_prev_config == "y":
            prev_data: Config = open("./config.json")
            prev_data = json.load(prev_data)
            return prev_data
        elif response_for_prev_config == "n":
            return None
        else:
            print("Invalid response.")
            self.handle_prev_config()

    def get_data_path(self):
        """Locates a valid directory from user input and stores it in Config state as `self.data_path`."""
        data_path = input("Provide the location of the directory where we can find your photos: ")

        if not os.path.exists(data_path):
            print("We didn't find a directory by this name.")
            self.data_path = self.get_data_path()
        else:
            print("Got it!")
            self.data_path = data_path

    def set_pg_config(self):
        """Determine if data should be associated with a PostgreSQL instance, and, if so, record the required connection info"""
        elect_for_pg = input("Connect this program to a PostgreSQL instance? y/n ").lower()
        if elect_for_pg == "y":
            self.pg_config = {}

            print("Please provide the relevant connection info. This sensitive information will only be recorded locally on your own machine.")
            dbname = input("Provide the DB name: ")
            user = input("Provide the username: ")
            password = input("Provide the password: ")

            print("The following details are optional and may be skipped if connecting to a local instance")
            host = input("Provide the host address: ")
            port = input("Provide the port connection number: ")

            print("Testing connection:")

            try:
                dsn = f"dbname={dbname} user={user} password={password}"
                if host:
                    dsn = dsn + host

                if port:
                    dsn = dsn + port

                conn = psycopg2.connect(f"dbname={dbname} user={user} password={password}")
                conn.close()

                print("Connection successful!")
                self.pg_config['dsn'] = dsn
            except psycopg2.Error as e:
                print("There was an error connecting: ")
                print(e)
                self.set_pg_config()

        elif elect_for_pg == "n":
            pass
        else:
            print("Invalid response.")
            self.set_pg_config()

    def output_formatting(self):
        sort_by_match_strength = input("Sort all files by match strength, or mix all matches together? sort/mix ").lower()
        if sort_by_match_strength == "sort":
            self.sort_by_match_strength = True
        elif sort_by_match_strength == "mix":
            self.sort_by_match_strength = False
        else:
            print("Invalid response.")
            self.output_formatting()

    def __encode(self):
        return json.dumps(self, default=lambda x: x.__dict__)

new_config = Config()
new_config.run()