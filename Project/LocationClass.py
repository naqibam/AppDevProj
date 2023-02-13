class GymLocation:
    count_id = 0

    def __init__(self, locationAddress, lat, lng):
        GymLocation.count_id += 1
        self.__gymLocation_id = GymLocation.count_id
        self.__locationAddress = locationAddress
        self.__lat = lat
        self.__lng = lng

    def get_location_id(self):
        return self.__gymLocation_id

    def get_locationAddress(self):
        return self.__locationAddress

    def get_lat(self):
        return self.__lat

    def get_lng(self):
        return self.__lng


    def set_location_id(self, gymLocation_id):
        self.__gymLocation_id = gymLocation_id

    def set_locationAddress(self, locationAddress):
        self.__locationAddress = locationAddress

    def set_lat(self, lat):
        self.__lat = lat

    def set_lng(self, lng):
        self.__lng = lng
