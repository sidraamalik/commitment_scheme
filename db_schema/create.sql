CREATE DATABASE IF NOT EXISTS commitment_scheme;
USE commitment_scheme;

CREATE TABLE IF NOT EXISTS keypair(
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uid INT(10) UNSIGNED,
    private_key VARCHAR(2500),
    public_key VARCHAR(1000),
    UNIQUE (uid)
);
CREATE TABLE IF NOT EXISTS user(
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(256),
    password VARCHAR(256),
    UNIQUE (username)
);
CREATE TABLE IF NOT EXISTS message(
    id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uid INT(10) UNSIGNED,
    message VARCHAR(2048),
    signature VARCHAR(512),
    message_type INT(2) DEFAULT 1
);
