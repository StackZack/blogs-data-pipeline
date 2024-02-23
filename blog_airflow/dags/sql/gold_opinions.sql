MERGE INTO {{ params.gold_schema }}.opinions gld
USING {{ params.stage_schema }}.stg_opinions stg
ON gld.opinion_id = stg.opinion_id
WHEN MATCHED THEN
	UPDATE SET
	opinion = CAST(stg.opinion AS BOOLEAN)
WHEN NOT MATCHED THEN
	INSERT VALUES(
		stg.opinion_id,
		CAST(stg.opinion AS BOOLEAN)
	);

INSERT INTO {{ params.gold_schema }}.blog_activity(
	blog_id, user_id, comment_id, favorite_id, opinion_id
)
SELECT
	stg.blog_id,
	stg.user_id,
	NULL,
	NULL,
	stg.opinion_id
FROM {{ params.stage_schema }}.stg_opinions stg
LEFT JOIN {{ params.gold_schema }}.blog_activity gld
	ON gld.blog_id = stg.blog_id
	AND gld.user_id = stg.user_id
	AND gld.opinion_id = stg.opinion_id
WHERE gld.blog_activity_id IS NULL;
