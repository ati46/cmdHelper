import os
import json

VIM_DATA = [
    { "action": "复制整行 (Copy Line)", "keywords": ["复制", "copy", "yank", "fuzi", "yy"], "command": "yy" },
    { "action": "复制选中部分 (Copy Selection)", "keywords": ["复制", "copy", "yank", "fuzi", "y"], "command": "y (在 Visual 模式下)" },
    { "action": "粘贴到光标后 (Paste After)", "keywords": ["粘贴", "paste", "zhantie", "p"], "command": "p" },
    { "action": "粘贴到光标前 (Paste Before)", "keywords": ["粘贴", "paste", "zhantie", "P"], "command": "P" },
    { "action": "复制选中内容到系统剪贴板 (Copy Selection to System Clipboard)", "keywords": ["复制", "系统剪贴板", "copy", "system", "clipboard", "plus", "register", "+", "y", "yank"], "command": "\"+y" },
    { "action": "复制当前行到系统剪贴板 (Copy Line to System Clipboard)", "keywords": ["复制", "整行", "系统剪贴板", "copy", "line", "system", "clipboard", "plus", "register", "+", "yy", "yank"], "command": "\"+yy" },
    { "action": "从系统剪贴板粘贴到光标后 (Paste from System Clipboard After)", "keywords": ["粘贴", "系统剪贴板", "paste", "system", "clipboard", "plus", "register", "+", "p"], "command": "\"+p" },
    { "action": "从系统剪贴板粘贴到光标前 (Paste from System Clipboard Before)", "keywords": ["粘贴", "系统剪贴板", "paste", "system", "clipboard", "plus", "register", "+", "P"], "command": "\"+P" },
    { "action": "设置默认使用系统剪贴板 (Set System Clipboard as Default)", "keywords": ["配置", "默认", "系统剪贴板", "unnamedplus", "clipboard", "vimrc", "set"], "command": "set clipboard=unnamedplus (在 ~/.vimrc 中添加)" },
    { "action": "可视模式下粘贴不覆盖默认寄存器 (Prevent Visual Paste Overwrite)", "keywords": ["可视模式", "粘贴", "覆盖", "不覆盖", "寄存器", "剪贴板", "visual", "paste", "overwrite", "xnoremap", "p"], "command": "xnoremap p \"_dP (在 ~/.vimrc 或 ~/.ideavimrc 中配置)" },
    { "action": "可视模式下连续粘贴最初复制的内容 (Visual Mode Paste Origin)", "keywords": ["可视模式", "连续粘贴", "复制内容", "粘贴", "visual", "paste", "origin", "0", "p"], "command": "ve\"0p (指定 0 号寄存器粘贴，多次粘贴时内容不被覆盖)" },
    { "action": "检查 Vim 是否支持系统剪贴板 (Check Clipboard Support)", "keywords": ["检查", "支持", "系统剪贴板", "version", "grep", "clipboard", "status"], "command": "vim --version | grep clipboard (需输出 +clipboard)" },
    { "action": "在命令行 / 或 : 状态下粘贴剪贴板/寄存器内容 (Paste in Command-line Mode)", "keywords": ["命令行", "粘贴", "搜索", "寄存器", "剪贴板", "paste", "command", "search", "ctrl", "r"], "command": "Ctrl + r 随后按 + (系统剪贴板) 或 \" (默认寄存器)" },
    { "action": "在命令行 / 或 : 状态下插入当前光标处的单词 (Insert Cursor Word to Command-line)", "keywords": ["插入单词", "光标词", "搜索词", "命令行", "cursor", "word", "insert", "ctrl", "r", "w"], "command": "Ctrl + r 随后按 Ctrl + w" },
    { "action": "启用粘贴模式防止缩进错乱 (Enable Paste Mode)", "keywords": ["粘贴模式", "缩进", "格式", "paste", "set", "indent", "format"], "command": ":set paste" },
    { "action": "Esc 回到 Normal 模式自动切回英文输入法 (Auto Switch Input Method on Esc)", "keywords": ["输入法", "自动切换", "英文", "中文", "fcitx", "esc", "normal", "input", "method", "ideavim"], "command": "在 ~/.vimrc, ~/.ideavimrc 或 VSCode/Cursor 中配置 fcitx 联动" },
    { "action": "关闭粘贴模式 (Disable Paste Mode)", "keywords": ["关闭粘贴", "nopaste", "set"], "command": ":set nopaste" },
    { "action": "快捷切换粘贴模式 (Toggle Paste Mode)", "keywords": ["切换粘贴", "toggle", "paste", "set"], "command": ":set paste!" },
    { "action": "设置快捷键一键切换粘贴模式 (Map Key to Toggle Paste)", "keywords": ["快捷键", "pastetoggle", "vimrc", "set", "f2"], "command": "set pastetoggle=<F2> (在 ~/.vimrc 中添加)" },
    { "action": "撤销上一步操作 (Undo)", "keywords": ["撤销", "undo", "chexiao", "u"], "command": "u" },
    { "action": "重做/反撤销上一步操作 (Redo)", "keywords": ["重做", "反撤销", "redo", "chongzuo", "fanchexiao", "ctrl", "r"], "command": "Ctrl + r" },
    { "action": "保存并退出 (Save and Quit)", "keywords": ["保存", "退出", "save", "quit", "wq", "x"], "command": ":wq 或 :x 或 ZZ" },
    { "action": "强制退出不保存 (Force Quit)", "keywords": ["退出", "quit", "q!"], "command": ":q!" },
    { "action": "删除当前行 (Delete Line)", "keywords": ["删除", "delete", "shanchu", "dd"], "command": "dd" },
    { "action": "删除到行尾 (Delete to End of Line)", "keywords": ["删除", "delete", "shanchu", "D"], "command": "D 或 d$" },
    { "action": "删除当前字符且不覆盖剪贴板 (Delete Char without overriding clipboard)", "keywords": ["删除", "delete", "shanchu", "x", "剪贴板", "黑洞", "寄存器"], "command": "x (需在 ~/.vimrc 配置 nnoremap x \"_x)" },
    { "action": "删除当前词 (Delete Word)", "keywords": ["删除", "词", "单词", "delete", "word", "diw"], "command": "diw (光标在词中任意位置)" },
    { "action": "删除并修改当前词 (Change Word)", "keywords": ["删除", "修改", "替换", "词", "单词", "change", "word", "ciw"], "command": "ciw (删除单词并进入插入模式)" },
    { "action": "从光标处删除并修改至词尾 (Change to End of Word)", "keywords": ["删除至词尾", "修改", "词尾", "change", "word", "end", "ce"], "command": "ce (从光标当前位置修改到单词结尾，并进入插入模式)" },
    { "action": "从光标处删除至词尾 (Delete to End of Word)", "keywords": ["删除至词尾", "词尾", "delete", "word", "end", "de"], "command": "de (从光标当前位置删除到单词结尾)" },
    { "action": "删除双引号内的内容 (Delete Inside Quotes)", "keywords": ["删除", "引号", "内容", "delete", "quotes", "di\""], "command": "di\" (也可用于单引号 di')" },
    { "action": "删除并修改双引号内的内容 (Change Inside Quotes)", "keywords": ["删除", "修改", "引号", "内容", "change", "quotes", "ci\""], "command": "ci\" (也可用于单引号 ci')" },
    { "action": "删除括号内的内容 (Delete Inside Brackets)", "keywords": ["删除", "括号", "内容", "delete", "brackets", "di(", "di[", "di{"], "command": "di( 或 di[ 或 di{ (删除对应括号内的内容)" },
    { "action": "删除并修改括号内的内容 (Change Inside Brackets)", "keywords": ["删除", "修改", "括号", "内容", "change", "brackets", "ci(", "ci[", "ci{"], "command": "ci( 或 ci[ 或 ci{ (删除内容并进入插入模式)" },
    { "action": "选中当前词 (Visual Select Word)", "keywords": ["选中", "选择", "词", "单词", "visual", "select", "word", "viw"], "command": "viw" },
    { "action": "选中引号或括号内的内容 (Visual Select Inside)", "keywords": ["选中", "选择", "引号", "括号", "内容", "visual", "select", "vi\"", "vi("], "command": "vi\" 或 vi( 等" },
    { "action": "进入行选择模式 (Visual Line Mode)", "keywords": ["选中", "选择", "行", "模式", "visual", "line", "V", "shift"], "command": "V (Shift + v)" },
    { "action": "进入块选择模式 (Visual Block Mode)", "keywords": ["选中", "选择", "块", "矩形", "模式", "visual", "block", "ctrl", "v"], "command": "Ctrl + v" },
    { "action": "跳到文件首行 (Go to First Line)", "keywords": ["跳转", "移动", "首行", "top", "first", "gg"], "command": "gg" },
    { "action": "跳到文件尾行 (Go to Last Line)", "keywords": ["跳转", "移动", "尾行", "bottom", "last", "G"], "command": "G" },
    { "action": "跳到行首 (Go to Line Start)", "keywords": ["跳转", "移动", "行首", "start", "^", "0"], "command": "^ (第一个非空白) 或 0 (绝对行首)" },
    { "action": "跳到行尾 (Go to Line End)", "keywords": ["跳转", "移动", "行尾", "end", "$"], "command": "$" },
    { "action": "查找 (Search)", "keywords": ["查找", "搜索", "search", "chazhao", "/"], "command": "/pattern (向下) 或 ?pattern (向上)" },
    { "action": "查找下一个 (Next Match)", "keywords": ["查找", "下一个", "next", "n"], "command": "n" },
    { "action": "查找上一个 (Previous Match)", "keywords": ["查找", "上一个", "prev", "N"], "command": "N" },
    { "action": "替换当前行 (Replace in Line)", "keywords": ["替换", "replace", "tihuan", "s"], "command": ":s/old/new/g" },
    { "action": "全局替换 (Replace Globally)", "keywords": ["替换", "全局", "replace", "global", "s"], "command": ":%s/old/new/g" },
    { "action": "交互式全局替换 (Interactive Global Replace)", "keywords": ["替换", "全局", "交互", "确认", "replace", "global", "interactive", "confirm", "s", "c"], "command": ":%s/old/new/gc" },
    { "action": "替换选中区域 (Replace in Visual Selection)", "keywords": ["替换", "选中", "区域", "visual", "selection", "replace", "s"], "command": ":'<,'>s/old/new/g (在 Visual 模式选中后按 :)" },
    { "action": "指定行范围替换 (Replace in Line Range)", "keywords": ["替换", "范围", "指定行", "range", "line", "replace", "s"], "command": ":10,20s/old/new/g (替换第10到20行)" },
    { "action": "多文件批量替换 (Batch Replace in Multiple Files)", "keywords": ["替换", "批量", "多文件", "批量替换", "batch", "multiple", "files", "argdo", "replace", "s"], "command": ":argdo %s/old/new/gc | update (需先 :args *.txt 加载文件)" },
    { "action": "进入插入模式 (Insert Mode)", "keywords": ["插入", "编辑", "insert", "i", "a", "o"], "command": "i (光标前), a (光标后), o (下一行)" },
    { "action": "在行首进入插入模式 (Insert at Line Start)", "keywords": ["插入", "编辑", "行首", "insert", "start", "I", "shift"], "command": "I (Shift + i)" },
    { "action": "在行尾进入插入模式 (Insert at Line End)", "keywords": ["插入", "编辑", "行尾", "insert", "end", "A", "shift"], "command": "A (Shift + a)" },
    { "action": "在当前行上方新起一行并插入 (Insert New Line Above)", "keywords": ["插入", "编辑", "上方", "新增", "insert", "above", "O", "shift"], "command": "O (Shift + o)" },
    { "action": "删除当前字符并插入 (Substitute Character)", "keywords": ["删除", "插入", "修改", "字符", "substitute", "s"], "command": "s" },
    { "action": "删除当前行并插入 (Substitute Line)", "keywords": ["删除", "插入", "修改", "行", "整行", "substitute", "line", "S", "cc"], "command": "S (Shift + s) 或 cc" },
    { "action": "跳转到指定行 (Go to Line N)", "keywords": ["跳转", "移动", "指定行", "line", "go", "G", ":"], "command": ":<N> 或 <N>G (例 :10 或 10G)" },
    { "action": "按单词左右移动光标 (Move by Word)", "keywords": ["跳转", "移动", "光标", "单词", "word", "w", "b", "e"], "command": "w (下个词首) / b (上个词首) / e (下个词尾)" },
    { "action": "向后查找本行内指定字符 (Find Next Char)", "keywords": ["跳转", "查找", "行内", "字符", "向后", "find", "f", "char"], "command": "f<字符> (例如 fL 找到下一个 L)" },
    { "action": "向前查找本行内指定字符 (Find Prev Char)", "keywords": ["跳转", "查找", "行内", "字符", "向前", "find", "F", "char"], "command": "F<字符> (例如 FL 找到前一个 L)" },
    { "action": "向后跳转到本行内指定字符的前一个位置 (Till Next Char)", "keywords": ["跳转", "定位", "行内", "字符前", "till", "t", "char"], "command": "t<字符> (例如 tL 跳到下一个 L 的前一格)" },
    { "action": "向前跳转到本行内指定字符的后一个位置 (Till Prev Char)", "keywords": ["跳转", "定位", "行内", "字符后", "till", "T", "char"], "command": "T<字符> (例如 TL 跳到前一个 L 的后一格)" },
    { "action": "重复上一次的行内字符查找 (Repeat Char Search Forward)", "keywords": ["重复", "查找", "行内", "下一个", "repeat", "next", ";"], "command": ";" },
    { "action": "反向重复上一次的行内字符查找 (Repeat Char Search Backward)", "keywords": ["反向重复", "查找", "行内", "上一个", "repeat", "prev", ","], "command": "," },
    { "action": "跳转到匹配的成对括号 (Jump to Matching Bracket)", "keywords": ["跳转", "定位", "括号", "匹配", "bracket", "parenthesis", "%"], "command": "% (在 ( ) [ ] { } 上使用)" },
    { "action": "历史跳转位置前后穿梭 (Jump List Navigation)", "keywords": ["跳转", "定位", "历史", "回退", "前进", "jump", "history", "ctrl", "o", "i"], "command": "Ctrl + o (回退到上个位置) / Ctrl + i (前进到下个位置)" },
    { "action": "屏幕区域快速跳转 (Jump to Screen Area)", "keywords": ["跳转", "移动", "屏幕", "顶部", "中间", "底部", "screen", "high", "middle", "low", "H", "M", "L"], "command": "H (屏幕首行) / M (屏幕中间行) / L (屏幕尾行)" },
    { "action": "居中当前光标所在行 (Center Screen on Cursor)", "keywords": ["居中", "屏幕", "中间", "滚动", "center", "screen", "zz"], "command": "zz" },
    { "action": "快速查找/高亮当前光标下的单词 (Find Word Under Cursor)", "keywords": ["查找", "搜索", "定位", "单词", "高亮", "word", "cursor", "*", "#"], "command": "* (向下搜索当前词) / # (向上搜索当前词)" },
    { "action": "跳转到局部变量/函数定义处 (Go to Local Definition)", "keywords": ["跳转", "定义", "变量", "函数", "definition", "local", "gd"], "command": "gd" },
    { "action": "一键开关右侧文件树 (Toggle Right-Side File Tree)", "keywords": ["文件树", "目录", "右侧", "tree", "toggle", "netrw", "leader", "e", "空格", "快捷键"], "command": "空格 + e (或 :call ToggleRightNetrw())" },
    { "action": "一键开关 Markdown 浏览器实时预览 (Toggle Markdown Preview)", "keywords": ["markdown", "预览", "浏览器", "preview", "toggle", "leader", "m", "空格", "快捷键"], "command": "空格 + m (或 :MarkdownPreviewToggle)" },
    { "action": "处于文件树模式时在目录和编辑器之间切换焦点 (Switch focus between file tree and editor)", "keywords": ["文件树", "目录树", "切换", "焦点", "窗口", "编辑器", "switch", "focus", "tree", "netrw", "ctrl", "h", "l"], "command": "Ctrl + h (跳回左侧编辑器) / Ctrl + l (跳向右侧文件树)" },
    { "action": "在文件树中选中并打开文件到编辑器 (Open file from tree to editor)", "keywords": ["文件树", "目录树", "打开文件", "打开", "回车", "netrw", "open", "file", "enter"], "command": "Enter (光标停在文件名上按回车)" },
    { "action": "文件树中误操作导致编辑器被目录覆盖时退回原文件 (Rollback from covered window in netrw)", "keywords": ["退回", "误按", "覆盖", "回退", "目录树", "文件树", "netrw", "rollback", "ctrl", "o"], "command": "Ctrl + o" },
    { "action": "在所有打开的窗口/分屏间循环切换焦点 (Cycle Window Focus)", "keywords": ["窗口切换", "循环切换", "焦点", "cycle", "focus", "window", "ctrl", "w"], "command": "Ctrl + w + w (双击 Ctrl+w)" },
    { "action": "向指定方向的窗口/分屏移动焦点 (Navigate Windows HJKL)", "keywords": ["窗口切换", "焦点", "方向", "navigate", "window", "h", "j", "k", "l", "ctrl", "w"], "command": "Ctrl + w + h/j/k/l (例如 Ctrl + w + h 移动到左边窗口)" },
    { "action": "水平拆分当前窗口 (Horizontal Split)", "keywords": ["水平分屏", "拆分窗口", "横向", "horizontal", "split", "ctrl", "w", "s"], "command": "Ctrl + w + s (或 :sp)" },
    { "action": "垂直拆分当前窗口 (Vertical Split)", "keywords": ["垂直分屏", "拆分窗口", "纵向", "vertical", "split", "ctrl", "w", "v"], "command": "Ctrl + w + v (或 :vsp)" },
    { "action": "仅保留当前窗口并关闭其他所有分屏 (Keep Only Current Window)", "keywords": ["关闭其他", "最大化", "独占窗口", "only", "close", "others", "ctrl", "w", "o"], "command": "Ctrl + w + o (或 :only)" },
    { "action": "关闭当前窗口/分屏 (Close Current Window)", "keywords": ["关闭窗口", "分屏关闭", "退出", "close", "window", "ctrl", "w", "c"], "command": "Ctrl + w + c (或 :q)" },
    { "action": "文件树模式下隐藏/显示以点开头的隐藏文件 (Toggle Hidden Files in Netrw)", "keywords": ["隐藏文件", "显示隐藏", "点文件", "netrw", "hide", "show", "dotfiles", "gh"], "command": "gh" },
    { "action": "循环切换文件树的列表显示风格 (Cycle List Styles in Netrw)", "keywords": ["显示风格", "列表排版", "视图", "netrw", "style", "list", "i"], "command": "i (在 thin/long/wide/tree 视图之间切换)" },
    { "action": "在文件树中新建文件 (Create New File in Netrw)", "keywords": ["新建文件", "创建文件", "netrw", "new", "create", "file", "%"], "command": "% (输入文件名后回车)" },
    { "action": "在文件树中新建文件夹/目录 (Create New Directory in Netrw)", "keywords": ["新建文件夹", "创建目录", "netrw", "new", "create", "directory", "dir", "d"], "command": "d (输入目录名后回车)" },
    { "action": "在文件树中重命名选中的文件或目录 (Rename File/Dir in Netrw)", "keywords": ["重命名", "修改名称", "改名", "netrw", "rename", "R"], "command": "R (输入新名字后回车)" },
    { "action": "在文件树中删除选中的文件或目录 (Delete File/Dir in Netrw)", "keywords": ["删除文件", "清理", "netrw", "delete", "D"], "command": "D (需要输入 y 确认)" },
    { "action": "极速保存当前文件 (Quick Save File)", "keywords": ["保存", "写入", "save", "write", "leader", "w", "空格", "快捷键"], "command": "空格 + w (或 :w)" },
    { "action": "极速退出当前窗口 (Quick Quit Window)", "keywords": ["退出", "关闭", "quit", "close", "leader", "q", "空格", "快捷键"], "command": "空格 + q (或 :q)" },
    { "action": "消除当前搜索高亮 (Clear Search Highlight)", "keywords": ["消除", "高亮", "清除", "search", "highlight", "clear", "noh", "esc", "快捷键"], "command": "Esc 键 (配置后单击即可清除高亮)" },
    { "action": "折行逻辑纵向移动 (Move Cursor by Screen Line on Wrap)", "keywords": ["折行", "移动", "光标", "wrap", "move", "j", "k", "gj", "gk", "快捷键"], "command": "j 或 k (已映射为 gj / gk，按屏幕视觉行移动)" },
    { "action": "重复上一次的修改操作 (Repeat Last Change)", "keywords": ["重复", "修改", "操作", "上次", "repeat", "change", "."], "command": "." },
    { "action": "向右缩进当前行 (Indent Line)", "keywords": ["缩进", "排版", "右移", "indent", ">"], "command": ">>" },
    { "action": "向左取消缩进当前行 (Unindent Line)", "keywords": ["取消缩进", "排版", "左移", "unindent", "<"], "command": "<<" },
    { "action": "大范围/多行缩进或取消缩进 (Large Scale Indentation)", "keywords": ["大范围", "多行", "缩进", "排版", "左右移动", "indent", "visual", ">", "<"], "command": "V (选定区域) -> 按 > (右移) 或 < (左移)" },
    { "action": "自动对齐/格式化整个文件 (Auto Format Entire File)", "keywords": ["自动对齐", "格式化", "排版", "整篇", "全部", "format", "autoalign", "gg", "=", "G"], "command": "gg=G (跳到文件头并自动缩进对齐到文件尾)" },
    { "action": "自动对齐选定区域或代码块 (Auto Format Block/Selection)", "keywords": ["对齐", "格式化", "区域", "花括号", "块", "align", "format", "block", "=", "i", "{"], "command": "V (选定区域) -> = (或 =i{ 自动对齐当前 {} 块内代码)" },
    { "action": "指定行范围缩进 (Indent Line Range)", "keywords": ["指定行", "范围", "缩进", "排版", "range", "line", "indent", ">", ":"], "command": ":10,20> (第10到20行向右缩进) 或 :10,20< (向左)" },
    { "action": "翻转当前字符的大小写 (Toggle Case)", "keywords": ["大小写", "转换", "翻转", "case", "toggle", "~"], "command": "~" },
    { "action": "将当前行全部转为小写 (Lowercase Line)", "keywords": ["小写", "转换", "行", "lowercase", "guu"], "command": "guu" },
    { "action": "将当前行全部转为大写 (Uppercase Line)", "keywords": ["大写", "转换", "行", "uppercase", "gUU"], "command": "gUU" },
    { "action": "快速向上跳转 N 行 (Jump up N lines)", "keywords": ["跳转", "移动", "上", "k", "行", "up", "lines", "11k"], "command": "<N>k (例如 11k 向上跳11行)" },
    { "action": "快速向下跳转 N 行 (Jump down N lines)", "keywords": ["跳转", "移动", "下", "j", "行", "down", "lines", "11j"], "command": "<N>j (例如 11j 向下跳11行)" },
    { "action": "快速向左跳转 N 个字符 (Jump left N chars)", "keywords": ["跳转", "移动", "左", "h", "字符", "left", "chars"], "command": "<N>h (例如 5h 向左跳5格)" },
    { "action": "快速向右跳转 N 个字符 (Jump right N chars)", "keywords": ["跳转", "移动", "右", "l", "字符", "right", "chars"], "command": "<N>l (例如 5l 向右跳5格)" },
    { "action": "向下翻页/滚动半页 (Scroll Down Page/Half-page)", "keywords": ["翻页", "向下", "半页", "整页", "滚动", "scroll", "down", "ctrl", "f", "d"], "command": "Ctrl + f (向下翻整页) 或 Ctrl + d (向下翻半页)" },
    { "action": "向上翻页/滚动半页 (Scroll Up Page/Half-page)", "keywords": ["翻页", "向上", "半页", "整页", "滚动", "scroll", "up", "ctrl", "b", "u"], "command": "Ctrl + b (向上翻整页) 或 Ctrl + u (向上翻半页)" },
    { "action": "逐行滚动屏幕而不移动光标 (Scroll Line-by-line)", "keywords": ["逐行", "屏幕滚动", "光标固定", "scroll", "line", "ctrl", "e", "y"], "command": "Ctrl + e (屏幕向下滚动一行) 或 Ctrl + y (屏幕向上滚动一行)" },
    { "action": "将当前行滚动至屏幕顶部/中部/底部 (Scroll Screen to Line Position)", "keywords": ["屏幕定位", "居中", "置顶", "置底", "scroll", "position", "zt", "zz", "zb"], "command": "zt (将当前行置顶) 或 zz (将当前行居中) 或 zb (将当前行置底)" },
    { "action": "进入列/矩形块选择模式 (Enter Visual Block Mode)", "keywords": ["列选择", "块选择", "矩形", "visual", "block", "ctrl", "v"], "command": "Ctrl + v" },
    { "action": "选中驼峰或蛇形变量的子单词部分 (Select Sub-word in CamelCase/snake_case)", "keywords": ["驼峰", "蛇形", "下划线", "子单词", "大写字母", "选择词", "camelcase", "snake", "subword", "b", "t", "v"], "command": "b (跳至子词首) -> vt<大写字母或下划线> (如 vtP 选中 validate)" },
    { "action": "矩形区域首部批量插入相同文字 (Column/Block Insert)", "keywords": ["批量插入", "首部", "插入", "insert", "visual", "block", "I", "shift", "esc"], "command": "Ctrl+v (选定区域) -> Shift+i (大写 I) -> 输入文字 -> Esc (双击/按一次 Esc 稍等即批量应用)" },
    { "action": "矩形区域尾部批量追加相同文字 (Column/Block Append)", "keywords": ["批量追加", "尾部", "追加", "append", "visual", "block", "A", "shift", "esc"], "command": "Ctrl+v (选定区域) -> Shift+a (大写 A) -> 输入文字 -> Esc (双击/按一次 Esc 稍等即批量应用)" },
    { "action": "矩形区域批量删除 (Column/Block Delete)", "keywords": ["批量删除", "删除", "delete", "visual", "block", "d", "x"], "command": "Ctrl+v (选定区域) -> 按 d 或 x" },
    { "action": "矩形区域批量替换为相同单字符 (Column/Block Replace Single Char)", "keywords": ["批量替换", "单字符", "替换", "replace", "visual", "block", "r"], "command": "Ctrl+v (选定区域) -> 按 r -> 输入要替换的单个字符" },
    { "action": "矩形区域批量改写为新字符串 (Column/Block Change)", "keywords": ["批量改写", "替换", "改写", "change", "visual", "block", "c", "esc"], "command": "Ctrl+v (选定区域) -> 按 c (原内容被删并进入插入模式) -> 输入新字符串 -> Esc (稍等即批量应用)" }
]

