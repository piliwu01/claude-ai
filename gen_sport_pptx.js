const pptxgen = require("pptxgenjs");

const ORANGE = "FF5A00";
const BLACK = "000000";
const GRAY = "555555";
const WHITE = "FFFFFF";
const FONT = "微軟正黑體";

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "運動家的風度";

// ============= P1 封面頁 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("運動家的風度", {
    x: 1, y: 1.8, w: 8, h: 1.1,
    fontFace: FONT, fontSize: 40, bold: true, color: BLACK, align: "center"
  });
  s.addText("贏了還不夠——談競爭的道德", {
    x: 1, y: 3.1, w: 8, h: 0.6,
    fontFace: FONT, fontSize: 18, color: ORANGE, align: "center"
  });
  s.addText("羅家倫", {
    x: 1, y: 3.9, w: 8, h: 0.5,
    fontFace: FONT, fontSize: 14, color: GRAY, align: "center"
  });
}

// ============= P2 動機觸發頁 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("你輸過嗎？你當時怎麼做？", {
    x: 0.5, y: 0.35, w: 9, h: 0.7,
    fontFace: FONT, fontSize: 28, bold: true, color: BLACK, align: "center"
  });
  s.addShape(pres.shapes.LINE, {
    x: 4.9, y: 1.3, w: 0, h: 3.5,
    line: { color: "EEEEEE", width: 1 }
  });
  s.addText("❌ 你可能的反應", {
    x: 0.4, y: 1.3, w: 4.2, h: 0.5,
    fontFace: FONT, fontSize: 14, bold: true, color: "CC0000", align: "center"
  });
  s.addText([
    { text: "罵裁判不公平", options: { bullet: true, breakLine: true } },
    { text: "說對方只是走運", options: { bullet: true, breakLine: true } },
    { text: "下次一定要贏回來", options: { bullet: true } }
  ], {
    x: 0.7, y: 2.0, w: 3.8, h: 2.0,
    fontFace: FONT, fontSize: 14, color: GRAY
  });
  s.addText("✅ 有風度的反應？", {
    x: 5.1, y: 1.3, w: 4.4, h: 0.5,
    fontFace: FONT, fontSize: 14, bold: true, color: "007700", align: "center"
  });
  // 右欄留空（教師引導後揭示）
  s.addText("（教師引導後揭示）", {
    x: 5.2, y: 2.5, w: 4.0, h: 0.5,
    fontFace: FONT, fontSize: 12, color: "DDDDDD", align: "center", italic: true
  });
}

// ============= P3 作者脈絡頁 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("他為什麼有資格說這件事？", {
    x: 0.5, y: 0.3, w: 9, h: 0.7,
    fontFace: FONT, fontSize: 28, bold: true, color: BLACK, align: "center"
  });
  // 時間軸橫線
  s.addShape(pres.shapes.LINE, {
    x: 1.0, y: 2.5, w: 8.0, h: 0,
    line: { color: "CCCCCC", width: 2 }
  });
  const nodes = [
    { cx: 1.8, label: "1919 年", desc: "五四運動\n主要發起者之一" },
    { cx: 5.0, label: "留學歐美", desc: "親眼見識\n西方運動精神" },
    { cx: 8.2, label: "1942 年", desc: "戰亂中發表\n此演講稿" }
  ];
  for (const n of nodes) {
    s.addShape(pres.shapes.OVAL, {
      x: n.cx - 0.15, y: 2.35, w: 0.3, h: 0.3,
      fill: { color: ORANGE }, line: { color: ORANGE }
    });
    s.addText(n.label, {
      x: n.cx - 1.1, y: 1.55, w: 2.2, h: 0.5,
      fontFace: FONT, fontSize: 13, bold: true, color: BLACK, align: "center", margin: 0
    });
    s.addText(n.desc, {
      x: n.cx - 1.1, y: 2.75, w: 2.2, h: 0.9,
      fontFace: FONT, fontSize: 12, color: GRAY, align: "center", margin: 0
    });
  }
  s.addText("當時中國正值戰亂，他提倡的不只是運動，是民族性的重建。", {
    x: 0.8, y: 4.55, w: 8.4, h: 0.6,
    fontFace: FONT, fontSize: 14, color: GRAY, align: "center", italic: true
  });
}

