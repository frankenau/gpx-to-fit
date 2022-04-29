#!/usr/bin/python
import os, sys, math, time, glob
import xml.etree.ElementTree

# try to create a fit-file from the
# waypoints and/or routes in a gpx-file

fit_data = bytearray()	# global fit_data array to be filled
defn_exported = dict()	# dictionary of message definition ids
defn_max_no = -1		# maximum message definition id (to be incremented)


def btarr_string(name, size):
	"""
	convert a string to a fixed-length byte-array
	padded with nul-characters if necessary
	"""
	return bytes(name + ("\0" * size),'utf-8')[0:size]

def btarr_number(numval, size):
	"""
	convert a number to a byte-array
	"""
	return int(numval).to_bytes(size, "little")

def btarr_coord(coord):
	"""
	convert a angle given in degrees to a byte-array
	used for latitude and logitude vales
	"""
	if coord < 0:
		coord += 360
	return btarr_number(11930465*coord, 4)

def btarr_timestamp(tsec):
	"""
	convert a timestamp to a byte-array
	input is given in seconds since epoch 1.1.1970, 00:00
	"""
	return btarr_number(tsec-631234800, 4)


def message_definition_id(name):
	"""
	return the definition id of a given message type
	if the id does not exit, a new definition is created
	"""
	global defn_max_no
	if name in defn_exported:
		# the name was alredy exported
		# use this id to continue wit a fit data message
		return btarr_number(defn_exported[name], 1)
	# created a new id and a new fit definition message
	defn_max_no += 1
	if name == "file_id":
		fit_data.extend(btarr_number(defn_max_no+64, 1))
		fit_data.extend(b'\x00\x00\x00\x00\x07')
		fit_data.extend(b'\x03\x04\x8C\x06\x04\x86\x07\x04\x86')
		fit_data.extend(b'\x01\x02\x84\x02\x02\x84\x05\x02\x84\x00\x01\x00')
	elif name == "location":
		# location (waypoint) definition message
		fit_data.extend(btarr_number(defn_max_no+64, 1))
		fit_data.extend(b'\x00\x00\x1D\x00\x08')
		fit_data.extend(b'\xFD\x04\x86\x00\x10\x07\x01\x04\x85\x02\x04\x85')
		fit_data.extend(b'\xFE\x02\x84\x03\x02\x84\x04\x02\x84\x05\x02\x84')
		defn_exported["location"] = defn_max_no
	elif name == "course":
		fit_data.extend(btarr_number(defn_max_no+64, 1))
		fit_data.extend(b'\x00\x00\x1F\x00\x03')
		fit_data.extend(b'\x05\x10\x07\x06\x04\x8C\x04\x01\x00')
	elif name == "lap":
		fit_data.extend(btarr_number(defn_max_no+64, 1))
		fit_data.extend(b'\x00\x00\x13\x00\x58\xFD\x04\x86\x02\x04\x86\x03\x04\x85\x04\x04\x85\x05\x04\x85')
		fit_data.extend(b'\x06\x04\x85\x07\x04\x86\x08\x04\x86\x09\x04\x86\x0A\x04\x86\x1B\x04\x85\x1C\x04')
		fit_data.extend(b'\x85\x1D\x04\x85\x1E\x04\x85\x29\x04\x86\x46\x04\x86\x62\x04\x86\x66\x04\x02\x67')
		fit_data.extend(b'\x04\x02\x68\x04\x02\x69\x04\x02\x6A\x04\x84\x6B\x04\x84\x6E\x04\x86\x6F\x04\x86')
		fit_data.extend(b'\x70\x04\x86\x71\x04\x86\x72\x04\x86\xFE\x02\x84\x0B\x02\x84\x0C\x02\x84\x0D\x02')
		fit_data.extend(b'\x84\x0E\x02\x84\x13\x02\x84\x14\x02\x84\x15\x02\x84\x16\x02\x84\x20\x02\x84\x21')
		fit_data.extend(b'\x02\x84\x22\x02\x84\x23\x02\x84\x25\x02\x84\x28\x02\x84\x47\x02\x84\x49\x02\x84')
		fit_data.extend(b'\x4D\x02\x84\x4E\x02\x84\x4F\x02\x84\x5A\x02\x84\x60\x02\x84\x61\x02\x84\x63\x02')
		fit_data.extend(b'\x84\x76\x02\x84\x77\x02\x84\x78\x02\x84\x7D\x02\x84\x7E\x02\x84\x88\x02\x84\x89')
		fit_data.extend(b'\x02\x84\x9B\x02\x84\x00\x01\x00\x01\x01\x00\x0F\x01\x02\x10\x01\x02\x11\x01\x02')
		fit_data.extend(b'\x12\x01\x02\x17\x01\x00\x18\x01\x00\x19\x01\x00\x1A\x01\x02\x26\x01\x00\x27\x01')
		fit_data.extend(b'\x00\x32\x01\x01\x33\x01\x01\x48\x01\x00\x50\x01\x02\x51\x01\x02\x52\x01\x02\x5B')
		fit_data.extend(b'\x01\x02\x5C\x01\x02\x5D\x01\x02\x5E\x01\x02\x5F\x01\x02\x64\x01\x01\x65\x01\x01')
		fit_data.extend(b'\x6C\x02\x02\x6D\x02\x02\x7C\x01\x01')
	elif name == "event":
		fit_data.extend(btarr_number(defn_max_no+64, 1))
		fit_data.extend(b'\x00\x00\x15\x00\x07')
		fit_data.extend(b'\xFD\x04\x86\x03\x04\x86\x00\x01\x00\x01\x01\x00')
		fit_data.extend(b'\x04\x01\x02\x13\x01\x02\x14\x01\x02')
	elif name == "record":
		fit_data.extend(btarr_number(defn_max_no+64, 1))
		fit_data.extend(b'\x00\x00\x14\x00\x36\xFD\x04\x86\x00\x04\x85\x01\x04\x85\x05\x04\x86\x0B\x04\x85')
		fit_data.extend(b'\x1D\x04\x86\x49\x04\x86\x4A\x04\x86\x4B\x04\x86\x4C\x04\x86\x4D\x04\x86\x4E\x04')
		fit_data.extend(b'\x86\x4F\x04\x86\x50\x04\x86\x02\x02\x84\x06\x02\x84\x07\x02\x84\x27\x02\x84\x28')
		fit_data.extend(b'\x02\x84\x29\x02\x84\x36\x02\x84\x39\x02\x84\x3D\x02\x84\x3F\x02\x84\x40\x02\x84')
		fit_data.extend(b'\x41\x02\x84\x42\x02\x83\x53\x02\x84\x54\x02\x84\x55\x02\x84\x57\x02\x84\x58\x02')
		fit_data.extend(b'\x84\x6C\x02\x84\x74\x02\x84\x03\x01\x02\x04\x01\x02\x0D\x01\x01\x12\x01\x02\x1E')
		fit_data.extend(b'\x01\x02\x2A\x01\x00\x2B\x01\x02\x2C\x01\x02\x2D\x01\x02\x2E\x01\x02\x2F\x01\x02')
		fit_data.extend(b'\x35\x01\x02\x43\x01\x01\x44\x01\x01\x45\x02\x02\x46\x02\x02\x47\x02\x02\x48\x02')
		fit_data.extend(b'\x02\x5A\x01\x01\x88\x01\x02')
	elif name == "course_point":
		fit_data.extend(btarr_number(defn_max_no+64, 1))
		fit_data.extend(b'\x00\x00\x20\x00\x08')
		fit_data.extend(b'\x01\x04\x86\x02\x04\x85\x03\x04\x85\x04\x04\x86')
		fit_data.extend(b'\x06\x10\x07\xFE\x02\x84\x05\x01\x00\x07\x21\x07')
	else:
		sys.exit('Fatal error: ' + name + ' is an unknown identifier')
	defn_exported[name] = defn_max_no
	return btarr_number(defn_max_no, 1)

