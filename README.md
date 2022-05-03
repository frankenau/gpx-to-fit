This is a very basic command line tool for converting gpx-files to fit-files written in Python 3. It's designed to run under any operating system Python 3 runs on.

The GPS Exchange Format, **GPX**, is a widely used format to exchange geographical data between programs. As a text/xml format, it's user readable too. For further information please refer this [Wikipedia article](https://en.wikipedia.org/wiki/GPS_Exchange_Format).

The **FIT** file format is a Garmin specific format used to exchange data between fitness watches of this manufacturer or accessories. These files may also contain geographical data. As binary files, they may not be as readable as gpx-files. A good overview about this abstract can be found at the developer [Garmin website](https://developer.garmin.com/fit/overview/).

The task of this utility is to parse a gpx-file and extract all routes and waypoints in this file. This data will be written to a number of fit files containing these routes and waypoints.

Say, you have a file *sample.gpx* containing some waypoints "WPT1, WPT2, ... WPTn" and 2 routes named "Route-1, Route-2". By converting it, using "**$ gpx-to-fit sample.gpx**", you should get 3 output files: "*Route-1\_course.fit*, *Route-2\_course.fit* and *sample-wpts.fit*". The first two contain your routes, the last file will contain the waypoints.

These files are ready to be copied on your watch. Use the *Courses*-folder for the route-files and the *Location*-folder for the waypoint-file.

You should then be able to use them for navigation (e.g. hiking).

Please note: There is absolutely no warranty given, that this program will work. If your expensive new watch (or your computer) will crash for good, it's your risk. If you got lost in the mountains, it's your problem too. No liability is taken by the author of this program. This is a pure hobby project without economic interest. Furthermore the author doesn't have (or ever had) any links to the Garmin corporation or any company linked to Garmin.

