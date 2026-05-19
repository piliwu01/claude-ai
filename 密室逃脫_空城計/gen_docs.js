const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, PageBreak, HeadingLevel
} = require('docx');
const fs = require('fs');

// A4 尺寸；左右上下各 1440 DXA（1 吋）邊距
// 內容寬度 = 11906 - 2880 = 9026
const PAGE = { width: 11906, height: 16838 };
const MARGIN = { top: 1440, bottom: 1440, left: 1440, right: 1440 };
const CONTENT_WIDTH = 9026;
const FONT = '微軟正黑體';

// 色票
const COL = {
  navy:   '1B3A6B',
  blue:   '2563EB',
  lightBlue: 'DBEAFE',
  gold:   'B45309',
  lightGold: 'FEF3C7',
  red:    'DC2626',
  lightRed: 'FEE2E2',
  green:  '16A34A',
  lightGreen: 'DCFCE7',
  gray:   '475569',
  lightGray: 'F1F5F9',
  white:  'FFFFFF',
  darkBg: '1E293B',
};

// ---------- 輔助函式 ----------

function border(color = 'CCCCCC', size = 4) {
  const b = { style: BorderStyle.SINGLE, size, color };
  return { top: b, bottom: b, left: b, right: b };
}

function noBorder() {
  const b = { style: BorderStyle.NIL, size: 0, color: 'FFFFFF' };
  return { top: b, bottom: b, left: b, right: b };
}

function cell(text, opts = {}) {
  const {
    bold = false, italic = false, size = 22, color = '000000',
    bg = null, align = AlignmentType.LEFT,
    colSpan = 1, w = null,
    borders = border(),
    font = FONT,
  } = opts;
  return new TableCell({
    columnSpan: colSpan,
    width: w ? { size: w, type: WidthType.DXA } : undefined,
    borders,
    shading: bg ? { fill: bg, type: ShadingType.CLEAR } : undefined,
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({
      alignment: align,
      children: [new TextRun({ text, bold, italic, size, color, font })],
    })],
  });
}

function hdr(text, opts = {}) {
  const { size = 36, bold = true, color = COL.navy, align = AlignmentType.CENTER, space = { before: 200, after: 160 } } = opts;
  return new Paragraph({
    alignment: align,
    spacing: space,
    children: [new TextRun({ text, bold, size, color, font: FONT })],
  });
}

function body(text, opts = {}) {
  const { size = 22, bold = false, color = '000000', align = AlignmentType.LEFT,
          indent = 0, space = { before: 40, after: 40 }, italic = false } = opts;
  return new Paragraph({
    alignment: align,
    spacing: space,
    indent: indent ? { left: indent } : undefined,
    children: [new TextRun({ text, bold, size, color, font: FONT, italic })],
  });
}

function separator(color = COL.blue) {
  return new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color, space: 1 } },
    spacing: { before: 80, after: 80 },
    children: [],
  });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

// 難度星號顏色
function difficultyRun(diff) {
  const filled = diff.replace(/★/g, '★').replace(/☆/g, '☆');
  return new TextRun({ text: `難度：${filled}`, size: 20, color: diff.includes('★★★') ? COL.red : diff.includes('★★') ? COL.gold : COL.green, font: FONT });
}

// ---------- 謎題資料 ----------