def fit_header():
	"""
	create the header of the fit file
	also reset all global variables in case of this is not the first and only fit file to write
	the datasize has to be left empty, since it is not known yet
	"""
	global fit_data
	global defn_exported
	global defn_max_no
	# reset definitions
	defn_exported = dict()
	defn_max_no = -1
	# create a 14-bit fit-header
	fit_data[::] = b''
	fit_data.extend(b'\x0E\x10\x5D\x08\x00\x00\x00\x00\x2E\x46\x49\x54\x00\x00')
	# to be filled, when finished:    |<--datasize-->|

def fit_completed():
	"""
	complete the fit file
	in this function, the datasize of the header is claculated
	also the crc-checksum is calculated and appended at the end
	"""
	# update data size in header
	dt_size = len(fit_data) - 14
	for n, sbt in enumerate(btarr_number(dt_size, 4)):
		fit_data[n+4] = sbt
	# add crc checksum
	crc_table = (0x0000, 0xCC01, 0xD801, 0x1400, 0xF001, 0x3C00, 0x2800, 0xE401,
	             0xA001, 0x6C00, 0x7800, 0xB401, 0x5000, 0x9C01, 0x8801, 0x4400)
	crc = 0
	for bt in fit_data:
		tmp = crc_table[crc & 0xF]
		crc = (crc >> 4) & 0x0FFF
		crc = crc ^ tmp ^ crc_table[bt & 0xF]
		tmp = crc_table[crc & 0xF]
		crc = (crc >> 4) & 0x0FFF
		crc = crc ^ tmp ^ crc_table[(bt >> 4) & 0xF]
	fit_data.extend(btarr_number(crc, 2))