CURL_DATA = [
    { "action": "发送 GET 请求 (GET Request)", "keywords": ["get", "请求", "request", "fetch"], "command": "curl http://example.com" },
    { "action": "发送 POST 请求 (POST Request)", "keywords": ["post", "请求", "request", "data", "d", "X"], "command": "curl -X POST -d 'data' http://example.com" },
    { "action": "发送 JSON 数据 (POST JSON)", "keywords": ["post", "json", "请求", "header", "H"], "command": "curl -X POST -H 'Content-Type: application/json' -d '{\"key\":\"val\"}' http://example.com" },
    { "action": "保存输出到文件 (Save to File)", "keywords": ["保存", "下载", "save", "download", "output", "o"], "command": "curl -o filename.html http://example.com" },
    { "action": "跟随重定向 (Follow Redirects)", "keywords": ["重定向", "跟随", "redirect", "follow", "L"], "command": "curl -L http://example.com" },
    { "action": "显示响应头 (Show Headers)", "keywords": ["头信息", "响应头", "header", "head", "I", "i"], "command": "curl -I http://example.com (仅头) 或 curl -i http://example.com (包含主体)" },
    { "action": "忽略证书验证 (Insecure/Skip Cert Check)", "keywords": ["证书", "忽略", "安全", "insecure", "cert", "k"], "command": "curl -k https://example.com" },
    { "action": "上传文件 (Upload File)", "keywords": ["上传", "文件", "upload", "file", "F", "form"], "command": "curl -F 'file=@path/to/file' http://example.com/upload" },
    { "action": "传递 Cookie (Send Cookie)", "keywords": ["cookie", "传递", "send", "b"], "command": "curl -b 'name=value' http://example.com" }
]