// ============= P4 運動三層意義 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("運動的意義，不只一層", {
    x: 0.5, y: 0.25, w: 9, h: 0.7,
    fontFace: FONT, fontSize: 28, bold: true, color: BLACK, align: "center"
  });
  // 第一層（底，最大）
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 4.0, w: 8.8, h: 0.95,
    fill: { color: "F5F5F5" }, line: { color: "DDDDDD", width: 1 }
  });
  s.addText([
    { text: "健康　", options: { bold: true, color: BLACK } },
    { text: "體力是一生成功的基礎", options: { color: GRAY } }
  ], {
    x: 0.6, y: 4.0, w: 8.8, h: 0.95,
    fontFace: FONT, fontSize: 14, align: "center", valign: "middle"
  });
  // 第二層（中）
  s.addShape(pres.shapes.RECTANGLE, {
    x: 1.6, y: 2.85, w: 6.8, h: 0.95,
    fill: { color: "EEEEEE" }, line: { color: "CCCCCC", width: 1 }
  });
  s.addText([
    { text: "心靈健全　", options: { bold: true, color: BLACK } },
    { text: "健全心靈寓於健全身體", options: { color: GRAY } }
  ], {
    x: 1.6, y: 2.85, w: 6.8, h: 0.95,
    fontFace: FONT, fontSize: 14, align: "center", valign: "middle"
  });
  // 第三層（頂，最小，橘框）
  s.addShape(pres.shapes.RECTANGLE, {
    x: 2.8, y: 1.7, w: 4.4, h: 0.95,
    fill: { color: WHITE }, line: { color: ORANGE, width: 2 }
  });
  s.addText([
    { text: "道德意義　", options: { bold: true, color: ORANGE } },
    { text: "在運動場上養成人生的正大態度", options: { color: BLACK } }
  ], {
    x: 2.8, y: 1.7, w: 4.1, h: 0.95,
    fontFace: FONT, fontSize: 13, align: "center", valign: "middle"
  });
  s.addText("← 本課的核心在這裡", {
    x: 7.25, y: 1.9, w: 2.4, h: 0.5,
    fontFace: FONT, fontSize: 11, color: ORANGE
  });
}

// ============= P5 君子之爭典故 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("古人早就示範過了", {
    x: 0.5, y: 0.25, w: 9, h: 0.65,
    fontFace: FONT, fontSize: 28, bold: true, color: BLACK, align: "center"
  });
  const boxes = [
    { x: 0.3, title: "賽前互揖", desc: "雙方拱手行禮，\n讓對方先登射堂" },
    { x: 3.65, title: "認真比賽", desc: "全力以赴，\n光明競爭" },
    { x: 7.0, title: "賽後敬酒", desc: "勝者請輸者喝酒，\n以禮相待" }
  ];
  for (let i = 0; i < boxes.length; i++) {
    const b = boxes[i];
    s.addShape(pres.shapes.RECTANGLE, {
      x: b.x, y: 1.2, w: 2.7, h: 1.8,
      fill: { color: "F8F8F8" }, line: { color: "DDDDDD", width: 1 }
    });
    s.addText(b.title, {
      x: b.x, y: 1.25, w: 2.7, h: 0.55,
      fontFace: FONT, fontSize: 15, bold: true, color: BLACK, align: "center"
    });
    s.addText(b.desc, {
      x: b.x + 0.1, y: 1.9, w: 2.5, h: 0.9,
      fontFace: FONT, fontSize: 12, color: GRAY, align: "center"
    });
    if (i < 2) {
      s.addText("▶", {
        x: b.x + 2.7, y: 1.85, w: 0.95, h: 0.5,
        fontFace: FONT, fontSize: 16, color: ORANGE, align: "center", margin: 0
      });
    }
  }
  s.addText("這就是羅家倫所說的——君子之爭。", {
    x: 1.0, y: 3.3, w: 8.0, h: 0.45,
    fontFace: FONT, fontSize: 14, color: GRAY, align: "center", italic: true
  });
  s.addText("「君子無所爭，必也射乎。揖讓而升，下而飲，其爭也君子。——論語八佾篇」", {
    x: 0.5, y: 4.0, w: 9.0, h: 0.6,
    fontFace: FONT, fontSize: 11, color: "AAAAAA", align: "center"
  });
}

