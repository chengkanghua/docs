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
  - `.gitignore` 已追加 `/mkdocs-docs/site/`(成品 1.8G 不进 git)。
- 注意: 各栏目 `README.md` 被 mkdocs 渲染成 `index.html`(非 README.html); 新增页面在 mkdocs.yml 的 `nav` 下加一行 "标题: 相对路径" 即可。
- 旧成品 `c:\Users\kanghua\mkdocs-site`(1.8G, 旧布局产物)已无用, 可删。

## 导航规则(用户偏好)
- 顶部菜单=根 `_navbar.md`; 每个顶部菜单下侧边导航=该栏目自带的 `_sidebar.md`。
- 未被 _sidebar 收录的 .md 自动补全进导航, 保证内容不丢(生成脚本已实现)。
- _sidebar 中引用的坏链/缺失文件自动跳过, 不硬造。

## 备注
- 内容 md 内有大量历史遗留的坏相对图片链接, 构建会出现 WARNING, 属内容问题。
- mkdocs.yml 全部由 `mkdocs-docs/generate_nav.py` 生成(脚本含完整配置模板); 改任何配置(exclude_docs/主题等)都改 generate_nav.py 再重跑, 勿直接改 mkdocs.yml(会被覆盖)。
- docs 根目录永久文件 = docsify 入口(index.html/_coverpage.md/_navbar.md/_sidebar.md/CNAME) + mkdocs.cmd/.sh + README.md。此前的 index.html.bak、nohup.out 已清理。
- 交互语言: 简体中文。