AWK_DATA = [
    { "action": "打印整行 (Print Line)", "keywords": ["打印", "输出", "print", "line", "0"], "command": "awk '{print $0}' file" },
    { "action": "打印指定列 (Print Specific Columns)", "keywords": ["打印", "输出", "列", "print", "column"], "command": "awk '{print $1, $3}' file" },
    { "action": "按分隔符切分 (Specify Delimiter)", "keywords": ["分隔符", "切分", "delimiter", "split", "F"], "command": "awk -F',' '{print $1}' file" },
    { "action": "带条件的打印 (Conditional Print)", "keywords": ["条件", "过滤", "if", "condition", "filter"], "command": "awk '$1 > 100 {print $0}' file" },
    { "action": "计算列总和 (Sum Column)", "keywords": ["计算", "总和", "累加", "sum", "calc"], "command": "awk '{sum += $1} END {print sum}' file" },
    { "action": "匹配正则模式 (Regex Match)", "keywords": ["正则", "匹配", "regex", "match", "pattern"], "command": "awk '/pattern/ {print $0}' file" },
    { "action": "打印行号 (Print Line Number)", "keywords": ["行号", "行数", "NR", "number"], "command": "awk '{print NR, $0}' file" },
    { "action": "提取并过滤进程 PID (Find Process PID via ps & grep)", "keywords": ["进程", "获取PID", "pid", "ps", "grep", "awk", "过滤自身"], "command": "ps -ef | grep 'process_name' | grep -v grep | awk '{print $2}'" },
    { "action": "分析日志统计 IP 或状态码频次并降序排序 (Log Frequency Count)", "keywords": ["日志", "统计", "频次", "词频", "排行", "ip", "sort", "uniq", "awk"], "command": "awk '{print $1}' access.log | sort | uniq -c | sort -nr" },
    { "action": "获取根分区磁盘使用率百分比 (Get Root Disk Usage %)", "keywords": ["磁盘", "根目录", "使用率", "空间", "df", "grep", "awk"], "command": "df -h | grep '/$' | awk '{print $5}'" },
    { "action": "提取最常使用的历史命令 Top 10 (History Command Top 10)", "keywords": ["历史命令", "常用", "排行", "history", "awk", "sort", "uniq", "head"], "command": "history | awk '{print $2}' | sort | uniq -c | sort -rn | head -n 10" }
]

