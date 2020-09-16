# Script-Auto-Create  自动生成脚本工具
# 更新时间：2020.09.15

# 使用方法：
根据测试用例需要创建的盘类型，选择相应的生成器子类subclass，运行
目前已有的三种生成器：jbod、raid、raid&jbod混组
如有另外需要，需创建新的生成器subclass
运行生成器，生成脚本后，将其拖入ps3test项目中运行测试。

# 生成器subclass使用方法：
以subclass_raid为例说明
修改
先根据要生成的用例，进行相应的 physical_disk、virtual_disk、 测试工具信息的修改
运行
需要根据提示输入：1. 输入测试工具。 'v' 或者 'f' ， 回车
                2. 输入脚本类名。 这个需要自行翻译，根据测试用例excel每一个大类翻译。回车
                   例如：BasicioRaid6RandomRead 基础io-raid6-随机读（11条子用例）
                3. 输入需要生成的测试用例exceal行号。形式有两种——————
                   xxx： 代表生成该行一条测试脚本用例
                   xxx-xxx: 代表生成该范围行的多条测试用例脚本（一般为同一个类名的一批脚本）

# 新增生成器子类subclass的方法：
分为两部分：在路径下