// ============= P6 風度一 正大光明的態度 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("風度一｜正大光明的態度", {
    x: 0.5, y: 0.2, w: 9, h: 0.65,
    fontFace: FONT, fontSize: 28, bold: true, color: BLACK, align: "center"
  });
  s.addText("在萬目睽睽下，仍選擇光明正大", {
    x: 0.5, y: 0.9, w: 9, h: 0.4,
    fontFace: FONT, fontSize: 14, color: GRAY, align: "center"
  });
  s.addShape(pres.shapes.LINE, {
    x: 4.85, y: 1.45, w: 0, h: 2.7,
    line: { color: "EEEEEE", width: 1 }
  });
  s.addText("❌ 沒風度的做法", {
    x: 0.4, y: 1.45, w: 4.2, h: 0.5,
    fontFace: FONT, fontSize: 14, bold: true, color: "CC0000", align: "center"
  });
  s.addText([
    { text: "• 暗箭傷人", options: { breakLine: true } },
    { text: "• 犯規取勝" }
  ], {
    x: 0.7, y: 2.1, w: 3.8, h: 1.0,
    fontFace: FONT, fontSize: 14, color: GRAY
  });
  s.addText("✅ 有風度的做法", {
    x: 5.1, y: 1.45, w: 4.4, h: 0.5,
    fontFace: FONT, fontSize: 14, bold: true, color: "007700", align: "center"
  });
  s.addText([
    { text: "• 公開競爭，守著規律", options: { breakLine: true, color: ORANGE } },
    { text: "• 不屑採取不光明的手段", options: { color: ORANGE } }
  ], {
    x: 5.2, y: 2.1, w: 4.3, h: 1.0,
    fontFace: FONT, fontSize: 14
  });
  s.addText("「雖然犯規可能得勝，但這是有風度的運動家引為恥辱的。」", {
    x: 0.5, y: 4.35, w: 9, h: 0.7,
    fontFace: FONT, fontSize: 14, color: "333333", align: "center", italic: true
  });
}

// ============= P7 風度二 服輸的精神 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("風度二｜服輸的精神", {
    x: 0.5, y: 0.2, w: 9, h: 0.65,
    fontFace: FONT, fontSize: 28, bold: true, color: BLACK, align: "center"
  });
  s.addText("輸了，然後呢？", {
    x: 0.5, y: 0.9, w: 9, h: 0.4,
    fontFace: FONT, fontSize: 14, color: GRAY, align: "center"
  });
  const steps = [
    { x: 0.4, y: 3.2, label: "不怨天，不尤人", desc: "輸了不怪別人，不怪環境", accent: false },
    { x: 3.1, y: 2.5, label: "找出自身問題", desc: "我輸了只怪我自己不行", accent: false },
    { x: 5.8, y: 1.8, label: "充實改進，下次再來", desc: "等我改進以後，下次再來", accent: true }
  ];
  for (let i = 0; i < steps.length; i++) {
    const st = steps[i];
    s.addShape(pres.shapes.RECTANGLE, {
      x: st.x, y: st.y, w: 2.5, h: 1.5,
      fill: { color: st.accent ? "FFF3ED" : "F8F8F8" },
      line: { color: st.accent ? ORANGE : "DDDDDD", width: st.accent ? 2 : 1 }
    });
    s.addText(st.label, {
      x: st.x + 0.1, y: st.y + 0.1, w: 2.3, h: 0.55,
      fontFace: FONT, fontSize: 13, bold: true,
      color: st.accent ? ORANGE : BLACK, align: "center"
    });
    s.addText(st.desc, {
      x: st.x + 0.1, y: st.y + 0.72, w: 2.3, h: 0.65,
      fontFace: FONT, fontSize: 11, color: GRAY, align: "center"
    });
    if (i < 2) {
      s.addText("→", {
        x: st.x + 2.5, y: st.y + 0.45, w: 0.6, h: 0.55,
        fontFace: FONT, fontSize: 18, color: ORANGE, align: "center", margin: 0
      });
    }
  }
  s.addText("還記得 P2 的右欄嗎？這就是答案。", {
    x: 5.5, y: 5.1, w: 4.1, h: 0.4,
    fontFace: FONT, fontSize: 11, color: "AAAAAA", align: "right"
  });
}

