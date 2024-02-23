MERGE INTO {{ params.gold_schema }}.favorites gld
USING {{ params.stage_schema }}.stg_favorites stg
ON gld.favorite_id = stg.favorite_id
WHEN MATCHED THEN
	UPDATE SET
	favorite_date = stg.favorite_date
WHEN NOT MATCHED THEN
	INSERT VALUES(
		stg.favorite_id,
		stg.favorite_date
	);

INSERT INTO {{ params.gold_schema }}.blog_activity(
	blog_id, user_id, comment_id, favorite_id, opinion_id
)
SELECT
	stg.blog_id,
	stg.user_id,
	NULL,
	stg.favorite_id,
	NULL
FROM {{ params.stage_schema }}.stg_favorites stg
LEFT JOIN {{ params.gold_schema }}.blog_activity gld
	ON gld.blog_id = stg.blog_id
	AND gld.user_id = stg.user_id
	AND gld.favorite_id = stg.favorite_id
WHERE gld.blog_activity_id IS NULL;
