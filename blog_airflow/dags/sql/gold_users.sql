MERGE INTO {{ params.gold_schema }}.users gld
USING {{ params.stage_schema }}.stg_users stg
ON gld.user_id = stg.user_id
WHEN MATCHED THEN
	UPDATE SET
	user_id = stg.user_id,
	first_name = stg.first_name,
	last_name = stg.last_name,
	email = stg.email
WHEN NOT MATCHED THEN
	INSERT VALUES(
		stg.user_id,
		stg.first_name,
		stg.last_name,
		stg.email
	);
