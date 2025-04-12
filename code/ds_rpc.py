def DiscordRPC():
    import pypresence
    from pypresence import Presence
    import time

    client_id = '1358790283902324858'  # Fake ID, put your real one here
    RPC = Presence(client_id)  # Initialize the client class
    is_connected = False
    start_time=time.time() 

    while True:  # The presence will stay on as long as the program is running
        try:
            if is_connected == False:
                RPC.connect()
            is_connected = True
            RPC.update(details="🌷 Platformer game made in python🌹", start=start_time)
            time.sleep(20) # Can only update rich presence every 15 seconds
        except Exception as e:
            if pypresence.DiscordNotFound:
                is_connected = False
            else:
                print(e)
            time.sleep(10)