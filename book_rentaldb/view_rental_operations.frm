TYPE=VIEW
query=select `r`.`id` AS `rental_id`,`u`.`name` AS `borrower_name`,`b`.`title` AS `book_title`,`r`.`rented_at` AS `rented_at`,`r`.`rented_at` + interval 7 day AS `due_date`,to_days(current_timestamp()) - to_days(`r`.`rented_at`) AS `days_elapsed`,case when `r`.`returned_at` is not null then \'Closed\' when to_days(current_timestamp()) - to_days(`r`.`rented_at`) > 7 then \'Overdue\' else \'Active\' end AS `status`,case when `r`.`returned_at` is null and to_days(current_timestamp()) - to_days(`r`.`rented_at`) > 7 then (to_days(current_timestamp()) - to_days(`r`.`rented_at`) - 7) * 10.00 else 0 end AS `fine_amount` from ((`book_rentaldb`.`rentals` `r` join `book_rentaldb`.`users` `u` on(`r`.`user_id` = `u`.`id`)) join `book_rentaldb`.`books` `b` on(`r`.`book_id` = `b`.`id`)) order by `r`.`rented_at` desc
md5=24544a0b2033eac527abb1931d1fd123
updatable=1
algorithm=0
definer_user=root
definer_host=localhost
suid=2
with_check_option=0
timestamp=0001765712210176003
create-version=2
source=SELECT \n    r.id AS rental_id,\n    u.name AS borrower_name,\n    b.title AS book_title,\n    r.rented_at,\n    \n    \n    \n    DATE_ADD(r.rented_at, INTERVAL 7 DAY) AS due_date,\n    \n    \n    \n    DATEDIFF(NOW(), r.rented_at) AS days_elapsed,\n    \n    \n    CASE \n        WHEN r.returned_at IS NOT NULL THEN \'Closed\'\n        WHEN DATEDIFF(NOW(), r.rented_at) > 7 THEN \'Overdue\' \n        ELSE \'Active\' \n    END AS status,\n\n    \n    CASE \n        WHEN r.returned_at IS NULL AND DATEDIFF(NOW(), r.rented_at) > 7 \n        THEN (DATEDIFF(NOW(), r.rented_at) - 7) * 10.00\n        ELSE 0 \n    END AS fine_amount\n\nFROM rentals r\nJOIN users u ON r.user_id = u.id\nJOIN books b ON r.book_id = b.id\nORDER BY r.rented_at DESC
client_cs_name=utf8mb4
connection_cl_name=utf8mb4_general_ci
view_body_utf8=select `r`.`id` AS `rental_id`,`u`.`name` AS `borrower_name`,`b`.`title` AS `book_title`,`r`.`rented_at` AS `rented_at`,`r`.`rented_at` + interval 7 day AS `due_date`,to_days(current_timestamp()) - to_days(`r`.`rented_at`) AS `days_elapsed`,case when `r`.`returned_at` is not null then \'Closed\' when to_days(current_timestamp()) - to_days(`r`.`rented_at`) > 7 then \'Overdue\' else \'Active\' end AS `status`,case when `r`.`returned_at` is null and to_days(current_timestamp()) - to_days(`r`.`rented_at`) > 7 then (to_days(current_timestamp()) - to_days(`r`.`rented_at`) - 7) * 10.00 else 0 end AS `fine_amount` from ((`book_rentaldb`.`rentals` `r` join `book_rentaldb`.`users` `u` on(`r`.`user_id` = `u`.`id`)) join `book_rentaldb`.`books` `b` on(`r`.`book_id` = `b`.`id`)) order by `r`.`rented_at` desc
mariadb-version=100432
