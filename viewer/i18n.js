// 画面の文言の辞書（日本語・英語）。Subject の中身は翻訳しない（書いた言語のまま出す）
// 言語の決め方: URL の ?lang= → 言語セレクタで選んだもの（このブラウザに覚える）→ ブラウザの言語
const I18N={
  ja:{
    pickSubject:'Subject を選ぶ',
    pickerHint:'Subject は <code>subjects/</code> の下のフォルダ1つ。新しく作るときは Claude に「新しい Subject を作って」と頼む。',
    noSubjects:'subjects/ に Subject がありません。',
    showOld:'old（deprecated を表示）',
    focusHint:'Claude に「これ」と言えば、ここに出ているものを読みます',
    splitHint:'ドラッグで幅を変える（ダブルクリックで元に戻す）',
    copy:'コピー',copied:'コピーしました',copyTitle:'{0} をコピー',
    focusNoL1:'Facet「{0}」は L1 が無いので、Claude には Facet 名で伝えてください',
    focusSharing:'Claude と共有中: ',
    facetQ:'Facet「{0}」',ofL1:' の L1',
    hasMaterial:'材料あり',notDiscussed:'未議論',stillEmpty:'（まだ空）',
    hideReason:'hide理由: ',notFilled:'（未記入）',
    inDiscussion:'入っている Discussion: ',sources:'根拠 (sources): ',derived:'派生 (逆向き): ',none:'なし',
    noL1Yet:'L1 はまだありません。決めるときの材料がある Discussion:',
    notDiscussedYet:'この Facet はまだ議論されていません。',
    secL1:'L1 決定',secL2:'L2 文脈（理由・選ばなかった案）',secMaterials:'Discussion の資料',
    secDiscs:'関連する Discussion',secLinked:'つながる Facet（参照している／されている）',
    asset:'実物 ',open:'開く',openApp:'アプリで開く',reveal:'フォルダで表示',
    openFailed:'開けませんでした（ローカルサーバー server.py で動かしているか確認）',
    reflected:'{0}：L2 に反映',
    discTitle:'Discussion（新しい順）',
    discHelp:'○ = その Discussion が L2 に反映された Facet、△ = 持ち越し（その Facet を決める材料がある）。○ や列の見出しを押すと Facet ビューアーへ。行を押すと要約が開く。',
    date:'日付',sourceCards:'原典カード',noSourceCards:'なし（会話だけの Discussion）',
    langLabel:'表示言語',sep:'・'
  },
  en:{
    pickSubject:'Choose a Subject',
    pickerHint:'A Subject is one folder under <code>subjects/</code>. To make a new one, ask Claude: "Create a new Subject".',
    noSubjects:'No Subjects found in subjects/.',
    showOld:'old (show deprecated)',
    focusHint:'Say "this" to Claude and it reads what is shown here',
    splitHint:'Drag to resize (double-click to reset)',
    copy:'Copy',copied:'Copied',copyTitle:'Copy {0}',
    focusNoL1:'Facet "{0}" has no L1 yet, so tell Claude the Facet name',
    focusSharing:'Shared with Claude: ',
    facetQ:'Facet "{0}"',ofL1:' L1',
    hasMaterial:'material',notDiscussed:'not discussed',stillEmpty:'(empty)',
    hideReason:'Hidden because: ',notFilled:'(not given)',
    inDiscussion:'In Discussion: ',sources:'Sources: ',derived:'Used by: ',none:'none',
    noL1Yet:'No L1 yet. Discussions with material for deciding it:',
    notDiscussedYet:'This Facet has not been discussed yet.',
    secL1:'L1 Decision',secL2:'L2 Context (reasons, rejected options)',secMaterials:'Discussion materials',
    secDiscs:'Related Discussions',secLinked:'Linked Facets (referencing / referenced by)',
    asset:'File ',open:'Open',openApp:'Open in app',reveal:'Show in folder',
    openFailed:'Could not open the file (is the local server, server.py, running?)',
    reflected:'{0}: reflected in L2',
    discTitle:'Discussions (newest first)',
    discHelp:'○ = this Discussion is reflected in that Facet\'s L2. △ = carried over (material for deciding that Facet). Click a ○ or a column header to open the Facet. Click a row to open its summary.',
    date:'Date',sourceCards:'Source cards',noSourceCards:'none (conversation only)',
    langLabel:'Language',sep:', '
  }
};
const LANGS=Object.keys(I18N),langKey='lattice.lang';
const LANG=(()=>{
  const q=new URLSearchParams(location.search).get('lang');if(LANGS.includes(q))return q;
  try{const s=localStorage.getItem(langKey);if(LANGS.includes(s))return s}catch(e){}
  return (navigator.language||'').toLowerCase().startsWith('ja')?'ja':'en';
})();
document.documentElement.lang=LANG;
// t('copyTitle', x) → 「x をコピー」。{0} {1} … を引数で埋める
function t(k,...a){const s=(I18N[LANG][k]??I18N.ja[k]??k);return s.replace(/\{(\d)\}/g,(_,i)=>a[i]??'')}
// data-i18n（中身）・data-i18n-title（title 属性）を持つ要素に文言を入れる
function applyI18n(){
  for(const el of document.querySelectorAll('[data-i18n]'))el.innerHTML=t(el.dataset.i18n);
  for(const el of document.querySelectorAll('[data-i18n-title]'))el.title=t(el.dataset.i18nTitle);
}
// 言語セレクタ。選んだら覚えて、?lang= を付け替えて読み込み直す
function langSelect(){
  const s=document.createElement('select');s.className='lang';s.title=t('langLabel');s.setAttribute('aria-label',t('langLabel'));
  s.innerHTML=LANGS.map(l=>`<option value="${l}"${l===LANG?' selected':''}>${l.toUpperCase()}</option>`).join('');
  s.onchange=()=>{try{localStorage.setItem(langKey,s.value)}catch(e){}
    const u=new URL(location.href);u.searchParams.set('lang',s.value);location.replace(u)};
  return s;
}
