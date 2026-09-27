# AutoTable（org.dromara.autotable）使用文档

适用范围：`yudao-cloud` 下所有 `yudao-module-*-server` 微服务模块，以及聚合了全部模块的 `yudao-server` 单体应用。

## 1. 是什么、解决什么问题

AutoTable 是根据 MyBatis-Plus 实体类（`@TableName` 标注的 DO）自动生成/校验数据库表结构的库。本项目通过两种方式接入：

- **配置文件**：每个模块的 `application.yaml` 里的 `auto-table:` 配置块
- **注解**：模块启动类（`XxxServerApplication`）上的 `@EnableAutoTable`

## 2. 核心配置项（`application.yaml`）

统一模板（各模块 `model-package` 不同，其余字段保持一致）：

```yaml
auto-table:
  enable: true
  mode: update            # 自动建表/更新表结构。validate 仅只读校验，表不存在会直接抛异常导致启动失败
  model-package: cn.iocoder.yudao.module.<模块名>.dal.dataobject
  show-banner: false
  strict-extends: false   # 放宽对继承字段（BaseDO/TenantBaseDO 等父类字段）的严格校验，父类字段需要配合 @AutoColumn 才能被正确识别生成
  auto-drop-table: false
  auto-drop-column: false
  mysql:
    table-default-charset: utf8mb4
    table-default-collation: utf8mb4_unicode_ci
  pgsql:
    pk-auto-increment-type: byDefault
```

`mode` 取值说明：
- `validate`：只读校验，表不存在直接 `throw RuntimeException("启动失败，%s中不存在表%s")`，不会建表。仅适合表结构已经手工建好、只想做一致性检查的环境。
- `update`：表不存在则建表，存在则按需增列/改列（不会因为 `auto-drop-table`/`auto-drop-column: false` 而删表删列）。项目当前统一用这个。

## 3.【关键规则】禁止在 `@EnableAutoTable` 注解里写死单模块包名

### 3.1 曾经踩过的坑

`yudao-server`（组合单体）启动类会这样扫描包：

```java
@SpringBootApplication(scanBasePackages = {"${yudao.info.base-package}.server", "${yudao.info.base-package}.module"})
```

`cn.iocoder.yudao.module` 这个扫描范围会把**所有业务模块自己的 `XxxServerApplication` 启动类**也一起扫描进同一个 Spring 容器——因为它们全部位于 `cn.iocoder.yudao.module.<模块名>` 包下，而且每个都标了 `@SpringBootApplication` + `@EnableAutoTable`。

结果就是单体启动时，同一个进程里同时存在 **22 个 `@EnableAutoTable` 声明**（21 个模块各自的 + `yudao-server` 自己的）。AutoTable 对这个注解的处理是全局、非累加的（后处理的会覆盖先处理的），谁写的 `basePackages` 越窄、越具体，一旦被"后处理"，就会导致其余模块的实体全部扫不到——实测出现过"只有 iot 模块的字段被检查，其他模块完全没有 AutoTable 活动"的情况。

### 3.2 规则

**模块启动类（`XxxServerApplication`）上的 `@EnableAutoTable` 不要配置 `basePackages`（保持裸注解 `@EnableAutoTable`，或干脆不加）**，扫描范围统一交给配置文件的 `auto-table.model-package` 决定。

如果确实需要在注解上配置（比如某些历史原因无法即时改造），**必须统一写成覆盖全部模块的通配符**，不要写本模块的窄包名：

```java
@EnableAutoTable(basePackages = {"cn.iocoder.yudao.module.**.dal.dataobject"})
```

这样即使多个 `@EnableAutoTable` 同时出现在一个 Spring 容器里，它们的值也是完全一致的，不存在"谁覆盖谁、少扫了哪个模块"的问题。

> 目前 `yudao-module-iot`、`yudao-module-wms` 的启动类上还各自写死了 `basePackages = "cn.iocoder.yudao.module.iot.dal.dataobject"` / `"...wms.dal.dataobject"`，属于历史遗留的反例，应改成裸注解或统一通配符。

