MERGE INTO {{ params.gold_schema }}.comments gld
USING {{ params.stage_schema }}.stg_comments stg
ON gld.comment_id = stg.comment_id
WHEN MATCHED THEN
	UPDATE SET
	content = stg.content
WHEN NOT MATCHED THEN
	INSERT VALUES(
		stg.comment_id,
		stg.content
	);

INSERT INTO {{ params.gold_schema }}.blog_activity(
	blog_id, user_id, comment_id, favorite_id, opinion_id
)
SELECT
	stg.blog_id,
	stg.user_id,
	stg.comment_id,
	NULL,
	NULL
FROM {{ params.stage_schema }}.stg_comments stg
LEFT JOIN {{ params.gold_schema }}.blog_activity gld
	ON gld.blog_id = stg.blog_id
	AND gld.user_id = stg.user_id
	AND gld.comment_id = stg.comment_id
WHERE gld.blog_activity_id IS NULL;
