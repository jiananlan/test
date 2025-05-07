import os
import subprocess
import sys

def run(cmd, env=None):
    print(f"\n=> 正在执行: {cmd}\n")
    proc = subprocess.run(cmd, shell=True, env=env)
    if proc.returncode != 0:
        print(f"\n命令失败: {cmd}\n")
        sys.exit(proc.returncode)
    return proc

def get_gcc_version():
    try:
        output = subprocess.check_output("gcc --version", shell=True).decode()
        for line in output.splitlines():
            if line.startswith("gcc"):
                versionstr = line.split()[-1]
                return versionstr.strip()
    except Exception:
        return None
    return None

def check_gfortran9():
    try:
        output = subprocess.check_output("gfortran-9 --version", shell=True).decode()
        if "Fortran" in output:
            return True
    except Exception:
        return False
    return False

def install_gfortran9():
    print("\n=> 检查 gfortran-9 是否已安装...")
    if check_gfortran9():
        print("gfortran-9 已安装。")
        return

    # 更新 APT 并安装 gfortran-9
    print("未检测到 gfortran-9，正在安装...")
    # 有些 Ubuntu 版本需要添加 toolchain PPA
    run("sudo apt-get update")
    res = subprocess.call("apt-cache policy gfortran-9", shell=True)
    if res != 0:
        print("gfortran-9 不在默认仓库，尝试添加 PPA...")
        run("sudo apt-get install -y software-properties-common")
        run("sudo add-apt-repository ppa:ubuntu-toolchain-r/test -y")
        run("sudo apt-get update")
    run("sudo apt-get install -y gfortran-9")
    run('sudo ln -sf $(which gfortran-9) /usr/bin/gfortran')
    if check_gfortran9():
        print("gfortran-9 安装成功。")
    else:
        print("gfortran-9 安装失败，请检查错误信息。")

def uninstall_install_gcc9():
    print('\n检测并处理gcc/g++版本...\n')
    version = get_gcc_version()
    if not version or not version.startswith("9."):
        print('\n[警告] 当前GCC版本为: %s ，需要切换为gcc-9 ...\n' % (version if version else '未安装'))
        print('[自动操作] 卸载旧gcc，并安装gcc-9和g++-9（需要sudo权限）...\n')

        # 可能需要保留其它程序依赖的版本，你可按需调整用于完整卸载
        run("sudo apt-get update")
        # 卸载当前gcc/g++
        run("sudo apt-get -y remove --purge gcc g++")
        # 安装gcc-9 g++-9
        run("sudo apt-get -y install gcc-9 g++-9")
        # 配置默认gcc为9
        run("sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 90")
        run("sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 90")
        # 可选：如果之前存在gcc和g++其它替代方案，可用--set强制选择9
        run("sudo update-alternatives --set gcc /usr/bin/gcc-9")
        run("sudo update-alternatives --set g++ /usr/bin/g++-9")

        newver = get_gcc_version()
        if newver and newver.startswith("9."):
            print(f"\n[OK] 已自动切换到gcc-9，当前版本: {newver}\n")
        else:
            print(f"[错误] 自动换GCC-9失败，请手动处理！")
            sys.exit(12)
    else:
        print(f"[信息] 当前GCC已是9.x，无需更改。")

def extract_tar(tarfile, target):
    if not os.path.exists(target):
        os.makedirs(target)
    print(f"[解压] {tarfile} --> {target}")
    run(f"tar -xf {tarfile} -C {target} --strip-components=1")

def build_mpich(src, install_dir):
    os.chdir(src)
    run(f"./configure --prefix={install_dir} CC=gcc CXX=g++ FC=gfortran F77=gfortran")
    run("make -j$(nproc)")
    run("make install")
    os.chdir("..")

def build_hdf5(src, install_dir, mpich_bin):
    os.chdir(src)
    env = os.environ.copy()
    env['CC'] = f"{mpich_bin}/mpicc"
    run(f"./configure --prefix={install_dir} --enable-parallel --enable-fortran", env=env)
    run("make -j$(nproc)")
    run("make install")
    os.chdir("..")

