CREATE TABLE IF NOT EXISTS `sent_attestation` (
	`id` int(10) NOT NULL auto_increment,
	`user_id` int(10),
	`status` BOOLEAN,
	`sent_at` TIMESTAMP,
	PRIMARY KEY( `id` )
);