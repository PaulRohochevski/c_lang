CREATE SCHEMA bank
  AUTHORIZATION postgres;

CREATE TABLE bank.user_credentials
(
  user_id       SERIAL,
  user_login    VARCHAR,
  user_password VARCHAR,
  CONSTRAINT user_credentials_user_id_pkey PRIMARY KEY (user_id)
);

CREATE TABLE bank.user_account
(
  account_id SERIAL,
  user_id    INTEGER,
  money      DOUBLE PRECISION,
  CONSTRAINT user_account_account_id_pkey PRIMARY KEY (account_id),
  CONSTRAINT user_account_user_id_fkey FOREIGN KEY (user_id) REFERENCES bank.user_credentials (user_id)
);

CREATE TABLE bank.user_credit
(
  credit_id       SERIAL,
  account_id      INTEGER,
  money           DOUBLE PRECISION,
  interest_rate   DOUBLE PRECISION,
  expiration_date DATE,
  CONSTRAINT user_credit_credit_id_pkey PRIMARY KEY (credit_id),
  CONSTRAINT user_credit_account_id_fkey FOREIGN KEY (account_id) REFERENCES bank.user_account (account_id)
);

CREATE TABLE bank.user_deposit
(
  deposit_id SERIAL,
  account_id INTEGER,
    money           DOUBLE PRECISION,
  interest_rate   DOUBLE PRECISION,
  expiration_date DATE,
  CONSTRAINT user_deposit_deposit_id_pkey PRIMARY KEY (deposit_id),
  CONSTRAINT user_deposit_account_id_fkey FOREIGN KEY (account_id) REFERENCES bank.user_account (account_id)
);

CREATE OR REPLACE FUNCTION bank.get_password_by_login(login VARCHAR)
  RETURNS VARCHAR AS
$BODY$
DECLARE
  psw VARCHAR;
BEGIN
  SELECT user_password
  FROM bank.user_credentials
  WHERE user_login = login
  INTO psw;

  IF ((login IN (SELECT user_login
                 FROM bank.user_credentials)) AND (psw IS NOT NULL))
  THEN RETURN psw;

  ELSEIF login NOT IN (SELECT user_login
                       FROM bank.user_credentials)
    THEN RETURN '1';

  ELSE
    RETURN '2';

  END IF;
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;


CREATE OR REPLACE FUNCTION bank.sign_up_new_user(login VARCHAR, password VARCHAR)
  RETURNS VARCHAR AS
$BODY$
BEGIN

  IF login IN (SELECT user_login
               FROM bank.user_credentials)
  THEN RETURN '1';

  ELSE
    INSERT INTO bank.user_credentials VALUES (DEFAULT, login, password);
    RETURN '0';

  END IF;
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;