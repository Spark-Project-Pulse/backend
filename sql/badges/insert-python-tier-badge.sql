-- Start a transaction to ensure atomicity
BEGIN;

-- Step 1: Insert the Python tag if it does not already exist
WITH
  existing_tag AS (
    SELECT
      tag_id
    FROM
      "Tags"
    WHERE
      name = 'Python'
  ),
  inserted_tag AS (
    INSERT INTO
      "Tags" (tag_id, name, created_at, updated_at)
    SELECT
      gen_random_uuid (),
      'Python',
      NOW(),
      NOW()
    WHERE
      NOT EXISTS (
        SELECT
          1
        FROM
          "Tags"
        WHERE
          name = 'Python'
      )
    RETURNING
      tag_id
  )
SELECT
  tag_id INTO TEMPORARY TABLE python_tag
FROM
  (
    SELECT
      tag_id
    FROM
      existing_tag
    UNION ALL
    SELECT
      tag_id
    FROM
      inserted_tag
  ) combined;

-- Step 2: Insert the Python Pro badge
WITH
  inserted_badge AS (
    INSERT INTO
      "Badges" (
        badge_id,
        name,
        description,
        is_global,
        created_at,
        image_url,
        associated_tag_id
      )
    VALUES
      (
        gen_random_uuid (),
        'Python Pro',
        'Earn reputation by contributing to Python-tagged questions.',
        FALSE,
        NOW(),
        'https://cdn-icons-png.flaticon.com/512/20/20100.png',
        (
          SELECT
            tag_id
          FROM
            python_tag
          LIMIT
            1
        )
      )
    RETURNING
      badge_id
  )
  -- Step 3: Insert the three tiers for Python Pro
INSERT INTO
  "BadgeTier" (
    id,
    tier_level,
    badge_id,
    name,
    description,
    image_url,
    reputation_threshold
  )
SELECT
  gen_random_uuid (),
  tiers.tier_level,
  inserted_badge.badge_id,
  tiers.tier_name,
  tiers.tier_description,
  tiers.tier_image_url,
  tiers.reputation_threshold
FROM
  inserted_badge
  CROSS JOIN (
    VALUES
      (
        1,
        'Python Pro I',
        'Achieve 5 reputation in Python-tagged questions.',
        'https://cdn-icons-png.flaticon.com/512/20/20100.png',
        5
      ),
      (
        2,
        'Python Pro II',
        'Achieve 10 reputation in Python-tagged questions.',
        'https://cdn-icons-png.flaticon.com/512/20/20100.png',
        10
      ),
      (
        3,
        'Python Pro III',
        'Achieve 15 reputation in Python-tagged questions.',
        'https://cdn-icons-png.flaticon.com/512/20/20100.png',
        15
      )
  ) AS tiers (
    tier_level,
    tier_name,
    tier_description,
    tier_image_url,
    reputation_threshold
  );

-- Commit the transaction
COMMIT;
