import os
import json
import requests
import subprocess
import shutil
import stat

# 1. 读取repos.list文件
# 2. 下载repo
# 3. 在新的gitlab中创建对应项目
# 4. 上传到新的gitlab

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


# def delete():
#     response = requests.get(_gitlab_url, headers=headers)
#     tmp = json.loads(response.text)
#     for i in tmp:
#         project_name = i["name"]
#         requests.delete("http://192.168.1.101/api/v4/projects/myscan-master%2f{}".format(project_name), headers=headers)

def create_project(group_id, group_name, project_name):
    fromdata = {
        "namespace_id": group_id,
        "name": project_name,
    }
    prj_url = "http://" + _gitlab_host + "/api/v4/projects"
    r = requests.post(prj_url, data=fromdata, headers=headers)
    print("create project message:", r.status_code,  r.text)
    
    obj = json.loads(r.text)
    ok = False
    if r.status_code == 201:
        ok = True
    elif r.status_code == 400:
        if "name" in obj["message"] and obj["message"]["name"][0] == "has already been taken":
            ok = True

    if ok:
        ret = "git@{}:{}/{}.git".format(_gitlab_host, group_name, project_name)
        print("create project ssh-url:", ret)
        return ret
    else: 
        print("create project [{}/{}] failed!".format(group_name, project_name))
        return ""

def read_projects_file(path):
    file_object = open(path)
    ret = []
    try:
        file_context = file_object.read() 
        lines = file_context.splitlines()
        # print(lines)
        for l in lines:
            l = "".join(l.split())
            items = l.split('/')
            if len(items) == 2:
                ret.append({
                    "url": "{}:{}.git".format(_old_gitlab_ssh_prefix, l),
                    "name": "{}_{}".format(items[0], items[1])
                })
            else:
                print("project list line error:", l)
    finally:
        file_object.close()
    return ret

#filePath:文件夹路径
def delete_path(filePath):
    if os.path.exists(filePath):
        for fileList in os.walk(filePath):
            for name in fileList[2]:
                os.chmod(os.path.join(fileList[0],name), stat.S_IWRITE)
                os.remove(os.path.join(fileList[0],name))
        shutil.rmtree(filePath)
        return True
    else:
        return False

def checkout_git_repo(url, local_path):
    r_check_src = ""
    if os.path.exists(local_path):
        print("path exist, pull it")
        r_check_src = subprocess.call("cd {} && git pull --all".format(local_path), shell=True)
        if r_check_src != 0: 
            if delete_path(local_path):
                checkout_git_repo(url, local_path)
    else:
        print("path not exist, clone")
        r_check_src = subprocess.call("git clone {} {}".format(url, local_path), shell=True)

    # print("--->", r_check_src)
    if r_check_src != 0:
        print("copy repo: checkout [{}] failed:{}".format(url, r_check_src))
        return False
    return True

def copy_git_repos(src, dst_group_id, dst_group_name):
    print("copy repo:[{}] ===> [git@{}:{}/{}.git]".format(src["url"], _gitlab_host, dst_group_name, src["name"]))
    # 签出源repo
    local_path = "./{}".format(src["name"])
    if not checkout_git_repo(src["url"], local_path):
        print("copy repo: checkout [{}] failed!".format(src["url"]))
        return False

    # 创建新的repo
    ssh_url = create_project(dst_group_id, dst_group_name, src["name"])
    if len(ssh_url) < 10:
        print("copy repo: create new repo failed:")
        return False

    # 上传本地
    subprocess.call("./mvgit.sh {} {} ".format(local_path, ssh_url), shell=True)

if __name__ == '__main__':
    # create_project("5", "cs", "test3")
    repos = read_projects_file("./repos.list")
    print(repos)
    for repo in repos:
        copy_git_repos(repo, _group_id, _group_name)
            
