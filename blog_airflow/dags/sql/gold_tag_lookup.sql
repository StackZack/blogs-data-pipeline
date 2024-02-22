MERGE INTO {{ params.gold_schema }}.tag_lookup gld
USING {{ params.stage_schema }}.stg_tags stg
ON gld.tag_id = stg.tag_id
WHEN MATCHED THEN
	UPDATE SET
	name = stg.name
WHEN NOT MATCHED THEN
	INSERT VALUES(
		stg.tag_id,
		stg.name
	);
