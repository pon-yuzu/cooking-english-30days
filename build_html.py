#!/usr/bin/env python3
"""
30日間クッキング英語 - HTML生成スクリプト

使い方:
  python build_html.py

content/ フォルダのJSONファイルから、docs/ フォルダにHTMLファイルを生成します。
"""

import json
import os
import re

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Day {day}: {recipe_en} {emoji}</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Hiragino Sans', sans-serif;
      background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 50%, #e8b4cb 100%);
      min-height: 100vh;
      padding: 20px;
    }}
    
    .container {{
      max-width: 700px;
      margin: 0 auto;
    }}
    
    .card {{
      background: white;
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }}
    
    .card-header {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
    }}
    
    .card-number {{
      background: #e8a4b8;
      color: white;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      font-size: 14px;
    }}
    
    .card-title {{
      font-size: 20px;
      font-weight: bold;
      color: #333;
    }}
    
    .card-subtitle {{
      font-size: 14px;
      color: #666;
    }}
    
    h1 {{
      color: white;
      text-align: center;
      margin-bottom: 8px;
      font-size: 28px;
    }}
    
    .day-badge {{
      text-align: center;
      color: rgba(255,255,255,0.9);
      margin-bottom: 24px;
      font-size: 14px;
    }}
    
    .english-text {{
      background: #f8f9fa;
      border-left: 4px solid #e8a4b8;
      padding: 16px;
      margin: 12px 0;
      line-height: 1.8;
      font-size: 16px;
    }}
    
    .english-text p {{
      margin-bottom: 12px;
    }}
    
    .english-text p:last-child {{
      margin-bottom: 0;
    }}
    
    .btn-row {{
      display: flex;
      gap: 8px;
      margin-top: 12px;
      flex-wrap: wrap;
    }}
    
    .btn {{
      padding: 10px 16px;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-size: 14px;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}
    
    .btn-primary {{
      background: #e8a4b8;
      color: white;
    }}
    
    .btn-primary:hover {{
      background: #d4899d;
    }}
    
    .btn-secondary {{
      background: #e9ecef;
      color: #495057;
    }}
    
    .btn-secondary:hover {{
      background: #dee2e6;
    }}
    
    .btn-success {{
      background: #28a745;
      color: white;
    }}
    
    .vocab-section {{
      display: none;
      margin-top: 16px;
      padding: 16px;
      background: #fff3cd;
      border-radius: 8px;
    }}
    
    .vocab-section.show {{
      display: block;
    }}
    
    .vocab-section h4 {{
      margin-bottom: 12px;
      color: #856404;
      font-size: 14px;
    }}
    
    .vocab-item {{
      display: flex;
      align-items: flex-start;
      gap: 8px;
      padding: 8px 0;
      border-bottom: 1px solid rgba(0,0,0,0.1);
    }}
    
    .vocab-item:last-child {{
      border-bottom: none;
    }}
    
    .vocab-item input[type="checkbox"] {{
      margin-top: 4px;
      width: 18px;
      height: 18px;
      cursor: pointer;
    }}
    
    .vocab-word {{
      font-weight: bold;
      color: #e8a4b8;
      min-width: 100px;
    }}
    
    .vocab-meaning {{
      color: #666;
    }}
    
    .quiz-section {{
      background: #e8f4fd;
      padding: 16px;
      border-radius: 8px;
      margin: 12px 0;
    }}
    
    .quiz-question {{
      font-weight: bold;
      margin-bottom: 12px;
      color: #0066cc;
    }}
    
    .quiz-options {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    
    .quiz-option {{
      padding: 12px;
      background: white;
      border: 2px solid #dee2e6;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    
    .quiz-option:hover {{
      border-color: #e8a4b8;
    }}
    
    .quiz-option.selected {{
      border-color: #e8a4b8;
      background: #f0f4ff;
    }}
    
    .quiz-option.correct {{
      border-color: #28a745;
      background: #d4edda;
    }}
    
    .quiz-option.incorrect {{
      border-color: #dc3545;
      background: #f8d7da;
    }}
    
    .quiz-result {{
      margin-top: 12px;
      padding: 12px;
      border-radius: 8px;
      display: none;
    }}
    
    .quiz-result.show {{
      display: block;
    }}
    
    .quiz-result.correct {{
      background: #d4edda;
      color: #155724;
    }}
    
    .quiz-result.incorrect {{
      background: #f8d7da;
      color: #721c24;
    }}
    
    .tips-section {{
      background: #fff;
      padding: 16px;
      border-radius: 8px;
      border: 2px dashed #ffc107;
      line-height: 1.8;
    }}
    
    .tips-section h4 {{
      color: #856404;
      margin-bottom: 8px;
    }}
    
    .tips-section p {{
      line-height: 1.8;
      color: #333;
      margin-bottom: 12px;
    }}
    
    .diary-section textarea {{
      width: 100%;
      min-height: 120px;
      padding: 12px;
      border: 2px solid #dee2e6;
      border-radius: 8px;
      font-size: 16px;
      line-height: 1.6;
      resize: vertical;
      font-family: inherit;
    }}
    
    .diary-section textarea:focus {{
      outline: none;
      border-color: #e8a4b8;
    }}
    
    .diary-hint {{
      background: #f8f9fa;
      padding: 12px;
      border-radius: 8px;
      margin-bottom: 12px;
      font-size: 14px;
      color: #666;
    }}
    
    .summary-section {{
      background: #1a1a2e;
      color: #eee;
      padding: 16px;
      border-radius: 8px;
      font-family: monospace;
      font-size: 13px;
      white-space: pre-wrap;
      line-height: 1.6;
      max-height: 400px;
      overflow-y: auto;
    }}
    
    .progress-bar {{
      background: rgba(255,255,255,0.3);
      border-radius: 10px;
      height: 8px;
      margin-bottom: 24px;
      overflow: hidden;
    }}
    
    .progress-fill {{
      background: white;
      height: 100%;
      border-radius: 10px;
      transition: width 0.3s;
    }}
    
    .copy-toast {{
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: #333;
      color: white;
      padding: 12px 24px;
      border-radius: 8px;
      opacity: 0;
      transition: opacity 0.3s;
      z-index: 1000;
    }}
    
    .copy-toast.show {{
      opacity: 1;
    }}
    
    .conversation-box {{
      background: #f8f9fa;
      border-radius: 12px;
      padding: 16px;
      margin: 12px 0;
    }}
    
    .conversation-line {{
      display: flex;
      gap: 12px;
      margin-bottom: 12px;
    }}
    
    .conversation-line:last-child {{
      margin-bottom: 0;
    }}
    
    .speaker {{
      font-weight: bold;
      color: #e8a4b8;
      min-width: 24px;
    }}
    
    .speaker.b {{
      color: #e91e63;
    }}
    
    .dialogue {{
      line-height: 1.6;
    }}
    
    .section-complete {{
      text-align: center;
      padding: 20px;
      color: #28a745;
    }}
    
    .footer-nav {{
      display: flex;
      justify-content: space-between;
      padding: 20px 0;
    }}
    
    .footer-nav .btn {{
      padding: 14px 24px;
    }}
    
    .nav-link {{
      text-decoration: none;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>{emoji} Day {day}: {recipe_en}</h1>
    <p class="day-badge">30日間クッキング英語 — {day}日目</p>
    
    <div class="progress-bar">
      <div class="progress-fill" id="progressFill" style="width: 0%"></div>
    </div>

    <!-- Section 1: Recipe -->
    <div class="card" id="section1">
      <div class="card-header">
        <div class="card-number">1</div>
        <div>
          <div class="card-title">Recipe</div>
          <div class="card-subtitle">{recipe_ja}のレシピを読んでみよう</div>
        </div>
      </div>
      
      <div class="english-text" id="recipeText">
        <p><strong>{recipe_title}</strong></p>
        <p>{recipe_intro}</p>
        <p><strong>Ingredients:</strong><br>{recipe_ingredients}</p>
        <p><strong>Steps:</strong></p>
        {recipe_steps}
      </div>
      
      <div class="btn-row">
        <button class="btn btn-secondary" onclick="copyText('recipeText')">📋 コピー</button>
        <button class="btn btn-secondary" onclick="openNaturalReader()">🔊 Natural Reader</button>
        <button class="btn btn-primary" onclick="toggleVocab('vocab1')">📚 単語リストを見る</button>
      </div>
      
      <div class="vocab-section" id="vocab1">
        <h4>💡 わからなかった単語にチェック ✓</h4>
        {recipe_vocab}
      </div>
    </div>

    <!-- Section 2: Quiz 1 -->
    <div class="card" id="section2">
      <div class="card-header">
        <div class="card-number">2</div>
        <div>
          <div class="card-title">Quiz 1</div>
          <div class="card-subtitle">レシピの内容チェック</div>
        </div>
      </div>
      
      <div class="quiz-section">
        <div class="quiz-question">Q: {quiz1_question}</div>
        <div class="quiz-options" id="quiz1">
          {quiz1_options}
        </div>
        <div class="quiz-result" id="quiz1-result"></div>
      </div>
    </div>

    <!-- Section 3: Review -->
    <div class="card" id="section3">
      <div class="card-header">
        <div class="card-number">3</div>
        <div>
          <div class="card-title">Review</div>
          <div class="card-subtitle">オーストラリアのレストランレビュー</div>
        </div>
      </div>
      
      <div class="english-text" id="reviewText">
        <p><strong>🏠 {review_restaurant} — {review_location}, Australia</strong></p>
        <p>{review_stars}</p>
        <p>{review_content}</p>
      </div>
      
      <div class="btn-row">
        <button class="btn btn-secondary" onclick="copyText('reviewText')">📋 コピー</button>
        <button class="btn btn-secondary" onclick="openNaturalReader()">🔊 Natural Reader</button>
        <button class="btn btn-primary" onclick="toggleVocab('vocab2')">📚 単語リストを見る</button>
      </div>
      
      <div class="vocab-section" id="vocab2">
        <h4>💡 わからなかった単語にチェック ✓</h4>
        {review_vocab}
      </div>
    </div>

    <!-- Section 4: Quiz 2 -->
    <div class="card" id="section4">
      <div class="card-header">
        <div class="card-number">4</div>
        <div>
          <div class="card-title">Quiz 2</div>
          <div class="card-subtitle">レビューの内容チェック</div>
        </div>
      </div>
      
      <div class="quiz-section">
        <div class="quiz-question">Q: {quiz2_question}</div>
        <div class="quiz-options" id="quiz2">
          {quiz2_options}
        </div>
        <div class="quiz-result" id="quiz2-result"></div>
      </div>
    </div>

    <!-- Section 5: Australia Tips -->
    <div class="card" id="section5">
      <div class="card-header">
        <div class="card-number">5</div>
        <div>
          <div class="card-title">🦘 Australia Tips</div>
          <div class="card-subtitle">{australia_tips_title}</div>
        </div>
      </div>
      
      <div class="tips-section">
        {australia_tips_content}
      </div>
    </div>

    <!-- Section 6: Conversation -->
    <div class="card" id="section6">
      <div class="card-header">
        <div class="card-number">6</div>
        <div>
          <div class="card-title">Conversation</div>
          <div class="card-subtitle">{conversation_scene}</div>
        </div>
      </div>
      
      <div class="conversation-box" id="conversationText">
        <p style="color: #666; font-size: 14px; margin-bottom: 12px;">🏠 {conversation_scene}</p>
        {conversation_lines}
      </div>
      
      <div class="btn-row">
        <button class="btn btn-secondary" onclick="copyConversation()">📋 コピー</button>
        <button class="btn btn-secondary" onclick="openNaturalReader()">🔊 Natural Reader</button>
        <button class="btn btn-primary" onclick="toggleVocab('vocab3')">📚 単語リストを見る</button>
      </div>
      
      <div class="vocab-section" id="vocab3">
        <h4>💡 わからなかった単語にチェック ✓</h4>
        {conversation_vocab}
      </div>
    </div>

    <!-- Section 7: Quiz 3 -->
    <div class="card" id="section7">
      <div class="card-header">
        <div class="card-number">7</div>
        <div>
          <div class="card-title">Quiz 3</div>
          <div class="card-subtitle">会話の内容チェック</div>
        </div>
      </div>
      
      <div class="quiz-section">
        <div class="quiz-question">Q: {quiz3_question}</div>
        <div class="quiz-options" id="quiz3">
          {quiz3_options}
        </div>
        <div class="quiz-result" id="quiz3-result"></div>
      </div>
    </div>

    <!-- Section 8: Try It! -->
    <div class="card" id="section8">
      <div class="card-header">
        <div class="card-number">8</div>
        <div>
          <div class="card-title">✏️ Try It!</div>
          <div class="card-subtitle">今日のことを3行で書いてみよう</div>
        </div>
      </div>
      
      <div class="diary-section">
        <div class="diary-hint">
          <p>💡 今日の会話や文をマネしてOK！わからない英語は日本語のままで大丈夫。</p>
          <p style="margin-top: 8px;">例：</p>
          <p style="font-style: italic; color: #e8a4b8;">{try_it_hint}</p>
        </div>
        
        <textarea id="diaryText" placeholder="I'm making...&#10;&#10;"></textarea>
      </div>
    </div>

    <!-- Section 9: Summary -->
    <div class="card" id="section9">
      <div class="card-header">
        <div class="card-number">✓</div>
        <div>
          <div class="card-title">📊 学習サマリー</div>
          <div class="card-subtitle">ChatGPTにコピペして解説をもらおう</div>
        </div>
      </div>
      
      <button class="btn btn-primary" onclick="generateSummary()" style="margin-bottom: 16px; width: 100%; justify-content: center;">
        📋 サマリーを生成する
      </button>
      
      <div class="summary-section" id="summaryOutput">
ここにサマリーが表示されます。
上のボタンを押してね！
      </div>
      
      <div class="btn-row" style="margin-top: 12px;">
        <button class="btn btn-success" onclick="copySummary()">📋 サマリーをコピー</button>
        <button class="btn btn-secondary" onclick="openChatGPT()">🤖 ChatGPTを開く</button>
      </div>
    </div>

    <!-- Footer Navigation -->
    <div style="text-align: center; margin-top: 8px;">
      <a href="index.html" class="btn btn-secondary" style="display: inline-flex; padding: 10px 20px; text-decoration: none;">🏠 ホームに戻る</a>
    </div>
    <div class="footer-nav">
      {nav_prev}
      {nav_next}
    </div>
  </div>

  <div class="copy-toast" id="copyToast">コピーしました！</div>

  <script>
    // Quiz state
    const quizResults = {{
      quiz1: null,
      quiz2: null,
      quiz3: null
    }};
    
    const quizCorrect = {{
      quiz1: {quiz1_correct},
      quiz2: {quiz2_correct},
      quiz3: {quiz3_correct}
    }};

    // Toggle vocabulary section
    function toggleVocab(id) {{
      const section = document.getElementById(id);
      section.classList.toggle('show');
      updateProgress();
    }}

    // Copy text to clipboard
    function copyText(elementId) {{
      const element = document.getElementById(elementId);
      const text = element.innerText;
      navigator.clipboard.writeText(text).then(() => {{
        showToast();
      }});
    }}

    // Copy conversation
    function copyConversation() {{
      const lines = document.querySelectorAll('#conversationText .conversation-line');
      let text = '';
      lines.forEach(line => {{
        const speaker = line.querySelector('.speaker').innerText;
        const dialogue = line.querySelector('.dialogue').innerText;
        text += speaker + ' ' + dialogue + '\\n';
      }});
      navigator.clipboard.writeText(text).then(() => {{
        showToast();
      }});
    }}

    // Open Natural Reader
    function openNaturalReader() {{
      window.open('https://www.naturalreaders.com/online/', '_blank');
    }}

    // Open ChatGPT
    function openChatGPT() {{
      window.open('https://chat.openai.com/', '_blank');
    }}

    // Show copy toast
    function showToast() {{
      const toast = document.getElementById('copyToast');
      toast.classList.add('show');
      setTimeout(() => {{
        toast.classList.remove('show');
      }}, 2000);
    }}

    // Quiz selection
    function selectQuiz(element, quizId, optionIndex) {{
      const options = document.querySelectorAll(`#${{quizId}} .quiz-option`);
      const resultDiv = document.getElementById(`${{quizId}}-result`);
      const isCorrect = optionIndex === quizCorrect[quizId];
      
      // Remove previous selections
      options.forEach(opt => {{
        opt.classList.remove('selected', 'correct', 'incorrect');
      }});
      
      // Add selection
      element.classList.add('selected');
      
      if (isCorrect) {{
        element.classList.add('correct');
        resultDiv.textContent = '⭕ 正解！';
        resultDiv.className = 'quiz-result show correct';
        quizResults[quizId] = true;
      }} else {{
        element.classList.add('incorrect');
        resultDiv.textContent = '❌ 残念！もう一度読んでみよう。';
        resultDiv.className = 'quiz-result show incorrect';
        quizResults[quizId] = false;
      }}
      
      updateProgress();
    }}

    // Update progress bar
    function updateProgress() {{
      let completed = 0;
      
      // Check vocab sections opened
      if (document.getElementById('vocab1').classList.contains('show')) completed++;
      if (document.getElementById('vocab2').classList.contains('show')) completed++;
      if (document.getElementById('vocab3').classList.contains('show')) completed++;
      
      // Check quizzes answered
      if (quizResults.quiz1 !== null) completed++;
      if (quizResults.quiz2 !== null) completed++;
      if (quizResults.quiz3 !== null) completed++;
      
      // Check diary written
      if (document.getElementById('diaryText').value.trim().length > 10) completed++;
      
      const percent = Math.min(100, (completed / 7) * 100);
      document.getElementById('progressFill').style.width = percent + '%';
    }}

    // Generate summary
    function generateSummary() {{
      // Get checked words
      const checkedWords = [];
      document.querySelectorAll('.vocab-check:checked').forEach(checkbox => {{
        const item = checkbox.closest('.vocab-item');
        const word = item.querySelector('.vocab-word').innerText;
        const meaning = item.querySelector('.vocab-meaning').innerText;
        checkedWords.push(`- ${{word}}（${{meaning}}）`);
      }});
      
      // Get quiz results
      const quizSummary = [];
      if (quizResults.quiz1 !== null) {{
        quizSummary.push(`Quiz 1: ${{quizResults.quiz1 ? '⭕ 正解' : '❌ 不正解'}}`);
      }}
      if (quizResults.quiz2 !== null) {{
        quizSummary.push(`Quiz 2: ${{quizResults.quiz2 ? '⭕ 正解' : '❌ 不正解'}}`);
      }}
      if (quizResults.quiz3 !== null) {{
        quizSummary.push(`Quiz 3: ${{quizResults.quiz3 ? '⭕ 正解' : '❌ 不正解'}}`);
      }}
      
      // Get diary text
      const diaryText = document.getElementById('diaryText').value.trim() || '（まだ書いてないよ）';
      
      // Generate summary
      const summary = `【Day {day}: {recipe_en} {emoji} 学習結果】

■ わからなかった単語（${{checkedWords.length}}個）
${{checkedWords.length > 0 ? checkedWords.join('\\n') : '（なし）'}}

■ クイズ結果
${{quizSummary.length > 0 ? quizSummary.join('\\n') : '（まだ解いてないよ）'}}

■ Try It! で書いた文
${{diaryText}}

---
このまま ChatGPT に貼って「解説して」「添削して」と言ってね！
特に Try It! で書いた英文の添削をお願いすると良いよ。`;

      document.getElementById('summaryOutput').textContent = summary;
      updateProgress();
    }}

    // Copy summary
    function copySummary() {{
      const summary = document.getElementById('summaryOutput').textContent;
      navigator.clipboard.writeText(summary).then(() => {{
        showToast();
      }});
    }}

    // Listen for diary input
    document.getElementById('diaryText').addEventListener('input', updateProgress);
  </script>
</body>
</html>'''


def generate_vocab_html(vocab_list):
    """Generate HTML for vocabulary items"""
    html = ""
    for item in vocab_list:
        word = item.get("word", "")
        meaning = item.get("meaning", "")
        html += f'''        <div class="vocab-item">
          <input type="checkbox" class="vocab-check" data-word="{word}">
          <span class="vocab-word">{word}</span>
          <span class="vocab-meaning">{meaning}</span>
        </div>
'''
    return html


def generate_quiz_options_html(quiz, quiz_id):
    """Generate HTML for quiz options"""
    html = ""
    for i, option in enumerate(quiz.get("options", [])):
        html += f'''          <div class="quiz-option" onclick="selectQuiz(this, '{quiz_id}', {i})">{option}</div>
'''
    return html


def generate_conversation_html(conversation):
    """Generate HTML for conversation lines"""
    html = ""
    for line in conversation.get("lines", []):
        speaker = line.get("speaker", "A")
        text = line.get("text", "")
        speaker_class = "speaker b" if speaker == "B" else "speaker"
        html += f'''        <div class="conversation-line">
          <span class="{speaker_class}">{speaker}:</span>
          <span class="dialogue">{text}</span>
        </div>
'''
    return html


def generate_steps_html(steps):
    """Generate HTML for recipe steps"""
    html = ""
    for i, step in enumerate(steps, 1):
        # Convert markdown bold to HTML
        step_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', step)
        html += f"<p>{i}. {step_html}</p>\n        "
    return html


def generate_stars(count):
    """Generate star rating"""
    return "⭐" * count


def build_html(day, content):
    """Build HTML file from JSON content"""
    meta = content.get("meta", {})
    recipe = content.get("recipe", {})
    review = content.get("review", {})
    conversation = content.get("conversation", {})
    australia_tips = content.get("australia_tips", {})
    
    # Navigation
    if day == 1:
        nav_prev = '<button class="btn btn-secondary" disabled>← 前の日</button>'
    else:
        nav_prev = f'<a href="day{day-1}.html" class="nav-link"><button class="btn btn-secondary">← Day {day-1}</button></a>'
    
    if day == 30:
        nav_next = '<button class="btn btn-primary" disabled>完了！ 🎉</button>'
    else:
        nav_next = f'<a href="day{day+1}.html" class="nav-link"><button class="btn btn-primary">Day {day+1} →</button></a>'
    
    # Format Australia tips content
    tips_content = australia_tips.get("content", "")
    tips_content_html = ""
    for para in tips_content.split("\n\n"):
        if para.strip():
            tips_content_html += f"<p>{para.strip()}</p>\n        "
    
    html = HTML_TEMPLATE.format(
        day=day,
        recipe_en=meta.get("en", ""),
        recipe_ja=meta.get("ja", ""),
        emoji=meta.get("emoji", "🍳"),
        recipe_title=recipe.get("title", ""),
        recipe_intro=recipe.get("intro", ""),
        recipe_ingredients=recipe.get("ingredients", ""),
        recipe_steps=generate_steps_html(recipe.get("steps", [])),
        recipe_vocab=generate_vocab_html(content.get("recipe_vocab", [])),
        quiz1_question=content.get("quiz1", {}).get("question", ""),
        quiz1_options=generate_quiz_options_html(content.get("quiz1", {}), "quiz1"),
        quiz1_correct=content.get("quiz1", {}).get("correct", 0),
        review_restaurant=review.get("restaurant", ""),
        review_location=review.get("location", ""),
        review_stars=generate_stars(review.get("stars", 5)),
        review_content=review.get("content", ""),
        review_vocab=generate_vocab_html(content.get("review_vocab", [])),
        quiz2_question=content.get("quiz2", {}).get("question", ""),
        quiz2_options=generate_quiz_options_html(content.get("quiz2", {}), "quiz2"),
        quiz2_correct=content.get("quiz2", {}).get("correct", 0),
        australia_tips_title=australia_tips.get("title", ""),
        australia_tips_content=tips_content_html,
        conversation_scene=conversation.get("scene", ""),
        conversation_lines=generate_conversation_html(conversation),
        conversation_vocab=generate_vocab_html(content.get("conversation_vocab", [])),
        quiz3_question=content.get("quiz3", {}).get("question", ""),
        quiz3_options=generate_quiz_options_html(content.get("quiz3", {}), "quiz3"),
        quiz3_correct=content.get("quiz3", {}).get("correct", 0),
        try_it_hint=content.get("try_it_hint", "I'm making ... tonight."),
        nav_prev=nav_prev,
        nav_next=nav_next,
    )
    
    return html


def build_index_html(recipes):
    """Build index.html with links to all days"""
    html = '''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>30日間クッキング英語</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Hiragino Sans', sans-serif;
      background: linear-gradient(135deg, #e8a4b8 0%, #b8a4e8 100%);
      min-height: 100vh;
      padding: 20px;
    }
    .container { max-width: 700px; margin: 0 auto; }
    h1 { color: white; text-align: center; margin-bottom: 8px; font-size: 28px; }
    .subtitle { text-align: center; color: rgba(255,255,255,0.9); margin-bottom: 24px; }
    .card {
      background: white;
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .day-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
      gap: 12px;
    }
    .day-link {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 16px;
      background: #f8f9fa;
      border-radius: 12px;
      text-decoration: none;
      color: #333;
      transition: all 0.2s;
    }
    .day-link:hover {
      background: #e8a4b8;
      color: white;
      transform: translateY(-2px);
    }
    .day-emoji { font-size: 32px; margin-bottom: 8px; }
    .day-number { font-weight: bold; font-size: 14px; }
    .day-name { font-size: 12px; color: #666; }
    .day-link:hover .day-name { color: rgba(255,255,255,0.8); }
  </style>
</head>
<body>
  <div class="container">
    <h1>🍳 30日間クッキング英語</h1>
    <p class="subtitle">料理しながら英検5級レベルの英語を学ぼう！</p>

    <div style="text-align: center; margin-bottom: 20px;">
      <a href="challenge.html" style="display: inline-block; background: white; color: #e8a4b8; font-weight: bold; font-size: 16px; padding: 16px 32px; border-radius: 50px; text-decoration: none; box-shadow: 0 4px 20px rgba(0,0,0,0.15); transition: all 0.2s;" onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 6px 24px rgba(0,0,0,0.2)'" onmouseout="this.style.transform='';this.style.boxShadow='0 4px 20px rgba(0,0,0,0.15)'">🎯 余力があるならチャレンジ！</a>
    </div>

    <div class="card">
      <div class="day-grid">
'''
    
    for r in recipes:
        html += f'''        <a href="day{r["day"]}.html" class="day-link">
          <span class="day-emoji">{r["emoji"]}</span>
          <span class="day-number">Day {r["day"]}</span>
          <span class="day-name">{r["en"]}</span>
        </a>
'''
    
    html += '''      </div>
    </div>
  </div>
</body>
</html>'''
    
    return html


def main():
    # Check if content directory exists
    if not os.path.exists("content"):
        print("❌ content/ フォルダが見つかりません")
        print("先に generate_content.py を実行してください")
        return
    
    # Create output directory
    os.makedirs("docs", exist_ok=True)
    
    recipes = [
        {"day": 1, "en": "Gyoza", "ja": "餃子", "emoji": "🥟"},
        {"day": 2, "en": "Shumai", "ja": "シュウマイ", "emoji": "🟡"},
        {"day": 3, "en": "Karaage", "ja": "唐揚げ", "emoji": "🍗"},
        {"day": 4, "en": "Chicken Nanban", "ja": "チキン南蛮", "emoji": "🍗"},
        {"day": 5, "en": "Yurinjii", "ja": "油淋鶏", "emoji": "🐔"},
        {"day": 6, "en": "Kakuni", "ja": "角煮", "emoji": "🍖"},
        {"day": 7, "en": "Fried Rice", "ja": "チャーハン", "emoji": "🍳"},
        {"day": 8, "en": "Ramen", "ja": "ラーメン", "emoji": "🍜"},
        {"day": 9, "en": "Onigiri", "ja": "おにぎり", "emoji": "🍙"},
        {"day": 10, "en": "Miso Soup", "ja": "味噌汁", "emoji": "🥣"},
        {"day": 11, "en": "Tamagoyaki", "ja": "卵焼き", "emoji": "🥚"},
        {"day": 12, "en": "Teriyaki Chicken", "ja": "照り焼きチキン", "emoji": "🍗"},
        {"day": 13, "en": "Japanese Curry", "ja": "カレー", "emoji": "🍛"},
        {"day": 14, "en": "Okonomiyaki", "ja": "お好み焼き", "emoji": "🥞"},
        {"day": 15, "en": "Takoyaki", "ja": "たこ焼き", "emoji": "🐙"},
        {"day": 16, "en": "Nikujaga", "ja": "肉じゃが", "emoji": "🥔"},
        {"day": 17, "en": "Gyudon", "ja": "牛丼", "emoji": "🥩"},
        {"day": 18, "en": "Tonkatsu", "ja": "とんかつ", "emoji": "🐷"},
        {"day": 19, "en": "Yakitori", "ja": "焼き鳥", "emoji": "🍢"},
        {"day": 20, "en": "Edamame", "ja": "枝豆", "emoji": "🫛"},
        {"day": 21, "en": "Chawanmushi", "ja": "茶碗蒸し", "emoji": "🍮"},
        {"day": 22, "en": "Tempura", "ja": "天ぷら", "emoji": "🍤"},
        {"day": 23, "en": "Soba", "ja": "そば", "emoji": "🍝"},
        {"day": 24, "en": "Udon", "ja": "うどん", "emoji": "🍜"},
        {"day": 25, "en": "Oyakodon", "ja": "親子丼", "emoji": "🐔"},
        {"day": 26, "en": "Katsudon", "ja": "カツ丼", "emoji": "🍱"},
        {"day": 27, "en": "Ochazuke", "ja": "お茶漬け", "emoji": "🍵"},
        {"day": 28, "en": "Takowasa", "ja": "たこわさ", "emoji": "🐙"},
        {"day": 29, "en": "Tsukemono", "ja": "浅漬け", "emoji": "🥒"},
        {"day": 30, "en": "Matcha Pudding", "ja": "抹茶プリン", "emoji": "🍵"},
    ]
    
    print("🔨 30日間クッキング英語 - HTML生成開始")
    print("=" * 50)
    
    success_count = 0
    
    for recipe in recipes:
        day = recipe["day"]
        json_path = f"content/day{day}.json"
        
        if not os.path.exists(json_path):
            print(f"⏭️  Day {day}: JSONファイルがありません - スキップ")
            continue
        
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                content = json.load(f)
            
            # Add meta if missing
            if "meta" not in content:
                content["meta"] = recipe
            
            html = build_html(day, content)
            
            with open(f"docs/day{day}.html", "w", encoding="utf-8") as f:
                f.write(html)
            
            print(f"✅ Day {day}: {recipe['en']} → docs/day{day}.html")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Day {day}: エラー - {e}")
    
    # Generate index.html
    index_html = build_index_html(recipes)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"✅ index.html 生成完了")
    
    print("=" * 50)
    print(f"✅ 生成完了: {success_count}/30 日分")
    print("📁 docs/ フォルダにHTMLファイルが保存されました")
    print("")
    print("ローカルで確認:")
    print("  open docs/index.html")
    print("")
    print("デプロイ:")
    print("  Cloudflare Pages / GitHub Pages で docs/ を公開")


if __name__ == "__main__":
    main()
