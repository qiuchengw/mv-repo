# mv-repo
自动化将git repo迁移到新的地址

仅支持gitlab。

目前代码比较粗糙


# -0---------------------
# 修改以下变量

# 0. 老的git地址前缀，必须使用ssh形式，本地配置好这个git地址的ssh访问
#   配合“repos.list”文件，每行一个repo地址【形式：groupname/reponame】
#   和此地址拼接形成完整的repo地址
_old_gitlab_ssh_prefix = "git@192.168.1.101"

# 1. 新的git的token，进入setting->access token --> 授权api、读写权限
headers = {
    "PRIVATE-TOKEN": "9fW86uqPVptKvY5HtzXN"
}

# 2. 新的git的组id和组名字，一定要对得上！目前仅支持一个组
_group_id = "7"
_group_name = "cs2"

# 3. 新的git地址
_gitlab_host = "192.168.1.101"
# _gitlab_url = "http://{}/api/v4/projects".format(_gitlab_host)
# -0-------------------------
