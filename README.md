# lingmo-release

Lingmo OS 发行版身份文件包。用于替代 Fedora 的 `fedora-release`，定义系统的操作系统身份（`/etc/os-release`、`/etc/issue`、`/etc/system-release` 等），并**覆盖（Obsoletes）Fedora 的 release 包**，防止 Fedora 的身份信息残留或被篡改。

## 为什么需要这个包

Fedora 基础镜像自带 `fedora-release` 包，它提供：

- `/etc/os-release` → `NAME="Fedora Linux"`
- `/etc/issue` / `/etc/issue.net` → Fedora 登录提示
- `/etc/system-release`、`/etc/redhat-release`
- `/etc/system-release-cpe`
- `/usr/lib/rpm/macros.d/macros.dist` → `%dist .fcXX`

如果不替换它，构建出来的 LingmoOS 系统里会到处显示 "Fedora Linux"，并且后续包的 RPM `%dist` 标签也会是 `.fc45` 而不是 `.lingmo5`。`lingmo-release` 就是用来把这些身份信息全部替换成 Lingmo OS。

## 提供的文件

| 路径 | 内容 |
|---|---|
| `/usr/lib/os-release`（`/etc/os-release` → 符号链接） | `NAME="Lingmo OS"`, `VERSION_ID=5`, `ID=lingmo` 等 |
| `/usr/lib/issue`、`/usr/lib/issue.net` | `Lingmo OS 5 (Unstable)` 登录提示 |
| `/usr/lib/lingmo-release`（`/etc/lingmo-release`） | `Lingmo OS release 5 (Unstable)` |
| `/etc/redhat-release` → `lingmo-release` | 兼容旧工具 |
| `/etc/system-release` → `lingmo-release` | 发行版标识 |
| `/usr/lib/system-release-cpe` | `cpe:/o:lingmo:lingmo:5` |
| `/usr/lib/rpm/macros.d/macros.dist` | `%dist` → `.lingmo5` |

## 如何覆盖 Fedora（防篡改）

spec 中通过以下声明实现替换：

```spec
Provides:  fedora-release = %{version}
Provides:  fedora-release-common = %{version}
Provides:  fedora-release-identity-basic = %{version}
Obsoletes: fedora-release < 100
Obsoletes: fedora-release-common < 100
Obsoletes: fedora-release-identity-basic < 100
Obsoletes: fedora-release-identity-wsl < 100
Conflicts: fedora-release
```

- `Obsoletes` 确保安装 `lingmo-release` 时，Fedora 的 release 包被自动卸载替换。
- `Provides` 保证任何 `Requires: fedora-release` 的包依赖仍能解析。
- `Conflicts` 防止两者同时存在。

## 构建

```bash
# 本地
rpmdev-setuptree
cp lingmo-release.spec ~/rpmbuild/SPECS/
cp os-release issue issue.net LICENSE ~/rpmbuild/SOURCES/
cd ~/rpmbuild/SPECS
dnf builddep -y lingmo-release.spec
rpmbuild -ba --nocheck lingmo-release.spec
```

产出：`lingmo-release-5-1.lingmo5.noarch.rpm`（SRPM 和二进制 RPM）。

GitHub Actions 会在 push 到 `main` 时自动构建并发布 release（见 `.github/workflows/build-release.yml`）。

## 文件清单

| 文件 | 说明 |
|---|---|
| `lingmo-release.spec` | RPM 打包规格 |
| `os-release` | 系统身份（Source1） |
| `issue` | 本地登录提示（Source2） |
| `issue.net` | 网络登录提示（Source3） |
| `LICENSE` | MIT 许可证（Source4） |
| `.github/workflows/build-release.yml` | 自动构建 + 发布 |

## 后续（ISO 构建会用到的关联包）

- `grub2` 系列：引导加载器（grub2-common / grub2-efi-x64 / grub2-tools）
- `plymouth` 系列：开机动画（plymouth / plymouth-core-libs / plymouth-theme-*）
- `kernel-core` / `dracut` / `systemd` / `NetworkManager`：系统核心
- `lorax` / `livecd-tools` / `xorriso` / `squashfs-tools`：ISO 构建工具