GREP_DATA = [
    { "action": "查找包含字符串的行 (Search String)", "keywords": ["查找", "搜索", "search", "find"], "command": "grep 'pattern' file" },
    { "action": "忽略大小写 (Ignore Case)", "keywords": ["大小写", "忽略", "case", "ignore", "i"], "command": "grep -i 'pattern' file" },
    { "action": "递归搜索目录 (Recursive Search)", "keywords": ["递归", "目录", "recursive", "dir", "r"], "command": "grep -r 'pattern' /path/to/dir" },
    { "action": "反向匹配/排除 (Invert Match)", "keywords": ["排除", "反向", "invert", "exclude", "v"], "command": "grep -v 'pattern' file" },
    { "action": "显示行号 (Show Line Number)", "keywords": ["行号", "number", "line", "n"], "command": "grep -n 'pattern' file" },
    { "action": "仅显示匹配的文件名 (List Files Only)", "keywords": ["文件名", "list", "file", "l"], "command": "grep -l 'pattern' *" },
    { "action": "精确匹配整词 (Match Whole Word)", "keywords": ["全词", "精确", "word", "exact", "w"], "command": "grep -w 'word' file" },
    { "action": "显示匹配行的前后几行 (Show Context)", "keywords": ["上下文", "前后", "context", "A", "B", "C"], "command": "grep -C 3 'pattern' file (前后各3行)" },
    { "action": "配合 find 与 xargs 批量搜索文件内容 (Search in Found Files)", "keywords": ["批量", "查找内容", "后缀", "find", "xargs", "grep"], "command": "find . -type f -name '*.py' | xargs grep 'pattern'" },
    { "action": "配合 tail 实时过滤日志中的关键字 (Realtime Filter Log)", "keywords": ["实时", "过滤", "监控", "日志", "tail", "grep", "error"], "command": "tail -f app.log | grep --line-buffered 'ERROR'" },
    { "action": "配合 ls 过滤特定文件类型/文件名后缀 (Filter Files with ls)", "keywords": ["过滤文件", "匹配", "后缀", "ls", "grep", "sh"], "command": "ls -l | grep '\\.sh$'" }
]

