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

def check_gcc9():
    print("检查gcc版本...")
    try:
        output = subprocess.check_output("gcc --version", shell=True).decode()
        if "gcc" in output and " 9." in output.split("\n")[0]:
            print("已检测到gcc 9.x")
            return True
        else:
            print("[错误] 当前gcc不是9.x版本，请手动安装并切换到gcc-9")
            return False
    except:
        print("[错误] 未找到gcc，请手动安装gcc-9")
        return False

def extract_tar(tarfile, target):
    if not os.path.exists(target):
        os.makedirs(target)
    print(f"[解压] {tarfile} --> {target}")
    run(f"tar -xf {tarfile} -C {target} --strip-components=1")

def build_mpich(src, install_dir):
    os.chdir(src)
    run(f"./configure --prefix={install_dir}")
    run("make -j$(nproc)")
    run("make install")
    os.chdir("..")

def build_hdf5(src, install_dir, mpich_bin):
    os.chdir(src)
    env = os.environ.copy()
    env['CC'] = f"{mpich_bin}/mpicc"
    run(f"./configure --prefix={install_dir} --enable-parallel", env=env)
    run("make -j$(nproc)")
    run("make install")
    os.chdir("..")

def build_hypre(src, install_dir, mpich_bin):
    os.chdir(src)
    env = os.environ.copy()
    env["CC"] = f"{mpich_bin}/mpicc"
    run(f"./configure --prefix={install_dir} --with-MPI", env=env)
    run("make -j$(nproc)")
    run("make install")
    os.chdir("..")

def extract_flash(tarfile):
    # 假设FLASH为预编译版本，直接解压到当前目录
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
    flash_tar = "FLASH4.6.2.tar.gz"    # 预编译包
    # 检查包
    for fn in [mpich_tar, hdf5_tar, hypre_tar, flash_tar]:
        if not os.path.exists(fn):
            print(f"[缺少文件] {fn}, 请补全后重试。")
            sys.exit(10)
    # 检查gcc-9
    if not check_gcc9():
        sys.exit(11)
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
    print("1. 依赖库已自动安装，环境变量已加入.bashrc。建议手动执行: source ~/.bashrc")
    print("2. 若需运行FLASH，使用mpirun/mpiexec等命令。例如：")
    print("     mpirun -np 4 ./flash4")
    print("3. 如果FLASH可执行文件名称或运行方法不同，请参考供应者的文档及README。")
    print("4. 若出现找不到libmpi.so等错误，请确认.bashrc已生效，或手动export一次环境变量。")

if __name__ == "__main__":
    main()