// ============= P8 威爾基的賀電 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("服輸精神的真實樣子", {
    x: 0.5, y: 0.25, w: 9, h: 0.65,
    fontFace: FONT, fontSize: 28, bold: true, color: BLACK, align: "center"
  });
  const nodes = [
    { label: "威爾基落敗", sub: "選舉結果揭曉", accent: false },
    { label: "主動發賀電\n給羅斯福", sub: "主動恭賀對手", accent: false },
    { label: "協助進行\n外交活動", sub: "為國家服務", accent: false },
    { label: "一切以\n國家為前提", sub: "超越個人得失", accent: true }
  ];
  const nodeW = 1.9, nodeH = 1.4, gap = 0.55, startX = 0.5, nodeY = 1.9;
  for (let i = 0; i < nodes.length; i++) {
    const n = nodes[i];
    const x = startX + i * (nodeW + gap);
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: nodeY, w: nodeW, h: nodeH,
      fill: { color: n.accent ? "FFF3ED" : "F8F8F8" },
      line: { color: n.accent ? ORANGE : "DDDDDD", width: n.accent ? 2 : 1 }
    });
    s.addText(n.label, {
      x: x + 0.05, y: nodeY + 0.1, w: nodeW - 0.1, h: 0.75,
      fontFace: FONT, fontSize: 13, bold: true,
      color: n.accent ? ORANGE : BLACK, align: "center"
    });
    s.addText(n.sub, {
      x: x + 0.05, y: nodeY + 0.9, w: nodeW - 0.1, h: 0.4,
      fontFace: FONT, fontSize: 10, color: GRAY, align: "center"
    });
    if (i < 3) {
      s.addText("→", {
        x: x + nodeW, y: nodeY + 0.38, w: gap, h: 0.55,
        fontFace: FONT, fontSize: 18, color: ORANGE, align: "center", margin: 0
      });
    }
  }
  s.addText("「就像網球賽後，勝負雙方隔網握手的精神一樣。」", {
    x: 1.0, y: 4.55, w: 8.0, h: 0.65,
    fontFace: FONT, fontSize: 14, color: GRAY, align: "center", italic: true
  });
}

// ============= P9 風度三 超越勝敗的心胸 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("服輸是第一步，但更難的是——", {
    x: 0.5, y: 0.25, w: 9, h: 0.45,
    fontFace: FONT, fontSize: 14, color: GRAY, italic: true, align: "center"
  });
  s.addText("風度三｜超越勝敗的心胸", {
    x: 0.5, y: 0.72, w: 9, h: 0.65,
    fontFace: FONT, fontSize: 28, bold: true, color: BLACK, align: "center"
  });
  // 上區塊（灰化）
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.7, y: 1.55, w: 8.6, h: 1.0,
    fill: { color: "F0F0F0" }, line: { color: "CCCCCC", width: 1 }
  });
  s.addText([
    { text: "悻悻然的小人　", options: { bold: true, color: "AAAAAA" } },
    { text: "輸了就生悶氣，憤恨難平", options: { color: "BBBBBB" } }
  ], {
    x: 0.7, y: 1.55, w: 8.6, h: 1.0,
    fontFace: FONT, fontSize: 14, align: "center", valign: "middle"
  });
  // 下區塊（橘色框線）
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.7, y: 2.72, w: 8.6, h: 2.0,
    fill: { color: "FFF3ED" }, line: { color: ORANGE, width: 2 }
  });
  s.addText("得失無動於衷的運動家", {
    x: 0.7, y: 2.82, w: 8.6, h: 0.5,
    fontFace: FONT, fontSize: 15, bold: true, color: BLACK, align: "center"
  });
  s.addText("勝固欣然，敗亦可喜", {
    x: 0.7, y: 3.32, w: 8.6, h: 0.7,
    fontFace: FONT, fontSize: 32, bold: true, color: ORANGE, align: "center"
  });
  s.addText("重視運動精神本身，而非勝負結果", {
    x: 0.7, y: 4.08, w: 8.6, h: 0.45,
    fontFace: FONT, fontSize: 13, color: GRAY, align: "center"
  });
}