const puzzles = [
  {
    id: 1, diff: '★☆☆', type: 'G — 撲克牌符號計數', cat: '符號類',
    answer: '421', knowledge: '四門大開、二名書童、一人撫琴',
    title: '第一關：神秘情報',
    storyIntro: '情報員傳來一張用撲克牌花色編成的訊號，必須破解才能得知城內現況！',
    puzzleLines: [
      '城中守備情況以撲克牌花色傳遞：',
      '',
      '　　♠♠♠♠　｜　♥♥　｜　♦',
      '',
      '每種花色出現幾個，就代表一個數字。',
      '三組數字依序排列，即為本關密碼。',
    ],
    makerNote: [
      '製作：將撲克牌花色圖案印在 A5 卡紙上，或直接手繪。',
      '答案解析：',
      '　♠♠♠♠ = 4　（四門大開）',
      '　♥♥   = 2　（兩名書童陪侍）',
      '　♦    = 1　（一人端坐撫琴）',
      '→ 密碼：421',
    ],
    wrongHint: '回想一下：諸葛亮打開了幾扇城門？身邊有幾位書童？城樓上有幾人撫琴？',
    unlock: '密碼正確！情報已確認，西城形勢一覽無遺。',
  },
  {
    id: 2, diff: '★☆☆', type: 'N — 藏頭詩首字提取', cat: '文字類',
    answer: '退兵', knowledge: '空城計的結果——司馬懿退兵',
    title: '第二關：密報文書',
    storyIntro: '城中發現一份可疑的文書，每段話的開頭似乎藏著什麼祕密……',
    puzzleLines: [
      '仔細閱讀以下文書：',
      '',
      '「退可守、進可攻，諸葛亮於城樓之上撫琴，',
      '　神情自若，氣定神閒，從容應對大軍壓境。」',
      '',
      '「兵不厭詐，此乃用兵之道。司馬懿見此情形，',
      '　心生疑惑，恐有伏兵，不敢貿然輕進。」',
      '',
      '取每段話的第一個字，合起來就是本關密碼。',
    ],
    makerNote: [
      '製作：將文書段落印在泛黃信紙樣式的紙張，增加情境感。',
      '答案解析：',
      '　第一段首字：退',
      '　第二段首字：兵',
      '→ 密碼：退兵',
    ],
    wrongHint: '注意看每一段話的第一個字，把它們連起來念念看。',
    unlock: '退兵！司馬懿已撤軍，空城計奏效！',
  },
  {
    id: 3, diff: '★☆☆', type: 'R — 形狀屬性計數', cat: '實物類',
    answer: '346', knowledge: '三國鼎立（3）、四門大開（4）、六出祁山（6）',
    title: '第三關：圖形密碼',
    storyIntro: '城牆上貼著三個神秘圖形，每個圖形的角數藏著故事中的重要數字！',
    puzzleLines: [
      '城牆上貼著三個圖形：',
      '',
      '　　　△　　　　□　　　　⬡',
      '　（三角形）　（正方形）　（六邊形）',
      '',
      '數數每個圖形有幾個角，',
      '按照從左到右的順序排列，即為密碼。',
      '',
      '提示：這三個數字分別對應三國時代的三件大事！',
    ],
    makerNote: [
      '製作：用 Word 插入三種幾何形狀，放大列印成 A5 卡片。',
      '答案解析：',
      '　三角形 = 3角 → 三國鼎立（魏、蜀、吳）',
      '　正方形 = 4角 → 四門大開（空城計關鍵動作）',
      '　六邊形 = 6角 → 六出祁山（諸葛亮北伐六次）',
      '→ 密碼：346',
    ],
    wrongHint: '仔細數一數每個圖形的角：三角形有幾個角？正方形呢？六邊形呢？',
    unlock: '346！三國歷史的關鍵數字都記住了！',
  },
  {
    id: 4, diff: '★★☆', type: 'K — Multi-tap 手機打字法', cat: '符號類',
    answer: 'RUSE', knowledge: '詭計（ruse），空城計的本質',
    title: '第四關：古老電報',
    storyIntro: '截獲一份用古老手機鍵盤輸入法編寫的電報，破解它找出這個英文單字！',
    puzzleLines: [
      '電報密碼：',
      '',
      '　　　777 ── 88 ── 7777 ── 33',
      '',
      '按鍵規則（數字重複幾次 = 按幾次 = 對應字母）：',
      '　2→A  22→B  222→C　　3→D  33→E  333→F',
      '　4→G  44→H  444→I　　5→J  55→K  555→L',
      '　6→M  66→N  666→O　　7→P  77→Q  777→R  7777→S',
      '　8→T  88→U  888→V　　9→W  99→X  999→Y  9999→Z',
      '',
      '破解四個按鍵組合，輸入對應英文單字。',
      '提示：這個詞在英文中意思是「計謀、詭計」。',
    ],
    makerNote: [
      '製作：將電報密碼寫在電報紙樣式卡片上，附按鍵對照表。',
      '答案解析：',
      '　777  → R（7鍵按3次）',
      '　88   → U（8鍵按2次）',
      '　7777 → S（7鍵按4次）',
      '　33   → E（3鍵按2次）',
      '→ 密碼：RUSE（英文：計謀、詭計）',
      '教學延伸：RUSE 正是空城計的英文詮釋，可讓學生討論中英對應。',
    ],
    wrongHint: '每個數字出現幾次，就按那個鍵幾次。例如 777 是按「7」三次，查表找第三個字母。',
    unlock: 'RUSE！計謀正是空城計的精髓！',
  },
  {
    id: 5, diff: '★★☆', type: 'H — 英數對照（A=01…Z=26）', cat: '文字類',
    answer: 'WEI', knowledge: '魏（Wei）國，司馬懿所屬',
    title: '第五關：數字情報',
    storyIntro: '截獲一份敵軍傳遞的數字情報，用英數對照法解碼，找出入侵西城的國家！',
    puzzleLines: [
      '情報數字：',
      '',
      '　　　23 ── 05 ── 09',
      '',
      '解碼規則：A=01, B=02, C=03 … Z=26',
      '',
      '將每個數字對應到英文字母，',
      '組合成一個英文單字，即為本關密碼。',
      '',
      '提示：這是入侵西城的國家名稱（漢語拼音）。',
    ],
    makerNote: [
      '製作：將數字印在情報紙條上，並附英數對照表。',
      '答案解析：',
      '　23 → W',
      '　05 → E',
      '　09 → I',
      '→ 密碼：WEI（魏國）',
      '教學延伸：可討論魏、蜀、吳三國各自的漢語拼音。',
    ],
    wrongHint: 'A=01, B=02, C=03……以此類推，23 對應哪個字母？05 呢？09 呢？',
    unlock: 'WEI！魏國，司馬懿正是魏國大將！',
  },
  {
    id: 6, diff: '★★☆', type: 'B — 漢字部件拼合', cat: '文字類',
    answer: '空城', knowledge: '空城計的核心場景——空城',
    title: '第六關：殘破紙片',
    storyIntro: '城中發現四張殘破的紙片，拼合成兩個漢字就是本關密碼！',
    puzzleLines: [
      '四張殘破紙片：',
      '',
      '　　【穴】　【工】　【土】　【成】',
      '',
      '這四個部件可以組合成兩個漢字，',
      '就是空城計的核心場景名稱。',
      '',
      '提示：',
      '　• 其中兩個部件合成一個字（上下結構）',
      '　• 另外兩個部件合成另一個字（左右結構）',
    ],
    makerNote: [
      '製作：將四個部件分別寫在小紙片或磁鐵字卡上，打亂順序分發。',
      '答案解析：',
      '　穴（上）+ 工（下）= 空',
      '　土（偏旁）+ 成（右邊）= 城',
      '→ 密碼：空城',
      '教學延伸：「城」的部首是土，成是聲旁，可說明形聲字結構。',
    ],
    wrongHint: '想一想「穴」加「工」拼成什麼字？「土」加「成」呢？',
    unlock: '空城！正是諸葛亮以空城退敵的關鍵！',
  },
  {
    id: 7, diff: '★★☆', type: 'W — 日常文件藏碼', cat: '文字類',
    answer: '西城', knowledge: '空城計發生地點——西城',
    title: '第七關：蜀漢密報',
    storyIntro: '截獲一份蜀漢的軍情急報，每段話的第一個字藏著重要地名……',
    puzzleLines: [
      '【蜀漢軍情急報】　（建興六年，緊急文書）',
      '',
      '「西望魏軍旌旗蔽野，十五萬大軍壓境而來，',
      '　情勢萬分危急，需即刻研擬對策。」',
      '',
      '「城中兵力不足，守備薄弱，',
      '　幸得丞相運籌帷幄，以計退敵。」',
      '',
      '取每段話的第一個字，合起來就是本關密碼。',
    ],
    makerNote: [
      '製作：設計成仿古文書風格（黃底紅印）的 A5 紙張。',
      '答案解析：',
      '　第一段首字：西',
      '　第二段首字：城',
      '→ 密碼：西城（空城計的發生地點）',
    ],
    wrongHint: '找出每一段的第一個字，連起來就是一個地名。',
    unlock: '西城！正是空城計發生的所在地！',
  },
  {
    id: 8, diff: '★★☆', type: 'A — 摩斯電碼', cat: '符號類',
    answer: 'CALM', knowledge: '諸葛亮沉著鎮定的特質',
    title: '第八關：城樓訊號',
    storyIntro: '城樓上傳來有節奏的敲擊聲，這是摩斯電碼，破解它找出諸葛亮最重要的特質！',
    puzzleLines: [
      '城樓傳來的敲擊聲（·短音  —長音）：',
      '',
      '　　—·—·　/　·—　/　·—··　/　——',
      '',
      '摩斯電碼對照表：',
      'A ·—　　B —···　C —·—·　D —··　　E ·',
      'F ··—·　G ——·　 H ····　 I ··　　 J ·———',
      'K —·—　 L ·—··　M ——　　N —·　　 O ———',
      'P ·——·　Q ——·—　R ·—·　 S ···　　T —',
      'U ··—　 V ···—　W ·——　 X —··—　Y —·——',
      'Z ——··',
      '',
      '破解四組電碼，組合成一個英文單字。',
      '提示：這個詞描述諸葛亮面對大軍壓境時的心理狀態。',
    ],
    makerNote: [
      '製作：將摩斯電碼印在卡片上，可用長短線條表示。',
      '答案解析：',
      '　—·—· → C',
      '　·—   → A',
      '　·—·· → L',
      '　——   → M',
      '→ 密碼：CALM（沉著、鎮定）',
      '教學延伸：討論諸葛亮的心理素質——危機中保持鎮定是成功關鍵。',
    ],
    wrongHint: '對照摩斯電碼表，每組符號對應一個英文字母。這個詞的意思是「冷靜、鎮定」。',
    unlock: 'CALM！沉著鎮定，正是諸葛亮成功的關鍵！',
  },
  {
    id: 9, diff: '★★★', type: 'I — 注音重組', cat: '文字類',
    answer: '城樓', knowledge: '諸葛亮撫琴的地點——城樓',
    title: '第九關：注音謎題',
    storyIntro: '發現一張殘破紙條，上面寫著兩個字，但這兩個字的注音可以重新組合成另一個詞！',
    puzzleLines: [
      '紙條上寫著：「樓程」',
      '',
      '　樓　→　注音：ㄌㄡˊ',
      '　程　→　注音：ㄔㄥˊ',
      '',
      '將這兩個字的注音拆散重組，',
      '可以拼出另一個跟空城計場景有關的詞語。',
      '',
      '提示：諸葛亮端坐撫琴的地方叫什麼？',
    ],
    makerNote: [
      '製作：將「樓程」寫在殘破風格的紙條上。',
      '答案解析：',
      '　樓 ㄌㄡˊ + 程 ㄔㄥˊ',
      '　↓ 注音互換',
      '　ㄔㄥˊ + ㄌㄡˊ → 城樓',
      '→ 密碼：城樓',
      '教學延伸：「程」和「城」注音相同（ㄔㄥˊ），可藉此討論同音字。',
    ],
    wrongHint: '「程」的注音是 ㄔㄥˊ，「樓」的注音是 ㄌㄡˊ。換個順序拼，ㄔㄥˊ＋ㄌㄡˊ 是哪兩個字？',
    unlock: '城樓！諸葛亮正是在城樓上端坐撫琴，退敵於無形！',
  },
  {
    id: 10, diff: '★★★', type: 'J — 詩文坐標', cat: '數字類',
    answer: '空城退敵', knowledge: '空城計的核心精神',
    title: '第十關（最終關）：藏寶圖文',
    storyIntro: '最終關卡！一段改寫自空城計的文字藏著密碼，依照坐標指示，找出四個關鍵字！',
    puzzleLines: [
      '以下是改寫自空城計的四行文字',
      '（不含標點，逐字計算）：',
      '',
      '第1行：諸葛孔明使出空城之計',
      '第2行：打開四門城樓端坐撫琴',
      '第3行：司馬懿見狀退兵而去不敢輕進',
      '第4行：蜀軍得保此役退敵大功告成',
      '',
      '坐標（→第幾字，↓第幾行）：',
      '',
      '　(→7,↓1)　(→5,↓2)　(→6,↓3)　(→8,↓4)',
      '',
      '依序找出四個字，組合成本關密碼！',
    ],
    makerNote: [
      '製作：將四行文字印在卡片上，附坐標指引。',
      '答案解析（不計標點）：',
      '　第1行：諸(1)葛(2)孔(3)明(4)使(5)出(6)空(7)… → (→7,↓1) = 空',
      '　第2行：打(1)開(2)四(3)門(4)城(5)… → (→5,↓2) = 城',
      '　第3行：司(1)馬(2)懿(3)見(4)狀(5)退(6)… → (→6,↓3) = 退',
      '　第4行：蜀(1)軍(2)得(3)保(4)此(5)役(6)退(7)敵(8)… → (→8,↓4) = 敵',
      '→ 密碼：空城退敵',
      '備注：可讓學生用鉛筆在文字上標注數字，再找對應位置。',
    ],
    wrongHint: '從左往右數字，不計標點。第1行第7個字是哪個？第2行第5個呢？',
    unlock: '空城退敵！你們成功破解了所有密碼，協助諸葛亮完成了空城計！恭喜逃脫成功！',
  },
];