TAIL_DATA = [
    { "action": "查看文件末尾默认10行 (View End of File)", "keywords": ["末尾", "查看", "end", "view"], "command": "tail file" },
    { "action": "实时滚动追踪新数据 (Follow Output)", "keywords": ["实时", "滚动", "监控", "追踪", "follow", "f"], "command": "tail -f file" },
    { "action": "查看末尾指定的行数 (Specific Number of Lines)", "keywords": ["行数", "指定", "最后几行", "lines", "n"], "command": "tail -n 20 file" },
    { "action": "输出最后 20 行并持续滚动追踪新日志 (Show Last N Lines and Follow)", "keywords": ["最后20行", "滚动", "追踪", "实时", "日志", "n", "f", "follow"], "command": "tail -n 20 -f file" },
    { "action": "以文件名追踪日志，且在日志轮转/重建后自动重连 (Follow by Name & Retry - Log Rotation)", "keywords": ["日志轮转", "重连", "轮替", "重建", "logrotate", "retry", "F"], "command": "tail -F file.log" },
    { "action": "同时监控多个日志文件，在新数据产生时标明文件名 (Follow Multiple Files with Headers)", "keywords": ["多文件", "多日志", "同时监控", "文件名", "multiple", "headers", "f"], "command": "tail -f file1.log file2.log" },
    { "action": "滚动查看日志并仅高亮/过滤特定的错误级别 (Follow Log and Filter Level)", "keywords": ["过滤错误", "高亮", "实时过滤", "级别", "grep", "error", "warn"], "command": "tail -f app.log | grep -iE 'error|warn|fail'" }
]

LS_DATA = [
    { "action": "列出当前目录下的文件和目录 (List Files)", "keywords": ["列出", "文件", "目录", "ls", "list", "show"], "command": "ls" },
    { "action": "以详细列表格式显示 (Long Format)", "keywords": ["详细", "列表", "权限", "大小", "时间", "long", "detail", "l"], "command": "ls -l" },
    { "action": "显示所有文件，包括隐藏文件 (Show All Including Hidden)", "keywords": ["所有", "隐藏", "点文件", "hidden", "all", "a"], "command": "ls -a" },
    { "action": "易读格式显示文件大小 (Human Readable Size)", "keywords": ["易读", "文件大小", "单位", "human", "size", "h"], "command": "ls -lh" },
    { "action": "以 MB (兆字节) 为单位强制显示文件大小 (Show Size in MB)", "keywords": ["兆字节", "文件大小", "单位", "mb", "megabytes", "block-size"], "command": "ls -l --block-size=M" },
    { "action": "以 KB/GB 为单位强制显示文件大小 (Show Size in KB/GB)", "keywords": ["千字节", "吉字节", "文件大小", "单位", "kb", "gb", "block-size"], "command": "ls -l --block-size=K 或 ls -l --block-size=G" },
    { "action": "列出文件并显示 inode 索引节点号 (Show Inode Numbers)", "keywords": ["索引节点", "系统信息", "inode", "i"], "command": "ls -i" },
    { "action": "以数字形式显示所有者和组 ID (Show Numeric UID/GID)", "keywords": ["数字ID", "用户组", "权限", "numeric", "uid", "gid", "n"], "command": "ls -ln" },
    { "action": "显示超高精度的完整时间戳 (Show Full Precise Timestamp)", "keywords": ["高精度", "完整时间", "秒", "纳秒", "timestamp", "full-time"], "command": "ls -l --full-time" },
    { "action": "用双引号括起文件名 (Quote Filenames with Double Quotes)", "keywords": ["引号", "双引号", "空格文件名", "quote", "Q"], "command": "ls -Q" },
    { "action": "仅列出当前目录下的子目录本身 (List Directories Only)", "keywords": ["仅目录", "过滤目录", "只看目录", "directories only", "d"], "command": "ls -d */" },
    { "action": "按修改时间排序，最新在最前 (Sort by Time)", "keywords": ["排序", "时间", "最新", "sort", "time", "t"], "command": "ls -lt" },
    { "action": "按修改时间反向排序，最新在最后 (Sort by Time Reverse)", "keywords": ["排序", "时间", "反向", "最新", "reverse", "time", "tr"], "command": "ls -ltr" },
    { "action": "按文件大小排序，最大在最前 (Sort by Size)", "keywords": ["排序", "大小", "最大", "sort", "size", "S"], "command": "ls -lS" },
    { "action": "递归列出所有子目录内容 (Recursive List)", "keywords": ["递归", "子目录", "所有", "recursive", "R"], "command": "ls -R" },
    { "action": "仅显示指定目录自身信息而非其内容 (Show Directory Details)", "keywords": ["目录自身", "信息", "属性", "directory", "d"], "command": "ls -ld /path/to/dir" },
    { "action": "在输出中给不同类型文件着色 (Colorized Output)", "keywords": ["颜色", "着色", "区分", "color"], "command": "ls --color=auto" },
    { "action": "给条目添加类型标识符 (Classify Entries)", "keywords": ["分类", "标识符", "类型", "classify", "F"], "command": "ls -F" }
]

