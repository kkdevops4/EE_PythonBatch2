class RadarSensor:
    def __init__(self,distance :float=0.0):
        self._distance=None
        self.distance=distance

    @property
    def distance(self)->float:
            return self._distance
    @distance.setter
    def distance(self,value:float):
            if not isinstance(value,(int,float)):
                raise TypeError("Distance must be a number.")
            if value<0:
                raise ValueError("Distance cannot be negative.")
            self._distance=float(value)
    def get_status(self)->str:
            d=self._distance
            if d>=10:
                return "SAFE"
            elif d>=5:
                return "CAUTION"
            else:
                return "DANGER"
if __name__ == "__main__":
    sensor = RadarSensor(12)
    print(sensor.distance, sensor.get_status())  # 12.0 SAFE

    sensor.distance = 7
    print(sensor.distance, sensor.get_status())  # 7.0 CAUTION

    sensor.distance = 3
    print(sensor.distance, sensor.get_status())  # 3.0 DANGER
