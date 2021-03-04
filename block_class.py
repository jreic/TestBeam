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
    if "144irrad" in sensor : return "50x50" , "FTH straight"
    if sensor == "126" : return "50x50" , "FTH wiggle"
    if sensor == "127" : return "50x50" , "FTH wiggle"
    if sensor == "130" : return "50x50" , "FTH wiggle"
    if sensor == "132" : return "50x50" , "FTH wiggle"
    if sensor == "113" : return "100x25", "CNM 3D"
    if sensor == "115" : return "100x25", "CNM 3D"
    if sensor == "114" : return "50x50" , "CNM 3D"
    if sensor == "116" : return "50x50" , "CNM 3D"
    if sensor == "180" : return "100x25", "HPK bitten no PT"
    if sensor == "181" : return "100x25", "HPK bitten no PT"
    if sensor == "183" : return "50x50",  "HPK default no PT"
    if sensor == "184" : return "50x50",  "HPK default no PT"
    if sensor == "185" : return "100x25", "HPK bitten no PT"
    if sensor == "186" : return "50x50",  "HPK default no PT"
    if sensor == "193" : return "100x25", "FBK 3D"
    if sensor == "194" : return "50x50",  "FBK 3D"
    if sensor == "IT1" : return "50x50",  "FBK slimedge 200"
    if "IT5irrad" in sensor : return "50x50",  "FBK slimedge 100"
    if sensor == "502" : return "100x25",  "FBK planar EXT02"

    return None,None

class block_obj :
    def __init__(self, run_range, sensor_name, angle=None, bias=None, lkc=None, threshold=None, temp=None, irrad=False, duplicate=0) :
        self.run_range = run_range
        self.sensor_name = sensor_name
        self.pitch, self.sensor_type = get_sensor_info(sensor_name)
        self.angle = angle
        self.bias = bias
        self.lkc = lkc
        self.threshold = threshold
        self.temp = temp
        self.irrad = irrad
        self.duplicate = duplicate

