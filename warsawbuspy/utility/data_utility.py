from warsawbuspy.utility.exceptions import InvalidFileExtensionException


# API sends times like 25:01:24 for schedules etc., so this function parses that back
# into normal time format (for 25:00:00 it would be 01:00:00).
def time_parser(time_data: str) -> str:
    if '24' <= time_data[:2] <= '29':
        time_data = '0' + str(int(time_data[:2]) % 24) + time_data[2:]
    return time_data


# Function used to check if the passed file_name has the valid extention.
def assert_file_extension(file_name: str, extension: str) -> None:
    if len(file_name) <= len(extension):
        raise InvalidFileExtensionException(extension)
    if file_name[len(file_name) - len(extension):] != extension:
        raise InvalidFileExtensionException(extension)


# Function to check if the given coordinates are valid.
def is_location_valid(longitude: float, latitude: float) -> bool:
    return (-180.0 <= longitude <= 180.0 and
            -90.0 <= latitude <= 90.0)
