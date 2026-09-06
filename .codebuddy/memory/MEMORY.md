# 长期记忆 MEMORY.md

## 项目与仓库
- 用户文档仓库根: `c:\Users\kanghua\docs`(docsify 结构; 各栏目目录有自己的 `_sidebar.md`/`_navbar.md`)。
- 2026-09-04 起新增 mkdocs-material 构建(用户已改为**官方布局 + 工程入仓**, 终版):
  - 仓库根只剩: `README.md` / `CNAME` / `requirement.txt` / `mkdocs-docs/`(工程)。docsify 的 index.html/_navbar/_sidebar/_coverpage/static 已被用户移除(疑似弃用 docsify)。
  - 工程 `docs/mkdocs-docs/`: `mkdocs.yml` + 内容目录 `mkdocs-docs/`(python/auto/linux/k8s-note/k8s-2023/dba-note/_media) + 成品 `site/`(位于内容目录之外, 不触发"site 在 docs_dir 内"限制)。
  - 关键配置: `docs_dir: mkdocs-docs`(内容目录)、`site_dir: site`(工程内、内容目录外)、`use_directory_urls: false`、`exclude_docs: **/_*.md / **/*.pyc / **/__pycache__/`。
  - 依赖: 全局 Python3.12 已装 mkdocs 1.6.1 + mkdocs-material 9.7.7 + pymdown-extensions 11.0.2(也可用仓库根 `requirement.txt` 重建); 仓库根 `.venv` 已被用户清理。
  - 导航: nav 固化在 mkdocs.yml(223 页), 手工维护; 一次性 `generate_nav.py` 已按用户要求删除(曾按 docsify 各 `_sidebar.md` 自动生成 nav)。
  - 内容目录根的 `README.md`(首页)与 `CNAME` 由仓库根同名文件复制而来(成品需含)。
  - 仓库根 `.gitignore`(已精简为 Python+mkdocs 专用, 去除 Django/Flask/Scrapy 等框架特定无用条目)忽略 `site/`(mkdocs 构建产物, 约1万文件/1.8G 不进 git)、Python 虚拟环境(venv/env/.venv/ENV 等)、缓存/编译产物(`__pycache__`/*.py[cod])、测试/lint 缓存、`.DS_Store`、`.env`、IDE(`.idea`/`.vscode`)等。
- 注意: 各栏目 `README.md` 被 mkdocs 渲染成 `index.html`(非 README.html); 新增页面在 mkdocs.yml 的 `nav` 下加一行 "标题: 相对路径" 即可。
- 旧成品 `c:\Users\kanghua\mkdocs-site`(1.8G, 旧布局产物)已无用, 可删。

## 导航规则(用户偏好)
- 顶部菜单=根 `_navbar.md`; 每个顶部菜单下侧边导航=该栏目自带的 `_sidebar.md`。
- 未被 _sidebar 收录的 .md 自动补全进导航, 保证内容不丢(生成脚本已实现)。
- _sidebar 中引用的坏链/缺失文件自动跳过, 不硬造。

## 备注
- 内容 md 内有大量历史遗留的坏相对图片链接, 构建会出现 WARNING, 属内容问题。
- mkdocs.yml 为站点唯一配置, **手工维护**(nav 直接写在 mkdocs.yml); 早期自动生成脚本 `generate_nav.py` 已按用户要求删除、不再存在, 改配置直接编辑 mkdocs.yml 即可。
- 仓库根当前文件: `README.md`(项目说明)/`CNAME`(自定义域名)/`requirement.txt`(Python 依赖)/`.gitignore`(本次建)。docsify 入口与 mkdocs.cmd/.sh 已移除/清理。
- 交互语言: 简体中文。
- 环境: `execute_command` 的 shell 是 **Git Bash**(Windows), 需用 Unix 命令(find/rm); 不要嵌套 `powershell -Command` 且内部含 `$变量`(bash 会把 `$` 展开为空, 导致 PowerShell 命令失效)。
- 部署方式(用户确认): 构建产物 `site/` **不进 git**(已被根 `.gitignore` 忽略), 用 `mkdocs gh-deploy` 把 `site/` 推送到 GitHub 的 `gh-pages` 分支; 主分支只保留源码。运行位置: 因 `mkdocs.yml` 在 `mkdocs-docs/` 子目录, 需 `cd mkdocs-docs && mkdocs gh-deploy` 或 `mkdocs gh-deploy -f mkdocs-docs/mkdocs.yml`。自定义域名 `docs.chengkanghua.top` 靠内容目录根 `CNAME`(由仓库根同名文件复制)随站点部署。
- docsify 已彻底弃用: 2026-09-06 删除内容目录内 14 个 docsify 残留文件(`_sidebar.md`×8/`_navbar.md`×4/`.nojekyll`×2), 仓库现仅 mkdocs-material 工程。
- 注意: `mkdocs-docs/mkdocs-docs/extra.css` 被 `mkdocs.yml` 的 `extra_css` 引用, 是网站自定义样式, **不可删**; 2026-09-06 发现该文件此前实际缺失(被引用但文件不在, 致 README 所述窄屏横排样式未生效), 已创建并加入: 顶部 header+tabs 浅灰背景(#f5f5f5)+深灰文字、窄屏标签横排。顶部 GitHub 图标链接由 `mkdocs.yml` 的 `repo_url: https://github.com/chengkanghua/docs` 控制。`mkdocs-docs/.mkdocsignore` 防止噪声复制进 site/, 建议保留。真正可删的"垃圾"只有 `site/`。第三方代码目录(uric_web/myblog/bootstrap/VueDemo/Muban/statics)被 exclude_docs 排除不发布, 但属笔记示例资产, 勿删。