// ============= P10 貫徹始終 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("風度的靈魂｜貫徹始終", {
    x: 0.5, y: 0.2, w: 9, h: 0.65,
    fontFace: FONT, fontSize: 28, bold: true, color: BLACK, align: "center"
  });
  s.addText("對承諾負責，不因無望得獎就放棄", {
    x: 0.5, y: 0.9, w: 9, h: 0.4,
    fontFace: FONT, fontSize: 14, color: GRAY, align: "center"
  });
  s.addShape(pres.shapes.LINE, {
    x: 4.85, y: 1.45, w: 0, h: 2.7,
    line: { color: "EEEEEE", width: 1 }
  });
  s.addText("❌ 臨陣脫逃的樣子", {
    x: 0.4, y: 1.45, w: 4.2, h: 0.5,
    fontFace: FONT, fontSize: 14, bold: true, color: "CC0000", align: "center"
  });
  s.addText([
    { text: "• 賽跑落後，直接退場", options: { breakLine: true } },
    { text: "• 言而無信，半途而廢" }
  ], {
    x: 0.7, y: 2.1, w: 3.8, h: 1.0,
    fontFace: FONT, fontSize: 14, color: GRAY
  });
  s.addText("✅ 貫徹始終的樣子", {
    x: 5.1, y: 1.45, w: 4.4, h: 0.5,
    fontFace: FONT, fontSize: 14, bold: true, color: "007700", align: "center"
  });
  s.addText([
    { text: "• 賽跑落後，仍然跑完全程", options: { breakLine: true, color: ORANGE } },
    { text: "• 言必信，行必果", options: { color: ORANGE } }
  ], {
    x: 5.2, y: 2.1, w: 4.3, h: 1.0,
    fontFace: FONT, fontSize: 14
  });
  s.addText("「因為他對承諾負責，不因無望得獎就放棄。」", {
    x: 0.5, y: 4.35, w: 9, h: 0.7,
    fontFace: FONT, fontSize: 14, color: "333333", align: "center", italic: true
  });
}

// ============= P11 三大風度統整頁 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("運動家的三種風度", {
    x: 0.5, y: 0.2, w: 9, h: 0.65,
    fontFace: FONT, fontSize: 28, bold: true, color: BLACK, align: "center"
  });
  // 上方橫軸
  s.addShape(pres.shapes.LINE, {
    x: 0.7, y: 1.25, w: 8.6, h: 0,
    line: { color: ORANGE, width: 1.5 }
  });
  const axisItems = [
    { x: 0.6, text: "外在行為" },
    { x: 4.25, text: "內在心態" },
    { x: 7.9, text: "持久意志" }
  ];
  for (const a of axisItems) {
    s.addText(a.text, {
      x: a.x, y: 0.97, w: 1.5, h: 0.35,
      fontFace: FONT, fontSize: 11, color: ORANGE, bold: true, align: "center"
    });
  }
  // 三格
  const boxes = [
    { x: 0.5, title: "正大光明的態度", q: "你的競爭方式光明嗎？", accent: false },
    { x: 3.6, title: "服輸與超越勝敗", q: "你能接受結果嗎？", accent: false },
    { x: 6.7, title: "貫徹始終的毅力", q: "你能堅持到最後嗎？", accent: true }
  ];
  for (let i = 0; i < boxes.length; i++) {
    const b = boxes[i];
    s.addShape(pres.shapes.RECTANGLE, {
      x: b.x, y: 1.5, w: 2.8, h: 2.6,
      fill: { color: b.accent ? "FFF8F5" : "F8F8F8" },
      line: { color: b.accent ? ORANGE : "DDDDDD", width: b.accent ? 2 : 1 }
    });
    s.addText(b.title, {
      x: b.x + 0.1, y: 1.65, w: 2.6, h: 0.7,
      fontFace: FONT, fontSize: 14, bold: true, color: BLACK, align: "center"
    });
    s.addText(b.q, {
      x: b.x + 0.1, y: 2.6, w: 2.6, h: 0.8,
      fontFace: FONT, fontSize: 12, color: GRAY, align: "center"
    });
    if (i < 2) {
      s.addText("→", {
        x: b.x + 2.8, y: 2.45, w: 0.8, h: 0.5,
        fontFace: FONT, fontSize: 18, color: ORANGE, align: "center", margin: 0
      });
      s.addText("更深一層", {
        x: b.x + 2.75, y: 2.0, w: 0.9, h: 0.4,
        fontFace: FONT, fontSize: 9, color: GRAY, align: "center"
      });
    }
  }
}

