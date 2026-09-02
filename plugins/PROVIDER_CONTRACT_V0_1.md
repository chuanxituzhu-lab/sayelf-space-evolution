# Space Core Provider / Adapter Contract v0.1

## Boundary

Provider 只能消费 Canonical Space Model 并返回结果/计划；不能改变 `schema_version`、解释五锁、重新布局空间、提升证据等级或偷偷调用外部服务。

## Minimal Python contract

```python
class ProviderContract(Protocol):
    provider_id: str

    def manifest(self) -> dict: ...
    def can_execute(model: CanonicalSpaceModel, operation: str) -> ValidationReport: ...
    def execute(model: CanonicalSpaceModel, operation: str = "plan") -> ExecutionResult: ...
```

## Manifest

```yaml
id: native.local
type: native_provider
version: 0.1.0
capabilities:
  - canonical_model
  - validate
  - execution_plan
  - build_prompts
interfaces:
  - python
  - cli-compatible
requires_auth: false
external_calls: false
```

未来 `image_provider`、`video_provider`、`cad_provider`、`bim_provider` 必须声明能力、版本、认证要求和是否外传数据。Core 默认选择 `native.local`；可选 Provider 缺失时不能阻断 Canonical Model、锁校验和本地执行计划。

## Required safety behavior

1. 执行前调用 `model.validate()`。
2. 五锁任一为 `unlocked` 或 `stale` 时返回 `blocked`，不生成外部任务。
3. 资产必须携带 `spatial_dna_version`、父资产、Prompt、五锁快照、Provider 和 revision。
4. 外部 Provider 不得接收未授权的本地原图、图纸、客户数据、凭据或未知数据。
5. Provider 生成失败、能力不足或锁漂移时返回可审计错误，不能用猜测结果冒充事实。

## Native Provider v0.1

`native.local` 是零插件默认实现，支持 `validate`、`plan`、`build_prompts`。它只做本地模型校验、执行计划和原有六阶段 Prompt 资产编排，不伪造 CAD/BIM、图像、视频或第三方软件输出。
