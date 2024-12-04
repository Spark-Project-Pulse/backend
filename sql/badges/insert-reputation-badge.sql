-- Start a transaction to ensure atomicity
BEGIN;

-- Insert the new badge 'Reputable Source' without an associated_tag
WITH inserted_badge AS (
  INSERT INTO "Badges" (
    badge_id,       -- Explicitly set the badge_id column
    name, 
    description, 
    is_global, 
    created_at, 
    image_url, 
    associated_tag_id
  )
  VALUES (
    gen_random_uuid(),  -- Generate a UUID for badge_id
    'Reputable Source',
    'Awarded to users who have achieved a significant reputation, demonstrating their expertise and contribution to the community.',
    TRUE,               -- is_global set to TRUE for a global badge
    NOW(),              -- created_at set to current timestamp
    'https://cdn-icons-png.flaticon.com/512/20/20100.png', -- Replace with your actual image URL
    NULL                -- No associated_tag_id since it's a global badge
  )
  RETURNING badge_id
)

-- Insert the three tiers for 'Reputable Source'
INSERT INTO "BadgeTier" (
  id,                  -- Add the id column
  tier_level, 
  badge_id, 
  name, 
  description, 
  image_url, 
  reputation_threshold
)
SELECT 
  gen_random_uuid(),   -- Generate a UUID for id
  tiers.tier_level,
  inserted_badge.badge_id,
  tiers.tier_name,
  tiers.tier_description,
  tiers.tier_image_url,
  tiers.reputation_threshold
FROM inserted_badge
CROSS JOIN (
  VALUES
    (1, 'Reputable Source I', 'Achieved a reputation of 5.', 'https://cdn-icons-png.flaticon.com/512/20/20100.png', 5),
    (2, 'Reputable Source II', 'Achieved a reputation of 10.', 'https://cdn-icons-png.flaticon.com/512/20/20100.png', 10),
    (3, 'Reputable Source III', 'Achieved a reputation of 15.', 'https://cdn-icons-png.flaticon.com/512/20/20100.png', 15)
) AS tiers(tier_level, tier_name, tier_description, tier_image_url, reputation_threshold);

-- Commit the transaction
COMMIT;