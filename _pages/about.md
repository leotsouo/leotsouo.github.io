---
permalink: /about/
title: 關於我
excerpt: "Leo Tsou，資訊工程碩士生，研究方向為 emotion detection。"
---
<p class="page-intro">我是 Leo Tsou，一名資訊工程碩士生。研究方向為 <span lang="en">emotion detection</span>，也持續投入軟體開發與個人專案。</p>
<nav class="local-index" aria-label="關於頁目錄"><a href="#research">研究</a><a href="#practice">實作</a><a href="#contact">聯絡</a></nav>
<section class="profile-section" id="research"><p class="eyebrow">01 / RESEARCH</p><div><h2>emotion detection</h2><p>我關注如何運用資料與模型辨識情緒。這個網站會逐步整理相關方法、實驗與學習紀錄，留下問題、選擇與思考的過程。</p><a class="text-link" href="{{ '/papers/' | relative_url }}">論文閱讀紀錄 {% include direction-icon.html direction='right' %}</a></div></section>
<section class="profile-section" id="practice"><p class="eyebrow">02 / PRACTICE</p><div><h2>把需求寫成工具</h2><p>QuestNote 和 Taste Compare，分別從日常任務與飲食紀錄出發：前者結合待辦事項與寵物收集，後者透過比較整理餐廳與餐點的偏好。</p><a class="text-link" href="{{ '/projects/' | relative_url }}">查看專案 {% include direction-icon.html direction='right' %}</a></div></section>
<section class="profile-section" id="contact"><p class="eyebrow">03 / CONTACT</p><div><h2>聯絡與程式碼</h2><p>工作聯絡可以透過電子郵件；公開程式碼與專案放在 GitHub。</p>{% include contact-links.html %}</div></section>

{% if site.data.profile.education.size > 0 %}<section class="profile-section" id="education"><p class="eyebrow">EDUCATION</p><div><h2>學歷</h2><ul>{% for entry in site.data.profile.education %}<li>{{ entry.school | escape }}{% if entry.degree %} · {{ entry.degree | escape }}{% endif %}{% if entry.period %} · {{ entry.period | escape }}{% endif %}</li>{% endfor %}</ul></div></section>{% endif %}