### 3.3 配置文件里的写法

**单模块独立部署**（微服务模式）：`model-package` 用本模块自己的包即可，不涉及多模块冲突：

```yaml
auto-table:
  model-package: cn.iocoder.yudao.module.wms.dal.dataobject
```

**组合单体部署**（`yudao-server`，`application-local.yaml`）：必须用能覆盖全部模块的写法，二选一：

```yaml
# 写法一：通配符（推荐，新增模块无需再改这里）
auto-table:
  model-package:
    - cn.iocoder.yudao.module.**.dal.dataobject

# 写法二：显式列出全部模块包（新增模块必须同步维护这份列表）
auto-table:
  model-package:
    - cn.iocoder.yudao.module.ai.dal.dataobject
    - cn.iocoder.yudao.module.bpm.dal.dataobject
    - cn.iocoder.yudao.module.crm.dal.dataobject
    - cn.iocoder.yudao.module.erp.dal.dataobject
    - cn.iocoder.yudao.module.fms.dal.dataobject
    - cn.iocoder.yudao.module.hrm.dal.dataobject
    - cn.iocoder.yudao.module.im.dal.dataobject
    - cn.iocoder.yudao.module.infra.dal.dataobject
    - cn.iocoder.yudao.module.iot.dal.dataobject
    - cn.iocoder.yudao.module.member.dal.dataobject
    - cn.iocoder.yudao.module.mes.dal.dataobject
    - cn.iocoder.yudao.module.mp.dal.dataobject
    - cn.iocoder.yudao.module.oa.dal.dataobject
    - cn.iocoder.yudao.module.pay.dal.dataobject
    - cn.iocoder.yudao.module.pms.dal.dataobject
    - cn.iocoder.yudao.module.product.dal.dataobject
    - cn.iocoder.yudao.module.promotion.dal.dataobject
    - cn.iocoder.yudao.module.report.dal.dataobject
    - cn.iocoder.yudao.module.statistics.dal.dataobject
    - cn.iocoder.yudao.module.system.dal.dataobject
    - cn.iocoder.yudao.module.trade.dal.dataobject
    - cn.iocoder.yudao.module.wms.dal.dataobject
```

优先用写法一（通配符），维护成本更低；写法二仅在需要精确控制扫描范围（比如临时排除某个模块）时使用。

**核心原则：注解优先级高于配置文件、越具体的配置越容易在多模块合并场景下"误伤"其它模块，所以能不写在注解上就不写，写的话必须和其它地方保持一致（通配符）。**

## 4. 继承字段（BaseDO / TenantBaseDO）注意事项

`creator`/`createTime`/`updater`/`updateTime`/`deleted`/`tenantId` 这些字段定义在 `BaseDO`/`TenantBaseDO` 基类上，AutoTable 默认可能识别不到父类字段或类型推断不准，需要：

1. 在基类字段上显式加 `@AutoColumn`/`@AutoColumns`（而不是只依赖 MyBatis-Plus 的 `@TableField`/`@TableLogic`）
2. 配置里加 `strict-extends: false`，放宽继承字段的严格校验

两者需要同时满足，缺一个都可能导致基类字段没有被生成到表结构里。

## 5. 排查清单

启动后发现"某个模块的表没有被自动建/检查"，按下面顺序排查：

1. 确认该模块的 `application.yaml` 里 `auto-table.enable: true` 且 `mode: update`
2. 确认 `model-package` 指向的包路径真实存在（用 `${yudao.info.base-package}` 占位符时，先确认它在当前文件里实际解析出的值，避免拼接出不存在的重复路径）
3. 如果是**单体聚合模式**（`yudao-server`）启动的，检查是否有多个 `@EnableAutoTable`（尤其是模块启动类上写死了窄 `basePackages`）互相覆盖——按第 3 节规则改成裸注解或统一通配符
4. 基类字段缺失，按第 4 节检查 `@AutoColumn` 和 `strict-extends`
