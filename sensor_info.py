def get_sensor_info(sensor) :

    if sensor == "140" : return "100x25", "FTH bias none"
    if sensor == "136" : return "100x25", "FTH bias none"
    if sensor == "129" : return "100x25", "FDB bias none"
    if sensor == "131" : return "100x25", "FDB bias none"
    if sensor == "139" : return "100x25", "FTH dot"
    if sensor == "135" : return "100x25", "FTH dot"
    if sensor == "138" : return "50x50" , "FTH bias none"
    if sensor == "134" : return "50x50" , "FTH bias none"
    if sensor == "125" : return "50x50" , "FDB bias none"
    if sensor == "128" : return "50x50" , "FDB bias none"
    if sensor == "137" : return "50x50" , "FTH straight"
    if sensor == "133" : return "50x50" , "FTH straight"
    if sensor == "144" : return "50x50" , "FTH straight"
    if sensor == "126" : return "50x50" , "FTH wiggle"
    if sensor == "127" : return "50x50" , "FTH wiggle"
    if sensor == "130" : return "50x50" , "FTH wiggle"
    if sensor == "132" : return "50x50" , "FTH wiggle"
    if sensor == "113" : return "100x25", "CNM 3D"
    if sensor == "115" : return "100x25", "CNM 3D"
    if sensor == "114" : return "50x50" , "CNM 3D"
    if sensor == "116" : return "50x50" , "CNM 3D"

    return None,None
