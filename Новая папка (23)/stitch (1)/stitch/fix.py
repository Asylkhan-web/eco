import os, re

files = [
    r'c:\Users\user\Desktop\эко\Новая папка (23)\stitch (1)\stitch\lesson_kinematics_in_nature\code.html',
    r'c:\Users\user\Desktop\эко\Новая папка (23)\stitch (1)\stitch\chlorophyll_physics\code.html',
    r'c:\Users\user\Desktop\эко\Новая папка (23)\stitch (1)\stitch\section3_electrostatics\code.html',
    r'c:\Users\user\Desktop\эко\Новая папка (23)\stitch (1)\stitch\section4_quantum\code.html'
]

replacement = """function getUser() { return JSON.parse(localStorage.getItem('pn_current_user')) || { ecoCoins: 420, unlockedChapters: [] }; }
  function updateUser(u) {
    const users = JSON.parse(localStorage.getItem('pn_users') || '[]');
    const idx = users.findIndex(v => v && u && v.email === u.email);
    if (idx !== -1) { users[idx] = u; localStorage.setItem('pn_users', JSON.stringify(users)); }
    localStorage.setItem('pn_current_user', JSON.stringify(u));
  }
  function addCoinsToGlobal(amount) {
    let u = getUser(); u.ecoCoins = (u.ecoCoins || 420) + amount; updateUser(u);
    const cd = document.getElementById('coin-display'); if(cd) cd.textContent = '$' + u.ecoCoins + ' Эко-тиын';
    const td = document.getElementById('total-coins'); if(td) td.textContent = u.ecoCoins;
  }
  
  function showCoinModal(chapterName, required) {
    let u = getUser();
    u.unlockedChapters = u.unlockedChapters || [];
    const isUnlocked = u.unlockedChapters.includes(chapterName);
    
    const iconEl = document.getElementById('chapter-modal-icon');
    if (iconEl) {
      iconEl.textContent = isUnlocked ? 'lock_open' : 'stars';
      iconEl.style.color = isUnlocked ? '#0d631b' : '#734e00';
    }
    const titleEl = document.getElementById('chapter-modal-title');
    if (titleEl) titleEl.textContent = chapterName;
    
    const modalBtn = document.querySelector('#chapter-modal button');
    const bodyEl = document.getElementById('chapter-modal-body');
    const coinsEl = document.getElementById('modal-coins-display');
    
    if (isUnlocked) {
      if(bodyEl) bodyEl.textContent = 'Тарау ашылды! Жаңа контентке қош келдіңіз.';
      if(coinsEl) coinsEl.textContent = 'АШЫҚ';
      if(modalBtn) { modalBtn.textContent = 'Кіру'; modalBtn.onclick = function() { document.getElementById('chapter-modal').classList.add('hidden'); }; }
    } else {
      const currentCoins = u.ecoCoins || 420;
      const remaining = Math.max(0, required - currentCoins);
      if (remaining > 0) {
        if(bodyEl) bodyEl.textContent = `Бұл тарауды ашу үшін тағы ${remaining} Эко-тиын жетіспейді. Сабақтарды орындап тиын жинаңыз!`;
        if(coinsEl) coinsEl.textContent = currentCoins + ' / ' + required + ' Эко-тиын';
        if(modalBtn) { modalBtn.textContent = 'Жабық'; modalBtn.onclick = function() { document.getElementById('chapter-modal').classList.add('hidden'); }; }
      } else {
        if(bodyEl) bodyEl.textContent = `Сізде жеткілікті тиын бар. Тарауды ашу үшін ${required} Эко-тиын жұмсалады.`;
        if(coinsEl) coinsEl.textContent = 'Құны: ' + required + ' Эко-тиын';
        if(modalBtn) {
          modalBtn.textContent = 'Ашу (Тиын жұмсау)';
          modalBtn.onclick = function() {
            u.ecoCoins -= required; u.unlockedChapters.push(chapterName); updateUser(u);
            const cd = document.getElementById('coin-display'); if(cd) cd.textContent = '$' + u.ecoCoins + ' Эко-тиын';
            const td = document.getElementById('total-coins'); if(td) td.textContent = u.ecoCoins;
            showCoinModal(chapterName, required);
            if(typeof showToast === 'function') showToast(chapterName + ' ашылды!');
          };
        }
      }
    }
    const modalEl = document.getElementById('chapter-modal');
    if (modalEl) modalEl.classList.remove('hidden');
  }"""

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the showCoinModal function completely
    content = re.sub(r'function showCoinModal\(chapterName, required\) \{[\s\S]*?classList\.remove\(''hidden''\);\s*\}', replacement, content)
    
    # Also find any places where coins are added and modify them to add to global ecoCoins
    content = re.sub(r'coinsEarned \+= coins;\n      totalCoins \+= coins;', 
                     r'coinsEarned += coins;\n      totalCoins += coins; addCoinsToGlobal(coins);', content)
    content = re.sub(r'elCoinsEarned \+= coins;\n      totalCoins \+= coins;', 
                     r'elCoinsEarned += coins;\n      totalCoins += coins; addCoinsToGlobal(coins);', content)
    content = re.sub(r'qCoinsEarned \+= coins;\n      totalCoins \+= coins;', 
                     r'qCoinsEarned += coins;\n      totalCoins += coins; addCoinsToGlobal(coins);', content)
    content = re.sub(r'molCoinsEarned \+= coins;\n      totalCoins \+= coins;', 
                     r'molCoinsEarned += coins;\n      totalCoins += coins; addCoinsToGlobal(coins);', content)
    
    # Lab completions
    content = re.sub(r'setTimeout\(\(\)=>\{ addCoins\(150\); \}, 500\);', r'setTimeout(()=>{ addCoinsToGlobal(150); }, 500);', content)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
