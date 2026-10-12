import re

with open("app/src/main/assets/index.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update Main Card CSS
old_main_css = """.movies-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;padding:16px 14px;justify-items:center}
.movie-card{text-align:center;position:relative;background:#111;border-radius:16px;padding:10px;overflow:hidden;width:100%;max-width:170px;min-width:0}
.poster{width:140px;height:140px;object-fit:contain;background:#1e1e1e;border-radius:14px;display:block;border:1px solid #222;margin:0 auto}
.favorite-btn{position:absolute;top:8px;left:8px;width:30px;height:30px;border-radius:50%;border:none;background:rgba(0,0,0,.6);color:#fff;z-index:2;cursor:pointer}
.favorite-btn.active{color:#e50914}
.movie-card h3{font-size:14px;font-weight:800;margin-top:8px;min-height:36px;line-height:18px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;word-break:break-word}
.movie-card p{font-size:12px;color:#777;margin-top:4px}"""

new_main_css = """.movies-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px 12px;padding:16px 12px;justify-items:stretch}
.movie-card{text-align:right;direction:rtl;position:relative;background:transparent;border-radius:14px;padding:0;overflow:visible;width:100%;max-width:180px;min-width:0;margin:0 auto;box-sizing:border-box}
.movie-card-clickable{position:relative;display:flex;flex-direction:column;width:100%;cursor:pointer;outline:none}
.movie-card-poster-wrap{position:relative;width:100%;aspect-ratio:2/3;border-radius:14px;overflow:hidden;background:#121212;border:1px solid #262626;box-shadow:0 6px 16px rgba(0,0,0,0.55);transition:transform 0.22s ease,border-color 0.22s ease}
.movie-card-clickable:hover .movie-card-poster-wrap,.movie-card-clickable:focus .movie-card-poster-wrap{transform:translateY(-2px);border-color:#3a3a3a}
.poster{width:100%;height:100%;object-fit:cover;background:#141414;border-radius:0;display:block;border:none;margin:0;transition:transform 0.25s ease}
.movie-card-clickable:hover .poster{transform:scale(1.03)}
.favorite-btn{position:absolute;top:8px;left:8px;width:30px;height:30px;border-radius:50%;border:none;background:rgba(0,0,0,.65);color:#fff;z-index:4;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:15px;backdrop-filter:blur(4px);transition:transform 0.15s ease}
.favorite-btn:active{transform:scale(0.9)}
.favorite-btn.active{color:#e50914}
.movie-card-type-badge{position:absolute;bottom:7px;right:7px;background:rgba(229,9,20,0.92);color:#fff;font-size:10px;font-weight:900;padding:3px 8px;border-radius:8px;backdrop-filter:blur(4px);box-shadow:0 2px 6px rgba(0,0,0,0.7);max-width:85%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;z-index:2;line-height:1.2}
.movie-card-version-badge{position:absolute;bottom:7px;left:7px;background:rgba(15,28,36,0.92);color:#38bdf8;border:1px solid #164e63;font-size:9.5px;font-weight:bold;padding:2px 6px;border-radius:6px;backdrop-filter:blur(4px);max-width:50%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;z-index:2;line-height:1.2}
.movie-card-info{padding:6px 2px 2px 2px;width:100%;box-sizing:border-box}
.movie-card h3{font-size:13px;font-weight:700;color:#fff;margin:0 0 2px 0;line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-align:right;min-height:unset}
.movie-card p{font-size:11px;font-weight:500;color:#888;margin:0;line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-align:right}"""

# 2. Update Light Mode CSS
old_light_css = """body.light-mode .movie-card{background:#ffffff;border:1px solid #e2e5ec;box-shadow:0 4px 12px rgba(0,0,0,0.05)}
body.light-mode .movie-card h3{color:#111}
body.light-mode .movie-card p{color:#555}
body.light-mode .poster{background:#eef0f4;border:1px solid #dcdfe6}"""

new_light_css = """body.light-mode .movie-card{background:transparent;border:none;box-shadow:none}
body.light-mode .movie-card-poster-wrap{background:#eef0f4;border:1px solid #dcdfe6;box-shadow:0 4px 12px rgba(0,0,0,0.06)}
body.light-mode .movie-card h3{color:#111}
body.light-mode .movie-card p{color:#666}
body.light-mode .poster{background:#eef0f4;border:none}"""

# 3. Update createCard function
old_create_card = """window.createCard=(item)=>{
  let fav=window.isFavorite(item.id);
  let click=(window.currentUserRole==="ADMIN"&&window.selectEpisodeMode)?`renderAddEpisodeForm('${item.firebaseId}')`:(window.currentUserRole==="ADMIN"&&window.deleteMode)?`askDeleteMovie('${item.firebaseId}')`:`openDetails('${item.firebaseId}')`;
  let del=(window.currentUserRole==="ADMIN"&&window.deleteMode)?`<button tabindex="0" style="position:absolute;top:6px;right:6px;width:22px;height:22px;border-radius:50%;border:none;background:#e50914;color:#fff;z-index:3" onclick="event.stopPropagation();askDeleteMovie('${item.firebaseId}')">✕</button>`:"";
  let editPosterBtn=(window.currentUserRole==="ADMIN")?`<button type="button" tabindex="0" style="width:100%;margin-top:8px;background:#1a2a3a;color:#00d2ff;border:1px solid #2a4a6a;padding:6px 8px;border-radius:8px;font-size:11px;font-weight:bold;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:4px" onclick="event.stopPropagation();openEditPosterModal('${item.firebaseId}')">🖼️ تعديل البوستر</button>`:"";
  let isAnimation = item.type === "animation" || item.type === "arabic" || item.type === "sports";
  let categoryLabel = window.translateCategoryLabel(item.category, isAnimation);
  return`<div class="movie-card" tabindex="0"><button tabindex="0" class="favorite-btn ${fav?"active":""}" onclick="event.stopPropagation();toggleFavorite('${item.id}')">♥</button>${del}<div onclick="${click}"><img class="poster" data-poster-fid="${item.firebaseId}" src="${item.poster}" loading="lazy" decoding="async"><h3>${item.title}</h3><p>${item.year} • ${categoryLabel}</p></div>${editPosterBtn}</div>`;
};"""

new_create_card = """window.createCard=(item)=>{
  let fav=window.isFavorite(item.id);
  let click=(window.currentUserRole==="ADMIN"&&window.selectEpisodeMode)?`renderAddEpisodeForm('${item.firebaseId}')`:(window.currentUserRole==="ADMIN"&&window.deleteMode)?`askDeleteMovie('${item.firebaseId}')`:`openDetails('${item.firebaseId}')`;
  let del=(window.currentUserRole==="ADMIN"&&window.deleteMode)?`<button tabindex="0" style="position:absolute;top:6px;right:6px;width:22px;height:22px;border-radius:50%;border:none;background:#e50914;color:#fff;z-index:5" onclick="event.stopPropagation();askDeleteMovie('${item.firebaseId}')">✕</button>`:"";
  let editPosterBtn=(window.currentUserRole==="ADMIN")?`<button type="button" tabindex="0" style="width:100%;margin-top:6px;background:#1a2a3a;color:#00d2ff;border:1px solid #2a4a6a;padding:5px 8px;border-radius:8px;font-size:11px;font-weight:bold;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:4px" onclick="event.stopPropagation();openEditPosterModal('${item.firebaseId}')">🖼️ تعديل البوستر</button>`:"";
  let isAnimation = item.type === "animation" || item.type === "arabic" || item.type === "sports";
  let categoryLabel = window.translateCategoryLabel(item.category, isAnimation);
  let rawBadge = (item.category && item.category !== "all") ? item.category : (isAnimation ? "الأنميشن" : "مسلسل");
  let typeBadgeLabel = rawBadge;
  if (rawBadge === "فيلم" || rawBadge === "فلم") typeBadgeLabel = "الفيلم";
  else if (rawBadge === "مسلسل") typeBadgeLabel = "مسلسل";
  else if (rawBadge === "أنميشن") typeBadgeLabel = "الأنميشن";
  else if (rawBadge === "أنمي") typeBadgeLabel = "الأنمي";
  let versionBadgeHtml = item.version ? `<span class="movie-card-version-badge">${window.escapeDescHtml(item.version)}</span>` : "";
  let yearText = item.year || 2024;
  let safeTitle = window.escapeDescHtml(item.title || "");
  return `<div class="movie-card" tabindex="0">
    <button tabindex="0" class="favorite-btn ${fav?"active":""}" onclick="event.stopPropagation();toggleFavorite('${item.id}')" title="المفضلة">♥</button>
    ${del}
    <div class="movie-card-clickable" onclick="${click}">
      <div class="movie-card-poster-wrap">
        <img class="poster" data-poster-fid="${item.firebaseId}" src="${item.poster}" alt="${safeTitle}" loading="lazy" decoding="async">
        <span class="movie-card-type-badge">${window.escapeDescHtml(typeBadgeLabel)}</span>
        ${versionBadgeHtml}
      </div>
      <div class="movie-card-info">
        <h3 title="${safeTitle}">${safeTitle}</h3>
        <p>${yearText} • ${window.escapeDescHtml(categoryLabel)}</p>
      </div>
    </div>
    ${editPosterBtn}
  </div>`;
};"""

assert old_main_css in text, "old_main_css not found"
assert old_light_css in text, "old_light_css not found"
assert old_create_card in text, "old_create_card not found"

text = text.replace(old_main_css, new_main_css, 1)
text = text.replace(old_light_css, new_light_css, 1)
text = text.replace(old_create_card, new_create_card, 1)

with open("app/src/main/assets/index.html", "w", encoding="utf-8") as f:
    f.write(text)

print("Replacement successful!")
