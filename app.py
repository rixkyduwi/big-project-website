from application import app
app.config['MYSQL_DATABASE_HOST']= 'us-cdbr-east-05.cleardb.net'
app.config['MYSQL_DATABASE_USER'] = 'bccc1e5d68a972'
app.config['MYSQL_DATABASE_PASSWORD']  = '1171dc99'
app.config['MYSQL_DATABASE_DB'] = 'heroku_068afdbbc88db22'
if __name__ == '__main__':
    app.run(port=5000, debug=True)