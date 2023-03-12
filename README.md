# move-simulator

A fun-project made to work with my distance-tracker. A sensor or device provides data about how much distance has been covered. No additional information like latitude or longitude are provided because the sensor won't have a GPS with it. This simulator inetgrates with the sensor, takes a desired start and stop point from user and shows live update based on sensor reading on the path from start to stop point in a map.

# Design

The system requires following data to be successful:
1. [Start-Stop Coordinates](#start-stop-coordinates)
1. [Route Coordinates](#route-coordinates)

## Start-Stop Coordinates

Start and stop coordinates provides latitude and longitude of beginning and destination. As latitude and longitude are not intuitive, coordinates are derived from start and destination address. To achieve this, [reverse-geocoding](https://github.com/mosteligible/reverse-geocoding) has been used.

## Route Coordinates

The latitude and longitude of route from start to stop coordinates are calculated with the help of [routing-engine](https://github.com/mosteligible/routing-engine). Routing engine provides the best path to take from start to stop coordinate in form of latitude and longitude coordinates.

## Implementation Overview

The implementation will work as shown in the diagram below:

![Implementation](./docs/move-simulator.png)
