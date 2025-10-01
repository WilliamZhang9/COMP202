# 1. Please complete the following:
#   Your First name and Last Name: William Zhang
#   Your Student ID: 260459020

#define constants
MIN_LAT = -90
MAX_LAT = 90
MIN_LONG = -180
MAX_LONG = 180
EARTH_RADIUS = 6378 #in km
STORM_STEPS= 5
import math
import random

def degrees_to_radians(degrees): # function to convert degrees to radians
    radians = degrees * (math.pi / 180)
    return round(radians, 2)

def get_valid_coordinate(val_name, min_float, max_float): # function to get valid coordinate input
    while True:
        value = float(input("What is your {} ?".format(val_name)))
        if min_float < value < max_float:   # check if value valid
            return value
        else:
            print("Invalid {}".format(val_name))

def get_gps_location(): # function to get valid gps location
    lat = get_valid_coordinate("latitude", MIN_LAT, MAX_LAT)
    longi = get_valid_coordinate("longitude", MIN_LONG, MAX_LONG)
    return lat, longi

def distance_two_points(lat1, long1, lat2, long2): # function to calculate distance between two gps points
    # converting degrees to radians by calling earlier function
    lat1_rad = degrees_to_radians(lat1)
    long1_rad = degrees_to_radians(long1)
    lat2_rad = degrees_to_radians(lat2)
    long2_rad = degrees_to_radians(long2)
    latDiff= lat2_rad-lat1_rad
    longDiff= long2_rad-long1_rad
    a = (math.sin(latDiff/2))**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * (math.sin(longDiff/2))**2 # haversine formula
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = EARTH_RADIUS * c
    return round(distance, 2) # 2 decimal places

def apply_wave_impact(position, min_float, max_float): # function to apply wave impact on a coordinate
    while True:
        wave_step = (random.random() - 0.5) * 2 # random float between -1 and 1
        new_pos = position + wave_step
        if min_float < new_pos < max_float: # strictly between bounds
            return round(new_pos, 2)
        # else, repeat the loop

def wave_hit_vessel (latitude, longitude): # function to simulate wave hits over storm duration
    i = 0
    while i < STORM_STEPS:
        latitude = apply_wave_impact(latitude, MIN_LAT, MAX_LAT)    # apply wave impact to latitude
        longitude = apply_wave_impact(longitude, MIN_LONG, MAX_LONG) # apply wave impact to longitude
        i += 1
    return latitude, longitude

def move_toward_waypoint(current_lat, current_long, waypoint_lat, waypoint_long):   # function to move vessel toward waypoint
    scale = random.random() + 1 # random float between 1 and 2
    new_lat = current_lat + (waypoint_lat - current_lat) / scale
    new_long = current_long + (waypoint_long - current_long) / scale
    new_lat = max(MIN_LAT, min(MAX_LAT, new_lat))   # ensuring new_lat meets value requirements
    new_long = max(MIN_LONG, min(MAX_LONG, new_long))
    return round(new_lat, 2), round(new_long, 2)

def vessel_menu(): # main function to run the vessel menu
    print("Welcome to the boat menu!")
    current_latitude = get_valid_coordinate("latitude", MIN_LAT, MAX_LAT)   # get initial coordinates
    current_longitude = get_valid_coordinate("longitude", MIN_LONG, MAX_LONG)

    waypoint_latitude = None
    waypoint_longitude = None
    storm_counter = STORM_STEPS
    mission_active = True   # to control the loop

    while mission_active:   # main execution
        print("Please select an option below:")
        print("1) Set waypoint")
        print("2) Move toward waypoint and Status report")
        print("3) Exit boat menu")
        choice = input("Choose: ")
        if choice == "1":
            print("Enter waypoint coordinates.")
            waypoint_latitude, waypoint_longitude = get_gps_location()
            print("Waypoint set to latitude of {:.1f} and longitude of {:.1f}.".format(waypoint_latitude, waypoint_longitude)) # 1 decimal place
        elif choice == "2":
            if not (waypoint_latitude and waypoint_longitude):
                print("No waypoint set.")
            else:
                print("Captain Log: Journeyed towards waypoint.")
                # move toward waypoint
                current_latitude, current_longitude = move_toward_waypoint(
                current_latitude, current_longitude, waypoint_latitude, waypoint_longitude)

                # 20% chance getting struck by wave
                if random.random() < 0.2:
                    current_latitude = apply_wave_impact(current_latitude, MIN_LAT, MAX_LAT)
                    current_longitude = apply_wave_impact(current_longitude, MIN_LONG, MAX_LONG)
                    print("Captain Log: Wave impact recorded.")

                print("Current position is latitude of {:.2f} and longitude of {:.2f}".format(current_latitude, current_longitude)) # 2 decimal places
                # calculate remaining distance
                remaining_distance = distance_two_points(current_latitude, current_longitude, waypoint_latitude, waypoint_longitude)
                print("Distance to waypoint: {:.2f} km".format(remaining_distance))

                if remaining_distance <= 10:
                    print("Mission success: waypoint reached before storm.")
                    mission_active = False
                else:
                    storm_counter -= 1
                    print("Storm T-minus: {}".format(storm_counter))
                    if storm_counter == 0:
                        current_latitude, current_longitude = wave_hit_vessel(current_latitude, current_longitude)
                        print("Mission failed: storm hit before arrival.")
                        mission_active = False

        elif choice == "3":
            print("Console closed by captain.")
            mission_active = False

        else:
            print("Invalid choice. Try again.")