def fit_write2disk(filename):
	"""
	write a finished fit array to disk
	"""
	with open(filename, "wb") as fp:
		# Write bytes to file
		fp.write(fit_data)


def fit_file_id(file_type):
	"""
	create the data message for the file_id
	this is necessary once at the start of the file
	the type-no for waypoint / location is:	file-type = 8
	the type-no for route / course is:		file-type = 6
	"""
	fit_data.extend( message_definition_id ("file_id") )
	fit_data.extend(b'\xC4\x07\x5D\xC9\x99\xF1\x15\x3C\xFF')
	fit_data.extend(b'\xFF\xFF\xFF\xFF\x00\x36\x0C\xFF\xFF')
	fit_data.extend(btarr_number(file_type, 1))

def fit_location(name, lat, lon, count):
	"""
	create the data message for a waypoint
	"""
	fit_data.extend( message_definition_id ("location") )
	fit_data.extend(b'\xFF\xFF\xFF\xFF')
	# waypoint (location) name
	fit_data.extend(btarr_string(name, 16))
	# coordinate
	fit_data.extend(btarr_coord(lat))
	fit_data.extend(btarr_coord(lon))
	# internal number (must be incremented)
	fit_data.extend(btarr_number(count, 2))
	fit_data.extend(b'\xFF\xFF\xAF\x0B\xFF\xFF')
	#                         | symbol
	# waypoint symbols are not yet implemented

def fit_course(name):
	"""
	create a data message for a course
	this belongs to a route header
	"""
	fit_data.extend( message_definition_id ("course") )
	# route (course) name
	fit_data.extend(btarr_string(name, 16))
	#fit_data.extend(b'\x03\x02\x00\x00\xFF')
	fit_data.extend(b'\x03\x02\x00\x00\x11')	# x11 = hiking

