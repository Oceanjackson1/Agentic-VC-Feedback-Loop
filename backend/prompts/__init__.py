"""场景注册表：管理所有分析场景"""

from prompts import vc_pitch, ecommerce_b2b, interview, meeting_summary

# 场景 ID → 场景模块的映射
SCENARIOS = {
    vc_pitch.SCENARIO_ID: vc_pitch,
    ecommerce_b2b.SCENARIO_ID: ecommerce_b2b,
    interview.SCENARIO_ID: interview,
    meeting_summary.SCENARIO_ID: meeting_summary,
}


def get_scenario(scenario_id: str):
    """获取场景模块，不存在则抛出 ValueError"""
    if scenario_id not in SCENARIOS:
        valid = ", ".join(SCENARIOS.keys())
        raise ValueError(f"不支持的场景: {scenario_id}，可选: {valid}")
    return SCENARIOS[scenario_id]


def get_all_scenarios_meta() -> list[dict]:
    """返回所有场景的元数据列表"""
    result = []
    for sid, mod in SCENARIOS.items():
        meta = dict(mod.SCENARIO_META)
        meta["id"] = sid
        result.append(meta)
    return result
