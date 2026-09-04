import gitlab

if __name__ == '__main__':
    """获取所有项目列表"""
    url = "http://10.211.55.20:8993"
    token = "JMx5wL2CrLrJKnDDGzXo"
    gl = gitlab.Gitlab(url, token)
    # print(gl)

    # """获取所有项目列表"""
    # projects = gl.projects.list(all=True)
    # for project in projects:
    #     print(project.id, project.name ,project.description)


    # """获取单个项目"""
    # project = gl.projects.get(2)

    # print("项目ID", project.id)
    # print("项目描述", project.description)
    # print("项目名", project.name)
    # print("创建时间", project.created_at)
    # print("默认主分支", project.default_branch)
    # print("tag数量", len(project.tag_list))
    # print("仓库地址[ssh]", project.ssh_url_to_repo)
    # print("仓库地址[http]", project.http_url_to_repo)
    # print("仓库访问地址", project.web_url)
    # print("仓库可见性", project.visibility)  # internal 内部项目 public 开源项目   private私有项目
    # print("仓库派生数量", project.forks_count)
    # print("仓库星标数量", project.star_count)
    # print("仓库拥有者", getattr(project, "owner", None)) # 因为默认的第一个仓库是没有拥有者的!!

    #
    # """
    # {
    #     'id': 2,
    #     'description': '自动化运维平台',
    #     'name': 'uric',
    #     'name_with_namespace': 'Administrator / uric',
    #     'path': 'uric',
    #     'path_with_namespace': 'root/uric',
    #     'created_at': '2022-08-20T03:34:48.446Z',
    #     'default_branch': 'main',
    #     'tag_list': [],
    #     'topics': [],
    #     'ssh_url_to_repo': 'ssh://git@192.168.101.8:2224/root/uric.git',
    #     'http_url_to_repo': 'http://192.168.101.8:8993/root/uric.git',
    #     'web_url': 'http://192.168.101.8:8993/root/uric',
    #     'readme_url': 'http://192.168.101.8:8993/root/uric/-/blob/main/README.md',
    #     'avatar_url': None,
    #     'forks_count': 0,
    #     'star_count': 0,
    #     'last_activity_at': '2022-08-20T03:34:48.446Z',
    #     'namespace': {
    #         'id': 1,
    #         'name': 'Administrator',
    #         'path': 'root',
    #         'kind': 'user',
    #         'full_path': 'root',
    #         'parent_id': None,
    #         'avatar_url': 'https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon',
    #         'web_url': 'http://192.168.101.8:8993/root'
    #     },
    #     '_links': {
    #         'self': 'http://192.168.101.8:8993/api/v4/projects/2',
    #         'issues': 'http://192.168.101.8:8993/api/v4/projects/2/issues',
    #         'merge_requests': 'http://192.168.101.8:8993/api/v4/projects/2/merge_requests',
    #         'repo_branches': 'http://192.168.101.8:8993/api/v4/projects/2/repository/branches',
    #         'labels': 'http://192.168.101.8:8993/api/v4/projects/2/labels',
    #         'events': 'http://192.168.101.8:8993/api/v4/projects/2/events',
    #         'members': 'http://192.168.101.8:8993/api/v4/projects/2/members'
    #     },
    #     'packages_enabled': True,
    #     'empty_repo': False,
    #     'archived': False,
    #     'visibility': 'internal',
    #     'owner': {
    #         'id': 1,
    #         'username': 'root',
    #         'name': 'Administrator',
    #         'state': 'active',
    #         'avatar_url': 'https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80&d=identicon',
    #         'web_url': 'http://192.168.101.8:8993/root'},
    #         'resolve_outdated_diff_discussions': False,
    #         'container_expiration_policy': {'cadence': '1d',
    #         'enabled': False,
    #         'keep_n': 10,
    #         'older_than': '90d',
    #         'name_regex': '.*',
    #         'name_regex_keep': None,
    #         'next_run_at': '2022-08-21T03:34:49.221Z'},
    #         'issues_enabled': True,
    #         'merge_requests_enabled': True,
    #         'wiki_enabled': True,
    #         'jobs_enabled': True,
    #         'snippets_enabled': True,
    #         'container_registry_enabled': True,
    #         'service_desk_enabled': False,
    #         'service_desk_address': None,
    #         'can_create_merge_request_in': True,
    #         'issues_access_level': 'enabled',
    #         'repository_access_level': 'enabled',
    #         'merge_requests_access_level': 'enabled',
    #         'forking_access_level': 'enabled',
    #         'wiki_access_level': 'enabled',
    #         'builds_access_level': 'enabled',
    #         'snippets_access_level': 'enabled',
    #         'pages_access_level': 'private',
    #         'operations_access_level': 'enabled',
    #         'analytics_access_level': 'enabled',
    #         'container_registry_access_level': 'enabled',
    #         'emails_disabled': None,
    #         'shared_runners_enabled': True,
    #         'lfs_enabled': True,
    #         'creator_id': 1,
    #         'import_status': 'none',
    #         'open_issues_count': 0,
    #         'ci_default_git_depth': 50,
    #         'ci_forward_deployment_enabled': True,
    #         'ci_job_token_scope_enabled': False,
    #         'public_jobs': True,
    #         'build_timeout': 3600,
    #         'auto_cancel_pending_pipelines': 'enabled',
    #         'build_coverage_regex': None,
    #         'ci_config_path': None,
    #         'shared_with_groups': [],
    #         'only_allow_merge_if_pipeline_succeeds': False,
    #         'allow_merge_on_skipped_pipeline': None,
    #         'restrict_user_defined_variables': False,
    #         'request_access_enabled': True,
    #         'only_allow_merge_if_all_discussions_are_resolved': False,
    #         'remove_source_branch_after_merge': True,
    #         'printing_merge_request_link_enabled': True,
    #         'merge_method': 'merge',
    #         'squash_option': 'default_off',
    #         'suggestion_commit_message': None,
    #         'merge_commit_template': None,
    #         'squash_commit_template': None,
    #         'auto_devops_enabled': True,
    #         'auto_devops_deploy_strategy': 'continuous',
    #         'autoclose_referenced_issues': True,
    #         'repository_storage': 'default',
    #         'keep_latest_artifact': True,
    #         'permissions': {
    #             'project_access': {
    #                 'access_level': 40,
    #                 'notification_level': 3
    #             },
    #             'group_access': None
    #         }
    #     }
    # """

    # """根据项目名搜索项目"""
    # projects = gl.projects.list(search='uric')
    # print(projects)


    # """根据项目的可见性列出符合条件的项目"""
    # projects = gl.projects.list(visibility='public')  # 公有项目列表
    # projects = gl.projects.list(visibility='private') # 私有项目列表
    # projects = gl.projects.list(visibility='internal') # 内部项目列表
    # print(projects)

    """创建一个项目"""
    # project = gl.projects.create({
    #     'name': 'test2',   # 项目名，不要使用中文或其他特殊符号
    #     # 'path': 'test2',   # 访问路径，如果不设置path，则path的值默认为name
    #     'description': '测试项目2',
    #     'visibility': 'public'
    # })
    # print(project)
    # """更新一个项目"""
    # # 先获取项目
    # project = gl.projects.get(3)
    # 在获取了项目以后，直接对当前项目对象设置属性进行覆盖，后面调用save方法即可保存更新内容
    # project.description = "测试项目2的描述信息被修改了1次"
    # project.save()

    # """删除一个项目"""
    # project = gl.projects.get(3)
    # project.delete()



    # """分支管理：获取所有分支"""
    # project = gl.projects.get(2)
    # branches = project.branches.list()
    # print(branches)  # [<ProjectBranch name:main>]

    # """根据名称获取一个分支"""
    # project = gl.projects.get(2)
    # branch = project.branches.get('master')
    # print("分支名称：", branch.name)
    # print("分支最新提交记录：", branch.commit)
    # print("分支合并状态：", branch.merged)
    # print("是否属于保护分支：", branch.protected)
    # print("当前分支是否可以推送代码：", branch.can_push)
    # print("是否是默认分支：", branch.default)
    # print("当前分支的访问路径：", branch.web_url)
    #
    # """
    # {
    #     'name': 'main',
    #     'commit': {
    #         'id': 'be71595d791b3437dee7e36a9dc221376392912f',
    #         'short_id': 'be71595d',
    #         'created_at': '2022-08-20T04:00:44.000+00:00',
    #         'parent_ids': [],
    #         'title': 'Initial commit',
    #         'message': 'Initial commit',
    #         'author_name': 'Administrator',
    #         'author_email': 'admin@example.com',
    #         'authored_date': '2022-08-20T04:00:44.000+00:00',
    #         'committer_name': 'Administrator',
    #         'committer_email': 'admin@example.com',
    #         'committed_date': '2022-08-20T04:00:44.000+00:00',
    #         'trailers': {},
    #         'web_url': 'http://192.168.101.8:8993/root/tools/-/commit/be71595d791b3437dee7e36a9dc221376392912f'
    #     },
    #     'merged': False,
    #     'protected': True,
    #     'developers_can_push': False,
    #     'developers_can_merge': False,
    #     'can_push': True,
    #     'default': True,
    #     'web_url': 'http://192.168.101.8:8993/root/tools/-/tree/main'
    # """

    # """给指定项目创建分支"""
    # project = gl.projects.get(2)
    # branch = project.branches.create({'branch': 'feature/user', 'ref': 'master'})
    # print(branch)

    """更新分支的属性【gitbal的v4版本中没有保护分支和取消保护分支的功能】"""
    # project = gl.projects.get(2)
    # branch = project.branches.get('feature/user')
    # # 设置当前分支为保护分支
    # branch.protect()


    # """删除一个分支"""
    # # 注意，只有一个保护分支时，是不能删除当前分支的
    # project = gl.projects.get(2)
    # project.branches.delete('feature/user')

    # """创建一个tag标签"""
    # project = gl.projects.get(2)
    # tag = project.tags.create({'tag_name': 'v1.0', 'ref': 'master'})
    # print(tag)

    # """获取所有tag标签"""
    # project = gl.projects.get(2)
    # tags = project.tags.list(all=True)
    # print(tags)

    # """获取一个tag标签信息"""
    # project = gl.projects.get(2)
    # tag = project.tags.get('v1.0')
    # print("标签名", tag.name)
    # print("标签的版本描述", tag.message)
    # print("标签的唯一标记(版本号)", tag.target) # 实际上就是本次创建标签时的分支最后一条commit的版本号
    # print("标签的最后一个commit记录", tag.commit)
    # print("当前标签是否发布", tag.release)
    # print("当前标签是佛属于保护标签", tag.protected)
    #
    # """
    # {
    #     'name': 'v1.0',
    #     'message': '',
    #     'target': 'be71595d791b3437dee7e36a9dc221376392912f',
    #     'commit': {
    #         'id': 'be71595d791b3437dee7e36a9dc221376392912f',
    #         'short_id': 'be71595d',
    #         'created_at': '2022-08-20T04:00:44.000+00:00',
    #         'parent_ids': [],
    #         'title': 'Initial commit',
    #         'message': 'Initial commit',
    #         'author_name': 'Administrator',
    #         'author_email': 'admin@example.com',
    #         'authored_date': '2022-08-20T04:00:44.000+00:00',
    #         'committer_name': 'Administrator',
    #         'committer_email': 'admin@example.com',
    #         'committed_date': '2022-08-20T04:00:44.000+00:00',
    #         'trailers': {},
    #         'web_url': 'http://192.168.101.8:8993/root/tools/-/commit/be71595d791b3437dee7e36a9dc221376392912f'
    #     },
    #     'release': None,
    #     'protected': False
    # }
    # """


    # """指定项目的commit提交记录"""
    # project = gl.projects.get(2)
    # commits = project.commits.list(all=True)
    # print(commits)

    # """根据版本号来获取commit记录"""
    # project = gl.projects.get(2)
    # commit = project.commits.get("c74c738d5f386ec062910b66620625e19deae9a8")
    # print(commit)
    # print(getattr(commit,'title'))
    # """
    # {
    #     'id': 'be71595d791b3437dee7e36a9dc221376392912f',
    #     'short_id': 'be71595d',
    #     'created_at': '2022-08-20T04:00:44.000+00:00',
    #     'parent_ids': [],
    #     'title': 'Initial commit',
    #     'message': 'Initial commit',
    #     'author_name': 'Administrator',
    #     'author_email': 'admin@example.com',
    #     'authored_date': '2022-08-20T04:00:44.000+00:00',
    #     'committer_name': 'Administrator',
    #     'committer_email': 'admin@example.com',
    #     'committed_date': '2022-08-20T04:00:44.000+00:00',
    #     'trailers': {},
    #     'web_url': 'http://192.168.101.8:8993/root/tools/-/commit/be71595d791b3437dee7e36a9dc221376392912f',
    #     'stats': {
    #         'additions': 3,
    #         'deletions': 0,
    #         'total': 3},
    #         'status': None,
    #         'project_id': 3,
    #         'last_pipeline': None
    #     }
    # """


    # """创建一个commit版本"""
    # project = gl.projects.get(2)
    # data = {
    # 'branch': 'master',
    # 'commit_message': '提交代码的版本描述',
    #     'actions': [
    #         {
    #         'action': 'create',  # 创建文件
    #         # 'action': 'update',  # 更新文件
    #         # 'action': 'delete',    # 删除文件
    #         # 'file_path':'uric.log' # 配合删除文件action就是删除的文件路径
    #         'file_path': 'docs/uric_api/logs/uric.log', # 文件路径 上传文件的仓库的路径
    #         'content': '上传文件的内容'  # 文件内容
    #         }
    #     ]
    # }
    #
    # commit = project.commits.create(data)


    """获取用户列表"""
    # print(gl.users.list())  # [<User id:1 username:root>]

    """获取单个用户信息"""
    user = gl.users.get(1)
    print(user)


