from snowflake import connector


#  snowflake
def sfconnect():
    cnx = connector.connect(
        account='xxx.eu-central-1',
        user='',
        password='',
        warehouse='COMPUTE_WH',
        database='DEMO_DB',
        schema='PUBLIC'
    )
    return cnx
