-- AI Content Factory - Seed Prompts
-- Version: 1.0.0
-- Description: Initialize 6 system built-in prompts

-- ==================== Topic Recommendation ====================

INSERT INTO prompts (name, display_name, description, template, variables, output_format, category, is_system, is_active) VALUES
('topic_recommendation', 'Topic Recommendation', 'Recommend 3-5 topics based on search results',
'You are a senior content planning expert, skilled in digging up hot topics.

Please recommend 3-5 attractive topics based on the following search results:

{search_results}

Each topic should include (in JSON format):
- title: Topic title (within 20 Chinese characters)
- type: Topic type (practical/viewpoint/story/review)
- advantage: Topic advantage (within 50 Chinese characters)
- rating: Recommendation level (1-5 stars)

Requirements:
1. Topics should be differentiated and cover different angles
2. Consider target audience interests
3. Evaluate creation difficulty and viral potential

Output only JSON array, no other content.',
'["search_results"]', 'json', 'topic', 1, 1);

-- ==================== Douyin Script ====================

INSERT INTO prompts (name, display_name, description, template, variables, output_format, category, is_system, is_active) VALUES
('douyin_script', 'Douyin Script', 'Create Douyin spoken scripts',
'You are a Douyin viral content creator, skilled in creating high-completion-rate spoken scripts.

Please create a Douyin spoken script based on the following information:
- Topic: {topic}
- Theme: {theme}

Requirements:
1. Word count: 500-600 Chinese characters
2. Style: Colloquial, down-to-earth
3. Structure:
   - Opening 3 seconds: Pain point/surprise/contrast
   - Middle: Valuable content/emotional value
   - Ending: Call to action (like/comment/follow)
4. Suitable for on-camera spoken delivery
5. Avoid sensitive words and prohibited terms

Output only the script content, no other explanation.',
'["topic", "theme"]', 'text', 'douyin', 1, 1);

-- ==================== WeChat Article ====================

INSERT INTO prompts (name, display_name, description, template, variables, output_format, category, is_system, is_active) VALUES
('wechat_article', 'WeChat Article', 'Create in-depth WeChat official account articles',
'You are a WeChat official account viral article author, skilled in creating in-depth long-form content.

Please create a WeChat official account article based on the following information:
- Topic: {topic}
- Theme: {theme}

Requirements:
1. Word count: Around 2000 Chinese characters
2. Format: Markdown
3. Structure:
   - Introduction: 100-200 characters, introduce the topic
   - Body: 3-5 subheadings, each 400-500 characters
   - Conclusion: 100-200 characters, summarize and elevate
4. Clear viewpoint, sufficient evidence
5. Suitable for WeChat official account reading experience (short paragraphs, more line breaks)

Output only the article content, no other explanation.',
'["topic", "theme"]', 'markdown', 'wechat', 1, 1);

-- ==================== Xiaohongshu Note ====================

INSERT INTO prompts (name, display_name, description, template, variables, output_format, category, is_system, is_active) VALUES
('xiaohongshu_note', 'Xiaohongshu Note', 'Create Xiaohongshu viral notes',
'You are a Xiaohongshu viral note creator, skilled in creating high-engagement notes.

Please create a Xiaohongshu note based on the following information:
- Topic: {topic}
- Theme: {theme}

Requirements:
1. Style: Lively, friendly, with emoji
2. Structure:
   - Title: Within 20 characters, eye-catching
   - Body: 300-500 characters, clear paragraphs
   - Tags: 5-10 related hashtags
3. Use emoji to enhance visual appeal
4. Ending call to action (save/like/comment)
5. Match Xiaohongshu community tone

Output only the note content, no other explanation.',
'["topic", "theme"]', 'text', 'xhs', 1, 1);

-- ==================== WeChat Cover Image ====================

INSERT INTO prompts (name, display_name, description, template, variables, output_format, category, is_system, is_active) VALUES
('wechat_cover', 'WeChat Cover', 'Generate WeChat official account cover images',
'Please generate a WeChat official account article cover image based on the following content.

Content topic: {topic}
Article title: {title}
Article style: {style}

Requirements:
1. Aspect ratio: 16:9
2. Style: Clean, professional
3. Include text: {title}
4. Suitable for WeChat official account cover dimensions

Describe the visual content for AI image generation.',
'["topic", "title", "style"]', 'text', 'image', 1, 1);

-- ==================== Xiaohongshu Cover Image ====================

INSERT INTO prompts (name, display_name, description, template, variables, output_format, category, is_system, is_active) VALUES
('xhs_cover', 'Xiaohongshu Cover', 'Generate Xiaohongshu cover images',
'Please generate a Xiaohongshu note cover image based on the following content.

Content topic: {topic}
Note title: {title}
Note style: {style}

Requirements:
1. Aspect ratio: 3:4
2. Style: Lively, eye-catching
3. Include text: {title}
4. Suitable for Xiaohongshu cover dimensions

Describe the visual content for AI image generation.',
'["topic", "title", "style"]', 'text', 'image', 1, 1);
