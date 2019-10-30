SELECT
    l.name AS name,
    r.total_properties AS total_properties,
    r.average_rent AS average_rent,
    r.rent_under_250 AS rent_under_250,
    r.rent_250_to_500 AS rent_250_to_500,
    d.distance_to_london_text AS distance_to_london_text,
    d.distance_to_london AS distance_to_london,
    d.duration_to_london_text AS duration_to_london_text,
    d.duration_to_london AS duration_to_london,
    s.score AS score
FROM
    location AS l
INNER JOIN
    rental_data AS r
ON
    r.location_name = l.name
INNER JOIN
    distance_matrix_data as d
ON
    d.location_name = l.name
INNER JOIN
    scores as s
ON
    s.location_name = l.name
GROUP BY
    r.location_name,
    r.total_properties,
    r.average_rent,
    r.rent_under_250,
    r.rent_250_to_500,
    r.datetime,
    d.location_name,
    d.distance_to_london,
    d.duration_to_london,
    d.distance_to_london_text,
    d.duration_to_london_text,
    d.datetime,
    s.location_name,
    s.score,
    s.datetime,
    l.name
HAVING
    r.datetime = (
        SELECT
            datetime
        FROM
            rental_data AS ra
        WHERE
            ra.location_name = r.location_name
        ORDER BY
            ra.datetime DESC
        LIMIT 1
    )
AND
    d.datetime = (
        SELECT
            datetime
        FROM
            distance_matrix_data AS da
        WHERE
            da.location_name = d.location_name
        ORDER BY
            da.datetime DESC
        LIMIT 1
    )
AND
    s.datetime = (
        SELECT
            datetime
        FROM
            scores AS sa
        WHERE
            sa.location_name = s.location_name
        ORDER BY
            sa.datetime DESC
        LIMIT 1
    );
