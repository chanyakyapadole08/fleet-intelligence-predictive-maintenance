USE fleet_intelligence;


-- 1. Total number of trucks
SELECT COUNT(*) AS total_trucks
FROM trucks;


-- 2. Total trips and distance
SELECT
    COUNT(*) AS total_trips,
    ROUND(SUM(distance_km), 2) AS total_distance_km
FROM trips;


-- 3. Average fuel efficiency
SELECT
    ROUND(AVG(distance_km / fuel_liters), 2) AS avg_fuel_efficiency
FROM trips;


-- 4. Truck-wise trip performance
SELECT
    truck_id,
    COUNT(*) AS total_trips,
    ROUND(SUM(distance_km), 2) AS total_distance_km,
    ROUND(AVG(distance_km / fuel_liters), 2) AS avg_fuel_efficiency
FROM trips
GROUP BY truck_id
ORDER BY total_distance_km DESC;


-- 5. Delivery performance
SELECT
    delivery_status,
    COUNT(*) AS total_trips,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM trips), 2) AS percentage
FROM trips
GROUP BY delivery_status;


-- 6. Maintenance cost by truck
SELECT
    truck_id,
    COUNT(*) AS maintenance_count,
    ROUND(SUM(repair_cost), 2) AS total_repair_cost,
    ROUND(SUM(downtime_hours), 2) AS total_downtime_hours
FROM maintenance
GROUP BY truck_id
ORDER BY total_repair_cost DESC;


-- 7. Truck + maintenance analysis
SELECT
    t.truck_id,
    t.truck_type,
    t.truck_age_years,
    t.total_mileage_km,
    COUNT(m.maintenance_id) AS maintenance_count,
    COALESCE(SUM(m.repair_cost), 0) AS total_repair_cost
FROM trucks t
LEFT JOIN maintenance m
    ON t.truck_id = m.truck_id
GROUP BY
    t.truck_id,
    t.truck_type,
    t.truck_age_years,
    t.total_mileage_km
ORDER BY total_repair_cost DESC;


-- 8. Route performance
SELECT
    r.route_id,
    r.origin,
    r.destination,
    COUNT(t.trip_id) AS total_trips,
    ROUND(AVG(t.distance_km), 2) AS avg_distance,
    ROUND(AVG(t.travel_time_hours), 2) AS avg_travel_time
FROM routes r
LEFT JOIN trips t
    ON r.route_id = t.route_id
GROUP BY
    r.route_id,
    r.origin,
    r.destination
ORDER BY total_trips DESC;