IDEA_DATA = [
    { "action": "随处搜索 (Search Everywhere)", "keywords": ["搜索", "全局", "文件", "类", "search", "everywhere", "shift", "shuangji"], "command": "Double Shift (双击 Shift)" },
    { "action": "查找动作/命令 (Find Action)", "keywords": ["查找", "动作", "命令", "action", "find", "a"], "command": "Ctrl + Shift + A" },
    { "action": "生成代码 (Generate Code - 构造函数/Getter/Setter)", "keywords": ["生成", "代码", "构造", "generate", "code", "insert", "alt"], "command": "Alt + Insert" },
    { "action": "查找类 (Go to Class)", "keywords": ["查找", "类", "跳转", "class", "n"], "command": "Ctrl + N" },
    { "action": "查找文件 (Go to File)", "keywords": ["查找", "文件", "跳转", "file", "shift", "n"], "command": "Ctrl + Shift + N" },
    { "action": "最近打开的文件 (Recent Files)", "keywords": ["最近", "文件", "历史", "recent", "e"], "command": "Ctrl + E" },
    { "action": "格式化代码 (Reformat Code)", "keywords": ["格式化", "排版", "代码", "format", "reformat", "l"], "command": "Ctrl + Alt + L" },
    { "action": "优化导入 (Optimize Imports)", "keywords": ["优化", "导入", "包", "import", "optimize", "o"], "command": "Ctrl + Alt + O" },
    { "action": "重命名 (Rename)", "keywords": ["重命名", "修改", "名字", "rename", "f6", "shift"], "command": "Shift + F6" },
    { "action": "复制当前行 (Duplicate Line)", "keywords": ["复制", "整行", "duplicate", "line", "d"], "command": "Ctrl + D" },
    { "action": "删除当前行 (Delete Line)", "keywords": ["删除", "整行", "delete", "line", "y"], "command": "Ctrl + Y" },
    { "action": "单行注释/取消注释 (Toggle Line Comment)", "keywords": ["注释", "单行", "comment", "line", "/"], "command": "Ctrl + /" },
    { "action": "多行块注释/取消注释 (Toggle Block Comment)", "keywords": ["注释", "多行", "块", "comment", "block", "shift", "/"], "command": "Ctrl + Shift + /" },
    { "action": "基本代码补全 (Basic Code Completion)", "keywords": ["补全", "提示", "代码", "complete", "space"], "command": "Ctrl + Space" },
    { "action": "智能代码补全 (Smart Code Completion)", "keywords": ["智能", "补全", "提示", "smart", "shift", "space"], "command": "Ctrl + Shift + Space" },
    { "action": "显示意图动作/快速修复 (Show Intention Actions / Quick Fix)", "keywords": ["修复", "意图", "建议", "fix", "intention", "alt", "enter"], "command": "Alt + Enter" },
    { "action": "跳转到声明/定义处 (Go to Declaration)", "keywords": ["跳转", "声明", "定义", "declaration", "definition", "b"], "command": "Ctrl + B 或 Ctrl + Click" },
    { "action": "查找引用 (Find Usages)", "keywords": ["查找", "引用", "使用", "usages", "find", "alt", "f7"], "command": "Alt + F7" },
    { "action": "显示引用 (Show Usages)", "keywords": ["显示", "引用", "使用", "usages", "show", "ctrl", "alt", "f7"], "command": "Ctrl + Alt + F7" }
]

GIT_DATA = [
    { "action": "克隆远程仓库 (Clone Repository)", "keywords": ["克隆", "下载", "clone", "git", "remote"], "command": "git clone <url>" },
    { "action": "初始化本地仓库 (Initialize Git Repo)", "keywords": ["初始化", "创建", "init", "git", "local"], "command": "git init" },
    { "action": "配置全局用户名 (Set Global Username)", "keywords": ["配置", "用户名", "config", "global", "user", "name"], "command": "git config --global user.name \"<name>\"" },
    { "action": "配置全局邮箱 (Set Global Email)", "keywords": ["配置", "邮箱", "config", "global", "email"], "command": "git config --global user.email \"<email>\"" },
    { "action": "查看工作区和暂存区状态 (Check Status)", "keywords": ["状态", "查看", "status", "git", "working"], "command": "git status" },
    { "action": "添加指定文件到暂存区 (Add File)", "keywords": ["添加", "暂存区", "add", "stage", "file"], "command": "git add <file>" },
    { "action": "添加所有修改到暂存区 (Add All Files)", "keywords": ["添加", "所有", "暂存区", "add", "all", "stage", "."], "command": "git add ." },
    { "action": "提交暂存区到仓库 (Commit Changes)", "keywords": ["提交", "保存", "commit", "message", "m"], "command": "git commit -m \"<message>\"" },
    { "action": "修改最后一次提交信息 (Amend Last Commit)", "keywords": ["修改", "最近一次", "提交信息", "amend", "commit", "message"], "command": "git commit --amend -m \"<new_message>\"" },
    { "action": "查看详细提交历史 (View Detailed History)", "keywords": ["历史", "日志", "log", "history", "commit"], "command": "git log" },
    { "action": "查看精简单行提交历史 (View Oneline History)", "keywords": ["历史", "单行", "精简", "log", "oneline"], "command": "git log --oneline" },
    { "action": "可视化分支合并图 (View Commit Graph)", "keywords": ["图", "合并图", "可视化", "graph", "log", "decorate", "all"], "command": "git log --oneline --graph --decorate --all" },
    { "action": "查看命令历史记录/找回丢失提交 (View Reference Log)", "keywords": ["历史", "恢复", "找回", "reflog", "history"], "command": "git reflog" },
    { "action": "对比工作区与暂存区的差异 (Show Diff Unstaged)", "keywords": ["差异", "对比", "diff", "unstaged"], "command": "git diff" },
    { "action": "对比暂存区与仓库最新版本的差异 (Show Diff Staged)", "keywords": ["差异", "对比", "暂存区", "diff", "staged", "cached"], "command": "git diff --cached" },
    { "action": "查看所有本地分支 (List Local Branches)", "keywords": ["分支", "查看", "branch", "local"], "command": "git branch" },
    { "action": "查看所有本地和远程分支 (List All Branches)", "keywords": ["分支", "查看", "远程", "branch", "all", "a"], "command": "git branch -a" },
    { "action": "创建并切换到新分支 (Create & Switch Branch)", "keywords": ["新建分支", "切换", "checkout", "switch", "branch", "b", "c"], "command": "git checkout -b <branch_name> 或 git switch -c <branch_name>" },
    { "action": "切换到已有分支 (Switch Branch)", "keywords": ["切换", "分支", "checkout", "switch", "branch"], "command": "git checkout <branch_name> 或 git switch <branch_name>" },
    { "action": "合并指定分支到当前分支 (Merge Branch)", "keywords": ["合并", "分支", "merge", "branch"], "command": "git merge <branch_name>" },
    { "action": "删除本地分支 (Delete Branch Safely)", "keywords": ["删除", "分支", "branch", "delete", "d"], "command": "git branch -d <branch_name>" },
    { "action": "强制删除本地分支 (Force Delete Branch)", "keywords": ["强制删除", "分支", "branch", "delete", "D"], "command": "git branch -D <branch_name>" },
    { "action": "查看关联的远程仓库地址 (List Remotes)", "keywords": ["远程仓库", "地址", "remote", "v"], "command": "git remote -v" },
    { "action": "关联远程仓库 (Add Remote Repository)", "keywords": ["关联", "添加远程", "remote", "add", "origin"], "command": "git remote add origin <url>" },
    { "action": "推送到远程仓库并建立追踪 (Push & Track Branch)", "keywords": ["推送", "远程", "追踪", "push", "origin", "u"], "command": "git push -u origin <branch_name>" },
    { "action": "推送本地提交到远程仓库 (Push to Remote)", "keywords": ["推送", "远程", "push", "origin"], "command": "git push origin <branch_name>" },
    { "action": "拉取远程分支并自动合并 (Pull & Merge)", "keywords": ["拉取", "更新", "pull", "origin", "merge"], "command": "git pull origin <branch_name>" },
    { "action": "获取远程仓库的最新更新但不合并 (Fetch Remotes)", "keywords": ["拉取", "更新", "不合并", "fetch", "origin"], "command": "git fetch origin" },
    { "action": "暂存当前工作区未提交的修改 (Stash Changes)", "keywords": ["暂存", "保存修改", "stash", "save"], "command": "git stash" },
    { "action": "恢复并删除最近一次的暂存内容 (Pop Stash)", "keywords": ["恢复", "还原", "暂存", "stash", "pop"], "command": "git stash pop" },
    { "action": "查看所有暂存列表 (List Stashes)", "keywords": ["查看", "暂存", "列表", "stash", "list"], "command": "git stash list" },
    { "action": "清除最近一次的暂存内容 (Drop Stash)", "keywords": ["清除", "丢弃", "暂存", "stash", "drop"], "command": "git stash drop" },
    { "action": "撤销工作区中指定文件的修改 (Discard Working Changes)", "keywords": ["撤销", "丢弃", "修改", "restore", "checkout"], "command": "git restore <file> 或 git checkout -- <file>" },
    { "action": "撤销已暂存的文件回到工作区 (Unstage File)", "keywords": ["撤销暂存", "暂存区", "restore", "staged", "reset"], "command": "git restore --staged <file> 或 git reset HEAD <file>" },
    { "action": "软重置回退到上一次 commit 但保留代码 (Soft Reset)", "keywords": ["回退", "重置", "保留代码", "reset", "soft", "head"], "command": "git reset --soft HEAD~1" },
    { "action": "硬重置回退并丢弃所有未提交修改 (Hard Reset)", "keywords": ["回退", "重置", "强行丢弃", "reset", "hard", "head"], "command": "git reset --hard HEAD~1" }
]