// ========== 教師版腳本 ==========

function buildTeacher() {
  const children = [];

  // 封面
  children.push(
    body('', { space: { before: 720, after: 0 } }),
    hdr('🎮 密室逃脫活動腳本', { size: 52, space: { before: 1000, after: 200 } }),
    hdr('《空城計》主題　教師版', { size: 36, color: COL.gold, space: { before: 0, after: 200 } }),
    hdr('國中二年級　國文科', { size: 28, color: COL.gray, space: { before: 0, after: 100 } }),
    hdr('本文件含完整答案與製作說明', { size: 22, color: COL.red, space: { before: 0, after: 800 } }),
    separator(COL.navy),
  );

  // 活動概述
  children.push(
    body('', { space: { before: 200, after: 0 } }),
    hdr('【活動概述】', { align: AlignmentType.LEFT, size: 30, space: { before: 200, after: 120 } }),
  );

  const overviewRows = [
    ['主題', '《空城計》（三國演義）'],
    ['適用年級', '國中二年級'],
    ['建議時間', '60～80 分鐘'],
    ['分組建議', '3～4 人一組，各組一份學生謎題卡'],
    ['關卡數', '共 10 關（由易到難）'],
    ['串鏈機制', '答對後告知老師密碼，才能領取下一關卡片'],
    ['結局', '全部解完即「逃脫成功」，可頒發獎狀或獎品'],
  ];
  const col1 = 2200, col2 = 6826;
  children.push(new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [col1, col2],
    rows: overviewRows.map(([k, v], i) =>
      new TableRow({ children: [
        cell(k, { bold: true, bg: COL.lightBlue, w: col1, borders: border(COL.blue, 4) }),
        cell(v, { w: col2, borders: border(COL.blue, 4) }),
      ]})
    ),
  }));

  // 故事情境
  children.push(
    body('', { space: { before: 240, after: 0 } }),
    separator(COL.navy),
    body('', { space: { before: 120, after: 0 } }),
    hdr('【故事情境（老師開場朗讀）】', { align: AlignmentType.LEFT, size: 30, space: { before: 0, after: 120 } }),
    body('你是蜀漢的年輕謀士，奉命協助諸葛亮守衛西城。', { size: 22, space: { before: 60, after: 40 } }),
    body('魏軍司馬懿率領十五萬大軍壓境，城中守備空虛，形勢萬分危急！', { size: 22, space: { before: 0, after: 40 } }),
    body('丞相諸葛亮決定使出「空城計」，但計謀能否成功，端賴你們解開 10 道謎題，', { size: 22, space: { before: 0, after: 40 } }),
    body('穩定軍心、傳遞情報，讓司馬懿知難而退！', { size: 22, space: { before: 0, after: 40 } }),
    body('', { space: { before: 80, after: 0 } }),
    body('時間緊迫，使命必達——謀士們，準備好了嗎？', { size: 22, bold: true, color: COL.red, space: { before: 0, after: 120 } }),
    separator(COL.navy),
  );

  // 關卡總覽表
  children.push(
    body('', { space: { before: 200, after: 0 } }),
    hdr('【關卡總覽】', { align: AlignmentType.LEFT, size: 30, space: { before: 0, after: 120 } }),
  );
  const w = [600, 2200, 1100, 800, 1300, 3026];
  children.push(new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: w,
    rows: [
      new TableRow({ children: [
        cell('關卡', { bold: true, bg: COL.navy, color: COL.white, w: w[0], align: AlignmentType.CENTER }),
        cell('謎型', { bold: true, bg: COL.navy, color: COL.white, w: w[1] }),
        cell('類別', { bold: true, bg: COL.navy, color: COL.white, w: w[2] }),
        cell('難度', { bold: true, bg: COL.navy, color: COL.white, w: w[3], align: AlignmentType.CENTER }),
        cell('答案', { bold: true, bg: COL.navy, color: COL.white, w: w[4], align: AlignmentType.CENTER }),
        cell('知識點', { bold: true, bg: COL.navy, color: COL.white, w: w[5] }),
      ]}),
      ...puzzles.map((p, i) =>
        new TableRow({ children: [
          cell(`第${p.id}關`, { align: AlignmentType.CENTER, bg: i % 2 ? null : COL.lightGray, w: w[0] }),
          cell(p.type, { bg: i % 2 ? null : COL.lightGray, w: w[1], size: 20 }),
          cell(p.cat, { bg: i % 2 ? null : COL.lightGray, w: w[2] }),
          cell(p.diff, { align: AlignmentType.CENTER, bg: i % 2 ? null : COL.lightGray, w: w[3] }),
          cell(p.answer, { bold: true, color: COL.blue, align: AlignmentType.CENTER, bg: i % 2 ? null : COL.lightGray, w: w[4] }),
          cell(p.knowledge, { bg: i % 2 ? null : COL.lightGray, w: w[5], size: 20 }),
        ]})
      ),
    ],
  }));

  // 每一關詳細說明
  for (const p of puzzles) {
    children.push(pageBreak());

    // 關卡標題
    const bg = p.diff === '★☆☆' ? COL.lightGreen : p.diff === '★★☆' ? COL.lightGold : COL.lightRed;
    const fc = p.diff === '★☆☆' ? COL.green : p.diff === '★★☆' ? COL.gold : COL.red;
    children.push(
      new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [CONTENT_WIDTH],
        rows: [new TableRow({ children: [
          new TableCell({
            width: { size: CONTENT_WIDTH, type: WidthType.DXA },
            borders: border(fc, 8),
            shading: { fill: bg, type: ShadingType.CLEAR },
            margins: { top: 120, bottom: 120, left: 200, right: 200 },
            children: [
              new Paragraph({ children: [
                new TextRun({ text: `【第 ${p.id} 關】　${p.title.replace('第'+p.id+'關：','').trim()}`, bold: true, size: 32, font: FONT, color: fc }),
              ]}),
              new Paragraph({ children: [
                new TextRun({ text: `謎型：${p.type}　　類別：${p.cat}　　`, size: 20, font: FONT, color: COL.gray }),
                difficultyRun(p.diff),
              ]}),
            ],
          }),
        ]})],
      }),
    );

    children.push(body('', { space: { before: 100, after: 0 } }));

    // 逆推設計說明
    children.push(
      hdr('▶ 逆推設計說明', { align: AlignmentType.LEFT, size: 24, color: COL.navy, space: { before: 80, after: 60 } }),
      body(`先決定答案：「${p.answer}」（${p.knowledge}）`, { size: 21, indent: 360 }),
      body(`再逆推：如何把「${p.answer}」藏進謎題裡，讓學生透過解碼得出答案。`, { size: 21, indent: 360, space: { before: 0, after: 120 } }),
    );

    // 題目說明
    children.push(
      hdr('▶ 題目說明（對學生朗讀）', { align: AlignmentType.LEFT, size: 24, color: COL.navy, space: { before: 80, after: 60 } }),
      body(p.storyIntro, { size: 21, indent: 360, italic: true, space: { before: 0, after: 80 } }),
    );

    // 謎題卡框
    children.push(new Table({
      width: { size: CONTENT_WIDTH, type: WidthType.DXA },
      columnWidths: [CONTENT_WIDTH],
      rows: [new TableRow({ children: [
        new TableCell({
          width: { size: CONTENT_WIDTH, type: WidthType.DXA },
          borders: border(COL.blue, 6),
          shading: { fill: 'F0F9FF', type: ShadingType.CLEAR },
          margins: { top: 120, bottom: 120, left: 240, right: 240 },
          children: p.puzzleLines.map(line =>
            new Paragraph({ spacing: { before: 20, after: 20 }, children: [
              new TextRun({ text: line || ' ', size: 22, font: FONT }),
            ]})
          ),
        }),
      ]})],
    }));

    // 製作方式
    children.push(
      body('', { space: { before: 100, after: 0 } }),
      hdr('▶ 製作方式與答案', { align: AlignmentType.LEFT, size: 24, color: COL.navy, space: { before: 80, after: 60 } }),
    );
    for (const line of p.makerNote) {
      children.push(body(line, { size: 21, indent: 360, space: { before: 10, after: 10 } }));
    }

    // 答案框
    children.push(
      body('', { space: { before: 80, after: 0 } }),
      new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [CONTENT_WIDTH],
        rows: [new TableRow({ children: [
          new TableCell({
            borders: border(COL.green, 8),
            shading: { fill: COL.lightGreen, type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 200, right: 200 },
            children: [new Paragraph({ children: [
              new TextRun({ text: `✅  正確答案：${p.answer}`, bold: true, size: 24, font: FONT, color: COL.green }),
            ]})],
          }),
        ]})],
      }),
    );

    // 錯誤提示 + 解鎖台詞
    children.push(
      body('', { space: { before: 100, after: 0 } }),
      hdr('▶ 答錯時的提示台詞', { align: AlignmentType.LEFT, size: 24, color: COL.navy, space: { before: 80, after: 60 } }),
      new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [CONTENT_WIDTH],
        rows: [new TableRow({ children: [
          new TableCell({
            borders: border(COL.gold, 6),
            shading: { fill: COL.lightGold, type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 200, right: 200 },
            children: [new Paragraph({ children: [
              new TextRun({ text: p.wrongHint, size: 22, font: FONT, italic: true }),
            ]})],
          }),
        ]})],
      }),
      body('', { space: { before: 100, after: 0 } }),
      hdr('▶ 解鎖台詞（答對時說）', { align: AlignmentType.LEFT, size: 24, color: COL.navy, space: { before: 80, after: 60 } }),
      new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [CONTENT_WIDTH],
        rows: [new TableRow({ children: [
          new TableCell({
            borders: border(COL.blue, 6),
            shading: { fill: COL.lightBlue, type: ShadingType.CLEAR },
            margins: { top: 80, bottom: 80, left: 200, right: 200 },
            children: [new Paragraph({ children: [
              new TextRun({ text: p.unlock, size: 22, font: FONT, bold: true }),
            ]})],
          }),
        ]})],
      }),
    );
  }

  // 教學建議
  children.push(
    pageBreak(),
    hdr('【教學建議】', { align: AlignmentType.LEFT, size: 30, space: { before: 0, after: 200 } }),
    separator(COL.navy),
    body('', { space: { before: 120, after: 0 } }),
  );
  const tips = [
    ['分組方式', '3～4 人一組，確保每人都有參與機會'],
    ['卡片發放', '老師手中保管所有關卡卡片，答對才發下一張，避免學生跳關'],
    ['時間控制', '10 關建議共 60～80 分鐘；可視狀況提供提示'],
    ['差異化', '難度較低的前三關（★☆☆）可讓程度較弱的學生先解，建立信心'],
    ['課文連結', '第 10 關詩文坐標使用課文改寫段落，鼓勵學生回頭查閱課文'],
    ['結尾活動', '全班解完後，可討論「你覺得空城計成功的關鍵是什麼？」'],
  ];
  const tw = [2500, 6526];
  children.push(new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: tw,
    rows: tips.map(([k, v], i) =>
      new TableRow({ children: [
        cell(k, { bold: true, bg: i % 2 ? null : COL.lightBlue, w: tw[0], borders: border(COL.blue, 4) }),
        cell(v, { bg: i % 2 ? null : COL.lightBlue, w: tw[1], borders: border(COL.blue, 4) }),
      ]})
    ),
  }));

  return new Document({
    styles: {
      default: { document: { run: { font: FONT, size: 22 } } },
    },
    sections: [{
      properties: { page: { size: PAGE, margin: MARGIN } },
      children,
    }],
  });
}

