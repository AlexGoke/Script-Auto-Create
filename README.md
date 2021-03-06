# Script-Auto-Create  自动生成脚本工具
# 更新时间：2020.10.08
#           2020.11.14

# 使用方法：

~~根据测试用例需要创建的盘类型，选择相应的生成器子类subclass，运行~~

~~目前已有的三种生成器：jbod、raid、raid&jbod混组~~

~~如有另外需要，需创建新的生成器subclass~~

~~运行生成器，生成脚本后，将其拖入ps3test项目中运行测试。~~


## 设置

打开要生成脚本的excel，进行如下修改：
1. 替换 测试工具的参数中英文表达：seekpct rdpct xfersize


打开生成器 “script_builder"

根据提示步骤，选择或设置5部分内容：

1. 设置 本次生成脚本用的excel路径名称
2. 设置 作者时间
3. 选择 脚本注释信息、import内容 （若没有，在template中自行仿照创建 路径：./template）
4. 选择 物理盘参数 内容模板（若没有，自行仿照创建）
5. 选择 虚拟盘参数 内容模板（若没有，自行仿照创建）

运行

## 运行

1. 输入测试工具。 'v' 或者 'f' , 回车

~~2. 输入脚本类名。 这个需要自行翻译，根据测试用例excel每一个大类翻译。回车~~

~~例如：BasicioRaid6RandomRead 基础io-raid6-随机读（11条子用例）~~

2. 输入类名 or 不输入（自动从excel中获取类名，需excel中写好）
3. 输入需要生成的测试用例exceal行号。形式有两种：

    xxx：    代表生成该行一条测试脚本用例

    xxx-xxx: 代表生成该范围行的多条测试用例脚本（一般为同一个类名的一批脚本）


* * *

~~# 生成器subclass使用方法：~~

~~以subclass_raid为例说明~~

## 设置

1. （若需要指定excel）将具体excel文件拖入该文件所在路径，到script_create文件 70行，修改自己要用的 excel文件名
2. 到相应生成器对应的模板template文件里, 修改“作者名”<author.>, “日期”  <year.month.day>
3. 根据要生成的用例，进行相应的 physical_disk、virtual_disk、 test_tool 参数信息的修改



~~# 新增生成器子类subclass的方法：~~


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
