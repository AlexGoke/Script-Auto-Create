# Script-Auto-Create  自动生成脚本工具
# 更新时间：2020.10.08
#           2020.11.14
#           2021.05.15


# 使用方法：

## 1. 打开要生成脚本的excel，进行如下修改：
1. 替换 测试工具的参数中英文表达：seekpct= , rdpct=, xfersize=, thread=, runtime= ...
   (注意：测试工具信息参数 当前都写在了测试步骤内容中，之后调整到“测试场景” [2021-05-15])

2. 修改excel中的“测试场景”信息, 规则为：
        excel中测试场景书写规范：
      1. 第一行为环境信息：控制器编号(可不写，默认0), 控制器接口信息(X2 or X4)
      2. 第二行为pd信息：
         1. 不同种盘用';'分隔 
         2. 同一种盘信息表示为：sata_ssdx1
         3. 最后一种盘结尾不要带';'
         4. 之后增添多个vd并行, 每一种vd分行写 [2021-05]
      3. 第三行为vd信息： type=raid1 count=1 strip=1024k;
      4. 第四行为IO信息：[暂无规范]
---

## 2. 打开生成器 “script_builder.py"

根据提示步骤，选择或设置5部分内容：

1. 设置 本次生成脚本用的excel路径名称：将具体excel文件拖入该文件所在路径，到script_create文件 70行，修改自己要用的 excel文件名
2. 设置 作者\时间

3. 选择 脚本注释信息、import内容 （若没有，在template中自行仿照创建 路径：./template）

[2020-11]

4. 选择 物理盘参数 内容模板（若没有，自行仿照创建）
5. 选择 虚拟盘参数 内容模板（若没有，自行仿照创建）
6. 选择 测试工具参数 内容模板（若没有，自行仿照创建）

[2021-05]

4. 不用在设置 pd、vd、IO-tool 的任何内容，只要第一步excel按规则写好了，直接运行即可
---

## 3. 运行

1. 输入测试工具。 'v' 或者 'f' , 回车
2. 输入类名 or 不输入（自动从excel中获取类名，需excel中写好）
3. 输入需要生成的测试用例exceal行号。形式有两种：

    xxx：    代表生成该行一条测试脚本用例

    xxx-xxx: 代表生成该范围行的多条测试用例脚本（一般为同一个类名的一批脚本）


## 大功告成 ！！！


--- ------------------ ------------------------------

# 功能更新记录
## 2020.09.24
        1.  增加了自动填写类名的功能，需在excel同类名的一批脚本前一行第一列写入类名
            运行生成器，输入类名步骤可随意输入，之后会被覆盖；
            在输入行号范围时，从类名行所在行号为起始行
            运行即可
        2.  增加了自动适配excel功能，之后的excel更新直接放入路径下即可。不用考虑excel列内容不同的问题

## 2020.10.01
        增加了 脚本名称自动修改工具 auto-rename
        （为避免不必要的损失，可以将待重命名的脚本文件夹 复制出一个 XXX_rename.py）
        1.  将待重命名的脚本文件所在的目录 （xxx_rename）路径，写入程序
        2.  将具有重命名的目标名称信息的excel的绝对路径，写入程序
        3.  找出重命名的目标名称所在具体行号范围，写入脚本中
        4.  运行（根据结果中 “匹配成功”/“匹配失败” 可判断是否有效rename）

## 2020.11.14
        脚本生成工具的

## 2021.05.14
        完成了测试场景+物理盘信息+raid信息 的自动获取, 规范了excel的局部格式(测试场景)