LAZYGIT_DATA = [
    { "action": "打开快捷键帮助菜单 (Open Help Menu)", "keywords": ["帮助", "快捷键", "菜单", "help", "keybindings", "menu", "?"], "command": "?" },
    { "action": "在主要面板之间进行切换 (Switch Panels)", "keywords": ["面板", "切换", "导航", "panel", "switch", "tab", "1", "2", "3", "4", "5"], "command": "1 / 2 / 3 / 4 / 5 (分别对应 状态/文件/分支/提交/暂存) 或 Tab" },
    { "action": "退出子级菜单/返回上一级面板/关闭弹窗 (Go Back/Esc/Return)", "keywords": ["返回", "回退", "上一级", "退出", "关闭", "esc", "q", "back", "return"], "command": "Esc 或 q" },
    { "action": "文件树视图下折叠目录/返回上层文件夹 (Collapse Directory)", "keywords": ["折叠", "收起", "目录", "上层", "文件夹", "collapse", "directory", "h", "left"], "command": "h (或 左方向键)" },
    { "action": "退出分支 commit log 视图并返回分支列表 (Exit Branch Commits and Return to Branches)", "keywords": ["回退", "分支列表", "提交记录", "日志", "返回", "exit", "log", "branch", "commits", "esc", "q"], "command": "Esc 或 q" },
    { "action": "退出 Lazygit (Quit Lazygit)", "keywords": ["退出", "关闭", "quit", "exit", "q"], "command": "q 或 Ctrl + c" },
    { "action": "撤销上一步 Git 操作 (Undo Last Git Cmd)", "keywords": ["撤销", "上一步", "undo", "last", "z"], "command": "z (基于 reflog 撤销提交，不包含工作区修改)" },
    { "action": "重做上一步 Git 操作 (Redo Last Git Cmd)", "keywords": ["重做", "恢复", "redo", "Z"], "command": "Z (Shift + z)" },
    { "action": "执行自定义 Shell 命令 (Execute Shell Cmd)", "keywords": ["执行", "命令", "shell", "command", ":"], "command": ":" },
    { "action": "暂存/取消暂存单个文件 (Stage/Unstage File)", "keywords": ["暂存", "取消暂存", "单文件", "stage", "unstage", "space", "空格"], "command": "Space (空格键)" },
    { "action": "暂存/取消暂存所有文件 (Stage/Unstage All Files)", "keywords": ["暂存所有", "全选", "stage", "all", "a"], "command": "a" },
    { "action": "输入提交信息并提交 (Commit Changes)", "keywords": ["提交", "输入", "commit", "c"], "command": "c (输入 message 后按回车确认)" },
    { "action": "使用外部 Git 编辑器提交 (Commit via Git Editor)", "keywords": ["编辑器", "提交", "commit", "editor", "C"], "command": "C (Shift + c)" },
    { "action": "修改(追加)最近一次提交 (Amend Last Commit)", "keywords": ["追加", "修改", "最近一次", "amend", "A"], "command": "A (Shift + a)" },
    { "action": "推送当前分支到远程仓库 (Push to Remote)", "keywords": ["推送", "远程", "push", "P"], "command": "P (Shift + p)" },
    { "action": "从远程仓库拉取更新 (Pull from Remote)", "keywords": ["拉取", "更新", "pull", "p"], "command": "p" },
    { "action": "拉取获取最新更新但不合并 (Fetch updates)", "keywords": ["获取", "更新", "fetch", "f"], "command": "f" },
    { "action": "放弃工作区中的文件修改 (Discard File Changes)", "keywords": ["放弃", "丢弃", "修改", "discard", "d"], "command": "d" },
    { "action": "在扁平视图和树状目录视图之间切换 (Toggle File Tree View)", "keywords": ["树状", "目录", "视图", "flat", "tree", "layout", "`"], "command": "` (反引号)" },
    { "action": "在外部编辑器中打开文件 (Edit File in Editor)", "keywords": ["打开", "编辑", "外部", "editor", "e"], "command": "e" },
    { "action": "使用系统默认程序打开文件 (Open File in App)", "keywords": ["打开", "默认程序", "open", "o"], "command": "o" },
    { "action": "查看并进入单个文件的具体更改/交互式暂存模式 (View File Changes / Line-by-Line Hunk View)", "keywords": ["查看更改", "单文件", "修改内容", "交互式", "hunk", "line", "diff", "enter", "回车"], "command": "Enter (回车键进入，Esc 或 q 退出返回)" },
    { "action": "查看暂存选项列表 (Stash Options)", "keywords": ["暂存", "保存修改", "stash", "options", "S"], "command": "S (Shift + s)" },
    { "action": "将所有修改进行 Git 暂存 (Stash All Changes)", "keywords": ["暂存", "保存修改", "stash", "s"], "command": "s" },
    { "action": "检出/切换选择的分支 (Checkout Branch)", "keywords": ["检出", "切换", "分支", "checkout", "space", "空格"], "command": "Space (空格键)" },
    { "action": "创建新分支 (Create New Branch)", "keywords": ["创建", "新建", "分支", "new", "branch", "n"], "command": "n" },
    { "action": "将选中的分支合并到当前分支 (Merge Selected Branch)", "keywords": ["合并", "分支", "merge", "M"], "command": "M (Shift + m)" },
    { "action": "在选中分支上变基当前分支 (Rebase Checked-out onto Selected)", "keywords": ["变基", "分支", "rebase", "r"], "command": "r" },
    { "action": "强制切换分支并丢弃本地改动 (Force Checkout Branch)", "keywords": ["强制切换", "丢弃改动", "checkout", "force", "F"], "command": "F (Shift + f)" },
    { "action": "删除分支 (Delete Branch)", "keywords": ["删除", "分支", "delete", "d"], "command": "d" },
    { "action": "重命名分支 (Rename Branch)", "keywords": ["重命名", "分支", "rename", "R"], "command": "R (Shift + r)" },
    { "action": "分支面板内切换本地分支/远程/标签子面板 (Switch sub-tabs in Branches panel)", "keywords": ["远程分支", "本地分支", "标签", "子面板", "切换", "branch", "remote", "tags", "[", "]"], "command": "[ 或 ] (中括号键)" },
    { "action": "展开并查看选中的远程仓库的分支 (Expand/View Remote Branches)", "keywords": ["远程分支", "展开", "查看", "origin", "remote", "branches", "view", "enter", "回车"], "command": "Enter (回车键)" },
    { "action": "查看选中提交中包含的文件 (View Files in Commit)", "keywords": ["查看文件", "提交文件", "view", "files", "enter", "回车"], "command": "Enter (回车键)" },
    { "action": "对当前面板列表项进行模糊搜索/过滤 (Filter Current List)", "keywords": ["搜索", "过滤", "查找", "定位", "filter", "search", "/"], "command": "/" },
    { "action": "按文件路径过滤提交记录历史 (Filter Commits by File Path)", "keywords": ["过滤历史", "文件路径", "历史提交", "特定文件", "filter", "commits", "file", "path", "ctrl", "s"], "command": "Ctrl + s (输入文件路径，仅显示修改该文件的提交)" },
    { "action": "将选中的提交检出为分离头指针 (Checkout Commit)", "keywords": ["检出", "分离头", "checkout", "commit", "space", "空格"], "command": "Space (空格键)" },
    { "action": "从选中提交开始进行交互式变基 (Start Interactive Rebase)", "keywords": ["交互式变基", "变基", "rebase", "interactive", "e"], "command": "e" },
    { "action": "将选中提交向下合并 (Squash Commit)", "keywords": ["合并", "向下合并", "squash", "s"], "command": "s" },
    { "action": "丢弃/删除选中提交 (Drop/Delete Commit)", "keywords": ["丢弃", "删除", "提交", "drop", "delete", "d"], "command": "d" },
    { "action": "修改选中提交的提交信息 (Reword Commit)", "keywords": ["修改信息", "改写", "reword", "r"], "command": "r" },
    { "action": "撤销选中提交的修改并生成新提交 (Revert Commit)", "keywords": ["撤销", "生成提交", "revert", "t"], "command": "t" },
    { "action": "在选中提交上新建标签 (Tag Commit)", "keywords": ["新建标签", "标签", "tag", "T"], "command": "T (Shift + t)" },
    { "action": "复制选中的提交用作樱桃挑选 (Copy/Cherry-pick Commit)", "keywords": ["樱桃挑选", "复制", "cherry-pick", "copy", "C"], "command": "C (Shift + c)" },
    { "action": "粘贴/应用复制的樱桃挑选提交 (Paste/Cherry-pick Commit)", "keywords": ["樱桃挑选", "粘贴", "cherry-pick", "paste", "V"], "command": "V (Shift + v)" },
    { "action": "上下移动提交顺序 (Move Commit Up/Down)", "keywords": ["移动顺序", "调整", "move", "alt", "ctrl", "j", "k"], "command": "Alt + Up / Down (或 Ctrl + k / j)" },
    { "action": "应用选中的暂存内容 (Apply Stash)", "keywords": ["应用暂存", "恢复暂存", "apply", "stash", "space", "空格"], "command": "Space (空格键)" },
    { "action": "应用并删除选中的暂存内容 (Pop Stash)", "keywords": ["应用删除", "弹出暂存", "pop", "stash", "g"], "command": "g" },
    { "action": "删除选中的暂存内容 (Drop Stash)", "keywords": ["删除暂存", "丢弃", "drop", "stash", "d"], "command": "d" },
    { "action": "从选中的暂存内容新建分支 (New Branch from Stash)", "keywords": ["新建分支", "暂存创建", "branch", "stash", "n"], "command": "n" },
    { "action": "解决冲突：选择当前(我们的)更改 (Pick Hunk)", "keywords": ["选择当前", "解决冲突", "pick", "hunk", "space", "空格"], "command": "Space (空格键)" },
    { "action": "解决冲突：同时保留双方更改 (Pick Both Hunks)", "keywords": ["保留双方", "解决冲突", "both", "hunks", "b"], "command": "b" },
    { "action": "冲突导航：下一个/上一个冲突 (Next/Prev Conflict)", "keywords": ["下一个", "上一个", "冲突导航", "conflict", "l", "h"], "command": "l / h (或 右/左 方向键)" },
    { "action": "冲突导航：下一个/上一个更改块 (Next/Prev Hunk)", "keywords": ["下一个", "上一个", "更改块", "hunk", "j", "k"], "command": "j / k (或 下/上 方向键)" }
]

