def flush_db(client):
    client.post('/internal/flush-db')