// ============= P12 誤解矯正頁 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("有風度 ≠ 不想贏", {
    x: 0.5, y: 0.3, w: 9, h: 0.7,
    fontFace: FONT, fontSize: 28, bold: true, color: BLACK, align: "center"
  });
  s.addShape(pres.shapes.LINE, {
    x: 4.85, y: 1.2, w: 0, h: 3.0,
    line: { color: "EEEEEE", width: 1 }
  });
  s.addText("❌ 常見誤解", {
    x: 0.4, y: 1.2, w: 4.2, h: 0.5,
    fontFace: FONT, fontSize: 14, bold: true, color: "CC0000", align: "center"
  });
  s.addText("有風度的人會讓著對方，不認真比賽", {
    x: 0.5, y: 1.85, w: 4.0, h: 1.3,
    fontFace: FONT, fontSize: 14, color: "AAAAAA", align: "center"
  });
  s.addText("✅ 正確理解", {
    x: 5.1, y: 1.2, w: 4.4, h: 0.5,
    fontFace: FONT, fontSize: 14, bold: true, color: "007700", align: "center"
  });
  s.addText("全力競爭，但競爭的方式要光明正大", {
    x: 5.1, y: 1.85, w: 4.3, h: 1.0,
    fontFace: FONT, fontSize: 14, color: ORANGE, align: "center"
  });
  s.addText("「來競爭當然要求勝利，來比賽當然想創紀錄。——羅家倫」", {
    x: 4.9, y: 3.1, w: 4.7, h: 0.65,
    fontFace: FONT, fontSize: 11, color: GRAY, align: "center", italic: true
  });
}

// ============= P13 從運動場到人生場 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("「運動家的風度表現在人生上，是一個莊嚴公正、協調進取的人生。」", {
    x: 0.5, y: 0.15, w: 9, h: 0.55,
    fontFace: FONT, fontSize: 13, color: GRAY, align: "center", italic: true
  });
  s.addText("從運動場到人生場", {
    x: 0.5, y: 0.75, w: 9, h: 0.65,
    fontFace: FONT, fontSize: 28, bold: true, color: BLACK, align: "center"
  });
  s.addText("運動場上", {
    x: 0.4, y: 1.55, w: 3.7, h: 0.45,
    fontFace: FONT, fontSize: 14, bold: true, color: BLACK, align: "center"
  });
  s.addText("人生場上", {
    x: 5.9, y: 1.55, w: 3.7, h: 0.45,
    fontFace: FONT, fontSize: 14, bold: true, color: BLACK, align: "center"
  });
  const rows = [
    { left: "光明競爭", right: "做事不走捷徑" },
    { left: "服輸不怨", right: "失敗後反省自己" },
    { left: "貫徹始終", right: "對承諾負責到底" }
  ];
  for (let i = 0; i < rows.length; i++) {
    const r = rows[i];
    const y = 2.1 + i * 0.9;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.4, y, w: 3.7, h: 0.7,
      fill: { color: "F8F8F8" }, line: { color: "DDDDDD", width: 1 }
    });
    s.addText(r.left, {
      x: 0.4, y, w: 3.7, h: 0.7,
      fontFace: FONT, fontSize: 14, color: BLACK, align: "center", valign: "middle"
    });
    s.addText("↔", {
      x: 4.25, y, w: 1.5, h: 0.7,
      fontFace: FONT, fontSize: 20, color: ORANGE, align: "center", valign: "middle", margin: 0
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: 5.9, y, w: 3.7, h: 0.7,
      fill: { color: "FFF3ED" }, line: { color: ORANGE, width: 1 }
    });
    s.addText(r.right, {
      x: 5.9, y, w: 3.7, h: 0.7,
      fontFace: FONT, fontSize: 14, color: ORANGE, align: "center", valign: "middle"
    });
  }
}