MVN_DATA = [
    { "action": "清理并打包 (Clean & Package)", "keywords": ["清理", "打包", "clean", "package", "mvn"], "command": "mvn clean package" },
    { "action": "跳过测试清理并打包 (Package Skip Tests)", "keywords": ["打包", "跳过测试", "skip", "test", "mvn", "Dmaven.test.skip"], "command": "mvn clean package -Dmaven.test.skip=true" },
    { "action": "清理并安装到本地仓库 (Install to Local Repo)", "keywords": ["安装", "本地", "install", "mvn"], "command": "mvn clean install" },
    { "action": "跳过测试安装到本地仓库 (Install Skip Tests)", "keywords": ["安装", "跳过测试", "install", "skip", "test", "mvn"], "command": "mvn clean install -Dmaven.test.skip=true" },
    { "action": "编译源代码 (Compile)", "keywords": ["编译", "compile", "mvn"], "command": "mvn compile" },
    { "action": "清理目标目录 (Clean)", "keywords": ["清理", "clean", "mvn"], "command": "mvn clean" },
    { "action": "运行测试 (Test)", "keywords": ["测试", "test", "mvn"], "command": "mvn test" },
    { "action": "显示依赖树 (Dependency Tree)", "keywords": ["依赖树", "冲突", "dependency", "tree", "mvn"], "command": "mvn dependency:tree" },
    { "action": "下载源码包 (Download Sources)", "keywords": ["下载", "源码", "source", "mvn"], "command": "mvn dependency:sources" },
    { "action": "下载 Javadoc (Download Javadocs)", "keywords": ["下载", "javadoc", "mvn"], "command": "mvn dependency:resolve -Dclassifier=javadoc" },
    { "action": "部署到远程私服 (Deploy)", "keywords": ["部署", "私服", "deploy", "mvn"], "command": "mvn clean deploy" },
    { "action": "强制更新快照依赖 (Force Update Snapshots)", "keywords": ["强制", "更新", "快照", "update", "snapshot", "U", "mvn"], "command": "mvn clean package -U" },
    { "action": "非交互/批处理模式构建 (Batch Mode / CI)", "keywords": ["非交互", "批处理", "流水线", "静默输出", "ci", "batch", "B", "mvn"], "command": "mvn clean package -B" },
    { "action": "非交互且强制更新构建 (CI Batch & Update)", "keywords": ["流水线", "非交互", "强制", "更新", "ci", "batch", "update", "B", "U", "mvn"], "command": "mvn clean package -B -U" }
]

def ensure_data_files(data_dir: str):
    """
    Ensure the data files exist in the specified directory.
    If they don't exist, create them with the initial data.
    """
    os.makedirs(data_dir, exist_ok=True)
    
    datasets = {
        "vim.json": VIM_DATA,
        "curl.json": CURL_DATA,
        "awk.json": AWK_DATA,
        "grep.json": GREP_DATA,
        "tail.json": TAIL_DATA,
        "ls.json": LS_DATA,
        "idea.json": IDEA_DATA,
        "git.json": GIT_DATA,
        "lazygit.json": LAZYGIT_DATA,
        "mvn.json": MVN_DATA
    }
    
    for filename, data in datasets.items():
        filepath = os.path.join(data_dir, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Created initial data file: {filepath}")
        else:
            print(f"Data file already exists: {filepath}")

if __name__ == "__main__":
    import platform
    app_name = "cmd_helper"
    if platform.system() == "Windows":
        base_dir = os.environ.get("APPDATA", os.path.expanduser("~"))
        default_dir = os.path.join(base_dir, app_name, "data")
    else:
        base_dir = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        default_dir = os.path.join(base_dir, app_name, "data")
    
    print(f"Regenerating data files in {default_dir}...")
    os.makedirs(default_dir, exist_ok=True)
    
    datasets = {
        "vim.json": VIM_DATA,
        "curl.json": CURL_DATA,
        "awk.json": AWK_DATA,
        "grep.json": GREP_DATA,
        "tail.json": TAIL_DATA,
        "ls.json": LS_DATA,
        "idea.json": IDEA_DATA,
        "git.json": GIT_DATA,
        "lazygit.json": LAZYGIT_DATA,
        "mvn.json": MVN_DATA
    }
    
    for filename, data in datasets.items():
        filepath = os.path.join(default_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Overwrote/updated data file: {filepath}")