def build_hypre(src, install_dir, mpich_bin):
    os.chdir(src)
    env = os.environ.copy()
    env["CC"] = f"{mpich_bin}/mpicc"
    run(f"./configure --prefix={install_dir} CC=mpicc CXX=mpic++ FC=mpif90 F77=mpif90", env=env)
    run("make -j$(nproc)")
    run("make install")
    os.chdir("..")

def extract_flash(tarfile):
    print(f"[解压] {tarfile} 到当前目录")
    run(f"tar -xf {tarfile} -C .")
    print("FLASH已解压，目录内容如下（部分）:")
    for f in os.listdir('.'):
        if f.lower().startswith("flash"):
            print("-", f)

def append_env_to_bashrc(mpich_install, hdf5_install, hypre_install):
    home = os.path.expanduser("~")
    bashrc = os.path.join(home, ".bashrc")
    env_text = f"""
# ==== FLASH/MPICH/HDF5/HYPRE 环境变量 for FLASH4.6.2 ====
export MPI_HOME={mpich_install}
export PATH=$MPI_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MPI_HOME/lib:{hdf5_install}/lib:{hypre_install}/lib:$LD_LIBRARY_PATH
export C_INCLUDE_PATH=$MPI_HOME/include:$C_INCLUDE_PATH
# ==== FLASH/MPICH/HDF5/HYPRE 环境变量 end ====
"""
    # 避免重复添加
    already = False
    if os.path.exists(bashrc):
        with open(bashrc, "r") as f:
            lines = f.readlines()
        if any("FLASH/MPICH/HDF5/HYPRE 环境变量" in line for line in lines):
            print(f"\n[信息] {bashrc} 中已经有相关环境变量，无需重复添加。\n")
            already = True
    if not already:
        with open(bashrc, "a") as f:
            f.write(env_text)
        print(f"\n[OK] 已写入环境变量到 {bashrc}。\n你需要运行：source ~/.bashrc 以便立即生效。\n")

def main():
    cwd = os.getcwd()
    mpich_tar = "mpich-3.2.tar.gz"
    hdf5_tar = "hdf5-1.8.12.tar.gz"
    hypre_tar = "hypre-2.9.0b.tar.gz"
    flash_tar = "FLASH4.6.2.tar.gz"
    # 检查包
    for fn in [mpich_tar, hdf5_tar, hypre_tar, flash_tar]:
        if not os.path.exists(fn):
            print(f"[缺少文件] {fn}, 请补全后重试。")
            sys.exit(10)

    # 尝试自动卸载并安装 gcc-9
    uninstall_install_gcc9()
    install_gfortran9()
    run('which gfortran')
    run('which gcc')
    run('gcc --version')
    run('gfortran --version')
    # 依赖解压、编译、安装
    print("\n#### 安装MPICH ####")
    mpich_src = "mpich_src"
    mpich_install = os.path.abspath("mpich_install")
    extract_tar(mpich_tar, mpich_src)
    build_mpich(mpich_src, mpich_install)

    print("\n#### 安装HDF5 ####")
    hdf5_src = "hdf5_src"
    hdf5_install = os.path.abspath("hdf5_install")
    extract_tar(hdf5_tar, hdf5_src)
    build_hdf5(hdf5_src, hdf5_install, mpich_install + "/bin")

    print("\n#### 安装HYPRE ####")
    hypre_src = "hypre_src"
    hypre_install = os.path.abspath("hypre_install")
    extract_tar(hypre_tar, hypre_src)
    build_hypre(hypre_src, hypre_install, mpich_install + "/bin")

    print("\n#### 解压FLASH预编译包 ####")
    extract_flash(flash_tar)

    print("\n========== 所有依赖已安装并配置环境变量 ==========")
    append_env_to_bashrc(mpich_install, hdf5_install, hypre_install)
    print("\n[说明]")
    print(" 1. 依赖库已自动安装，环境变量已加入.bashrc。建议手动执行: source ~/.bashrc")
    print(" 2. 若需运行FLASH，使用mpirun/mpiexec等命令。例如：")
    print("      mpirun -np 4 ./flash4")
    print(" 3. 如果FLASH可执行文件名称或运行方法不同，请参考供应者的文档及README。")
    print(" 4. 若出现找不到libmpi.so等错误，请确认.bashrc已生效，或手动export一次环境变量。")

if __name__ == "__main__":
    main()