// ============= P14 金句頁 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText([
    { text: "寧可有", options: { color: BLACK } },
    { text: "光明", options: { color: ORANGE } },
    { text: "的失敗，", options: { color: BLACK, breakLine: true } },
    { text: "絕不要", options: { color: BLACK } },
    { text: "不榮譽", options: { color: ORANGE } },
    { text: "的成功！", options: { color: BLACK } }
  ], {
    x: 0.8, y: 1.4, w: 8.4, h: 2.7,
    fontFace: FONT, fontSize: 36, bold: true, align: "center", valign: "middle"
  });
}

// ============= P15 延伸案例 難民代表隊 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("他們用行動證明了這句話", {
    x: 0.5, y: 0.2, w: 9, h: 0.65,
    fontFace: FONT, fontSize: 28, bold: true, color: BLACK, align: "center"
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.05, w: 9.0, h: 1.35,
    fill: { color: "F5F5F5" }, line: { color: "DDDDDD", width: 1 }
  });
  s.addText([
    { text: "馬蒂妮（Yusra Mardini）\n", options: { bold: true, breakLine: true } },
    { text: "17 歲逃離敘利亞，在引擎故障的橡皮艇上，於愛琴海游泳推船 3.5 小時，才得以抵達希臘。", options: { color: GRAY } }
  ], {
    x: 0.7, y: 1.1, w: 8.6, h: 1.25,
    fontFace: FONT, fontSize: 13, align: "center", valign: "middle", color: BLACK
  });
  const actions = [
    { label: "抵達德國後持續訓練，\n取得奧運資格", tag: "貫徹始終 ✓" },
    { label: "以難民身分\n站上奧運最高殿堂", tag: "正大光明 ✓" },
    { label: "成為聯合國難民署\n代表大使，繼續發聲", tag: "超越勝敗 ✓" }
  ];
  for (let i = 0; i < actions.length; i++) {
    const a = actions[i];
    const x = 0.4 + i * 3.15;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 2.6, w: 2.9, h: 1.2,
      fill: { color: "F8F8F8" }, line: { color: "DDDDDD", width: 1 }
    });
    s.addText(a.label, {
      x: x + 0.05, y: 2.65, w: 2.8, h: 0.85,
      fontFace: FONT, fontSize: 11, color: BLACK, align: "center"
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.35, y: 3.6, w: 2.2, h: 0.32,
      fill: { color: ORANGE }, line: { color: ORANGE }
    });
    s.addText(a.tag, {
      x: x + 0.35, y: 3.6, w: 2.2, h: 0.32,
      fontFace: FONT, fontSize: 10, color: WHITE, bold: true, align: "center", valign: "middle"
    });
  }
}

// ============= P16 行動召喚頁 =============
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("你在哪個場合，最需要這種風度？", {
    x: 0.5, y: 1.3, w: 9, h: 1.2,
    fontFace: FONT, fontSize: 28, bold: true, color: BLACK, align: "center", valign: "middle"
  });
  s.addText("考試失利　　社團競爭　　與人爭執", {
    x: 1.0, y: 2.75, w: 8.0, h: 0.6,
    fontFace: FONT, fontSize: 14, color: "888888", align: "center"
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 2.0, y: 3.8, w: 6.0, h: 0.85,
    fill: { color: WHITE }, line: { color: ORANGE, width: 1.5 }
  });
  s.addText("請在學習單上寫下：你的場合 ＋ 你會怎麼做。", {
    x: 2.0, y: 3.8, w: 6.0, h: 0.85,
    fontFace: FONT, fontSize: 13, color: BLACK, align: "center", valign: "middle"
  });
}

// 輸出
const outputPath = "C:/Users/北興/Desktop/claude-ai/運動家的風度_教學簡報.pptx";
pres.writeFile({ fileName: outputPath })
  .then(() => console.log("✅ 完成：" + outputPath))
  .catch(err => { console.error("❌", err); process.exit(1); });
