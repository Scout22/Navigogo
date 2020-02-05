CREATE TABLE IF NOT EXISTS `users` (
	`id` int(10) NOT NULL auto_increment,
	`first_name` varchar(255),
	`last_nam` varchar(255),
	`email` varchar(255),
	`navigo_token` varchar(255),
	`navigo_pass_id` BIGINT,
	`functional` BOOLEAN,
	`created_at` TIMESTAMP,
	PRIMARY KEY( `id` )
);