// ========== 學生謎題卡 ==========

function buildStudent() {
  const children = [];

  // 故事開場
  children.push(
    body('', { space: { before: 400, after: 0 } }),
    hdr('⚔️  密室逃脫：空城計', { size: 48, space: { before: 0, after: 160 } }),
    hdr('── 學生謎題卡 ──', { size: 28, color: COL.gray, space: { before: 0, after: 300 } }),
    separator(COL.navy),
    body('', { space: { before: 160, after: 0 } }),
    hdr('【任務說明】', { align: AlignmentType.LEFT, size: 28, space: { before: 0, after: 120 } }),
  );

  for (const line of [
    '你是蜀漢的年輕謀士，奉命協助諸葛亮守衛西城。',
    '魏軍司馬懿率領十五萬大軍壓境，形勢萬分危急！',
    '丞相諸葛亮決定使出「空城計」——',
    '你必須破解 10 道謎題，協助計謀成功，讓司馬懿知難而退！',
    '',
    '【規則】',
    '• 每解開一關，將答案告訴老師確認',
    '• 答對才能領取下一關卡片',
    '• 全部解完，即逃脫成功！',
    '',
    '時間緊迫，使命必達——謀士們，準備好了嗎？',
  ]) {
    children.push(body(line, { size: 22, space: { before: 40, after: 40 }, bold: line.startsWith('•') || line.startsWith('【') }));
  }

  children.push(separator(COL.navy));

  // 每一關謎題卡
  for (const p of puzzles) {
    children.push(pageBreak());

    const bg = p.diff === '★☆☆' ? COL.lightGreen : p.diff === '★★☆' ? COL.lightGold : COL.lightRed;
    const fc = p.diff === '★☆☆' ? COL.green : p.diff === '★★☆' ? COL.gold : COL.red;

    // 卡片標題
    children.push(new Table({
      width: { size: CONTENT_WIDTH, type: WidthType.DXA },
      columnWidths: [CONTENT_WIDTH],
      rows: [new TableRow({ children: [
        new TableCell({
          borders: border(fc, 10),
          shading: { fill: bg, type: ShadingType.CLEAR },
          margins: { top: 160, bottom: 160, left: 240, right: 240 },
          children: [
            new Paragraph({ alignment: AlignmentType.CENTER, children: [
              new TextRun({ text: p.title, bold: true, size: 36, font: FONT, color: fc }),
            ]}),
            new Paragraph({ alignment: AlignmentType.CENTER, children: [
              new TextRun({ text: `謎型：${p.type}　　難度：${p.diff}`, size: 20, font: FONT, color: COL.gray }),
            ]}),
          ],
        }),
      ]})],
    }));

    // 故事情境
    children.push(
      body('', { space: { before: 120, after: 0 } }),
      body(p.storyIntro, { size: 22, italic: true, color: COL.navy, space: { before: 0, after: 120 } }),
      separator(COL.gray),
    );

    // 謎題卡
    children.push(
      body('', { space: { before: 100, after: 0 } }),
      new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [CONTENT_WIDTH],
        rows: [new TableRow({ children: [
          new TableCell({
            borders: border(COL.blue, 6),
            shading: { fill: 'F8FAFF', type: ShadingType.CLEAR },
            margins: { top: 160, bottom: 160, left: 280, right: 280 },
            children: p.puzzleLines.map(line =>
              new Paragraph({ spacing: { before: 40, after: 40 }, children: [
                new TextRun({ text: line || ' ', size: 23, font: FONT }),
              ]})
            ),
          }),
        ]})],
      }),
    );

    // 作答區
    children.push(
      body('', { space: { before: 200, after: 0 } }),
      separator(COL.gray),
      body('', { space: { before: 120, after: 0 } }),
      body('我的答案：　　　　　　　　　　　', { size: 24, bold: true, space: { before: 0, after: 40 } }),
      body('（答案告訴老師確認後，才能領取下一關卡片）', { size: 20, color: COL.gray, italic: true }),
    );
  }

  return new Document({
    styles: {
      default: { document: { run: { font: FONT, size: 22 } } },
    },
    sections: [{
      properties: { page: { size: PAGE, margin: MARGIN } },
      children,
    }],
  });
}

// ========== 執行生成 ==========

const outDir = __dirname;

Promise.all([
  Packer.toBuffer(buildTeacher()),
  Packer.toBuffer(buildStudent()),
]).then(([teacherBuf, studentBuf]) => {
  fs.writeFileSync(`${outDir}/教師版腳本_空城計密室逃脫.docx`, teacherBuf);
  fs.writeFileSync(`${outDir}/學生謎題卡_空城計密室逃脫.docx`, studentBuf);
  console.log('✅ 兩份檔案已生成！');
  console.log(`   教師版腳本_空城計密室逃脫.docx`);
  console.log(`   學生謎題卡_空城計密室逃脫.docx`);
}).catch(err => {
  console.error('❌ 生成失敗：', err);
  process.exit(1);
});