def fit_lap(time_stamp, lat1, lon1, lat2, lon2, distance):
	"""
	create a data message for a lap
	this belongs to a route header
	"""
	fit_data.extend( message_definition_id ("lap") )
	fit_data.extend(btarr_timestamp(time_stamp))
	fit_data.extend(btarr_timestamp(time_stamp))
	# start point
	fit_data.extend(btarr_coord(lat1))
	fit_data.extend(btarr_coord(lon1))
	# destination point
	fit_data.extend(btarr_coord(lat2))
	fit_data.extend(btarr_coord(lon2))
	# 4-byte total-elapsed-time
	fit_data.extend(b'\xFF\xFF\xFF\xFF')
	# 4-byte total-timer-time (seems to be in ms)
	# I'd calculated the walking time by assuming 4 km/h speed
	fit_data.extend(btarr_number(900 * distance, 4))
	# 4-byte total-distance (seems to be in cm)
	fit_data.extend(btarr_number(100 * distance, 4))
	# 4-byte total-cycles		0xffff
	fit_data.extend(b'\xFF\xFF\xFF\xFF')
	fit_data.extend(b'\x01\xD9\x8D\x24\x6D\xEF\x3E\x05\xD8\xD0\x8C\x24\x32\x72\x3E\x05\xFF\xFF\xFF\xFF')
	fit_data.extend(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
	fit_data.extend(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
	fit_data.extend(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF\xF4\x14')
	fit_data.extend(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
	fit_data.extend(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
	fit_data.extend(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x09\x01\xFF\xFF')
	fit_data.extend(b'\xFF\xFF\xFF\x07\xFF\xFF\xFF\xFF\x7F\x7F\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x7F')
	fit_data.extend(b'\x7F\xFF\xFF\xFF\xFF\x7F')

def fit_event(is_start):
	"""
	create a data message for an event
	this needs to be once at the start and the end of a route
	"""
	fit_data.extend( message_definition_id ("event") )
	if (is_start):      # |<- timestamp ->|
		fit_data.extend(b'\x99\xF1\x15\x3C\x00\x00\x00\x00\x00\x00\x00\xFF\xFF')
	else:
		fit_data.extend(b'\x80\xF2\x15\x3C\x00\x00\x00\x00\x00\x04\x00\xFF\xFF')

def fit_record(time_stamp, lat, lon, distance):
	"""
	create the data message for a route-point
	"""
	fit_data.extend( message_definition_id ("record") )
	fit_data.extend(btarr_timestamp(time_stamp))
	fit_data.extend(btarr_coord(lat))
	fit_data.extend(btarr_coord(lon))
	fit_data.extend(btarr_number(100 * distance, 4))	# distance in cm
	fit_data.extend(b'\xFF\xFF\xFF\x7F')
	fit_data.extend(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
	fit_data.extend(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
	fit_data.extend(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
	fit_data.extend(b'\xFF\x7F\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x7F\xFF')
	fit_data.extend(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x7F\x7F\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x7F\xFF')

def fit_course_point(time_stamp, name, lat, lon):
	"""
	create the data message for a course-point
	a point of special interest on the course
	I haven't implemented this yet
	"""
	fit_data.extend( message_definition_id ("course_point") )
	fit_data.extend(btarr_timestamp(time_stamp))
	fit_data.extend(btarr_coord(lat))
	fit_data.extend(btarr_coord(lon))
	fit_data.extend(b'\x00\x00\x00\x00')
	fit_data.extend(btarr_string(name, 16))
	fit_data.extend(b'\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
	fit_data.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
	fit_data.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')


def point_distance(x1, y1, x2, y2):
	"""
	calculate the great circle distance of two points
	I added 4% considering the "curviness" of a real-world route
	"""
	# convert to radians
	x1 = math.radians(x1)
	y1 = math.radians(y1)
	x2 = math.radians(x2)
	y2 = math.radians(y2)
	# great circle distance in radians
	angle = math.acos(math.sin(x1) * math.sin(x2) + math.cos(x1) * math.cos(x2) * math.cos(y1 - y2))
	return int(1.04 * 111222 * math.degrees(angle))

def calc_route_distances(coords):
	"""
	extend an array of adjacent coordinates with their distances
	calculated from the start point
	"""
	distance = 0
	last_lat = -1000
	last_lon = -1000
	for coord in coords:
		if last_lat != -1000:
			distance += point_distance(coord["lat"], coord["lon"], last_lat, last_lon)
		last_lat = coord["lat"]
		last_lon = coord["lon"]
		coord["dist"] = distance
	return distance


# global timestamp
g_timestamp = int(time.time())

def nodeName(xmlNode):
	"""
	extract the nodename from a xml-node
	namespace is stripped if necessary
	"""
	ndname = xmlNode.tag
	if '}' in ndname:
		ndname = ndname.split('}', 1)[1]
	return ndname

def convert_gpx_to_fit (file_path):
	"""
	the main conversion function used for one gpx file
	may create a number of fit files as output
	"""
	filename, file_extension = os.path.splitext(file_path)
	waypt_no = 0	# internal fit-file waypoint-number, must be incremented
	route_no = 0
	waypt_coords = []

	try:
		root = xml.etree.ElementTree.parse(file_path).getroot()
	except Exception:
		print(" ... upps: '" + filename + "' doesn't seem to be a valid gpx-file.", file=sys.stderr)
		return

	print (">-> converting", file_path)

	for child in root:
		if nodeName(child) == "rte":
			route_coords = []
			route_name = "R{:03d}".format(route_no+1)
			for data in child:
				if nodeName(data) == "rtept":
					lat = float(data.attrib['lat'])
					lon = float(data.attrib['lon'])
					route_coords.append( {"lon": lon, "lat": lat, "dist": -1} )
				elif nodeName(data) == "name":
					route_name = data.text
			if len(route_coords) > 0:
				fit_header()
				fit_file_id(6)
				fit_course(route_name)
				calc_route_distances(route_coords)
				fit_lap(g_timestamp, route_coords[0] ["lat"], route_coords[0] ["lon"],
									 route_coords[-1]["lat"], route_coords[-1]["lon"],
									 route_coords[-1]["dist"])
				fit_event(True)
				for coord in route_coords:
					fit_record(g_timestamp, coord["lat"], coord["lon"], coord["dist"])
				fit_event(False)
				fit_completed()
				route_no += 1
				file_path = filename + "-rt{:02d}.fit".format(route_no)
				print (" >> writing", file_path)
				fit_write2disk(file_path)
		elif nodeName(child) == "wpt":
			lat, lon = 0, 0
			wpt_name = "W{:03d}".format(waypt_no+1)
			for data in child:
				if nodeName(data) == "name":
					wpt_name = data.text
			lat = float(child.attrib['lat'])
			lon = float(child.attrib['lon'])
			waypt_coords.append( {'name': wpt_name, 'lat': lat, 'lon': lon} )
			waypt_no += 1

	if len(waypt_coords) > 0:
		fit_header()
		fit_file_id(8)
		for n in range(0, waypt_no):
			fit_location(waypt_coords[n]['name'], waypt_coords[n]['lat'], waypt_coords[n]['lon'], n)
		fit_completed()
		file_path = filename + "-wpts.fit"
		print (" >> writing", file_path)
		fit_write2disk(file_path)


if len(sys.argv) >= 2:
	if len(sys.argv) == 2 and sys.argv[1] in ("-h", "--help"):
		print ("convert routes and waypoints from a gpx-file to Garmin's fit-format", file=sys.stderr)
		print ("if no arguments given, process all gpx-files in the current directory", file=sys.stderr)
		print ("usage: " + os.path.basename(sys.argv[0]) + " [gpx-file-names]", file=sys.stderr)
	else:
		for fn in sys.argv[1:]:
			if os.path.isfile (fn):
				convert_gpx_to_fit (fn)
			else:
				print ("error:", fn, "is not a file", file=sys.stderr)
else:
	for fn in glob.glob ("*.gpx"):
		convert_gpx_to_fit (fn)

