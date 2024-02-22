WITH blog_tag_ids AS (
	SELECT blog_id, ARRAY_AGG(tag_id) tag_ids
	FROM {{ params.stage_schema }}.stg_blog_tags
	GROUP BY 1
)
MERGE INTO {{ params.gold_schema }}.blogs gld
USING (
	SELECT
		sb.blog_id,
		bti.tag_ids,
		sb.title,
		sb.content
	FROM {{ params.stage_schema }}.stg_blogs sb
	LEFT JOIN blog_tag_ids bti
		ON sb.blog_id = bti.blog_id
) stg
ON gld.blog_id = stg.blog_id
WHEN MATCHED THEN
	UPDATE SET
	blog_id = stg.blog_id,
	tag_ids = stg.tag_ids,
	title = stg.title,
	content = stg.content
WHEN NOT MATCHED THEN
	INSERT VALUES(
		stg.blog_id,
		stg.tag_ids,
		stg.title,
		stg.content
	);

INSERT INTO {{ params.gold_schema }}.blog_activity(
	blog_id, user_id, comment_id, favorite_id, opinion_id
)
SELECT
	stg.blog_id,
	stg.user_id,
	NULL,
	NULL,
	NULL
FROM {{ params.stage_schema }}.stg_opinions stg
LEFT JOIN {{ params.gold_schema }}.blog_activity gld
	ON gld.blog_id = stg.blog_id
	AND gld.user_id = stg.user_id
	AND gld.comment_id IS NULL
	AND gld.favorite_id IS NULL
	AND gld.opinion_id IS NULL
WHERE gld.blog_activity_id IS NULL;
