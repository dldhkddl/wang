"""
YouTube Shorts SEO 점수 분석 (축약 버전)
"""
import ollama
import re


def get_seo_evaluation_prompt(script: str) -> str:
    return f"""
You are a YouTube Shorts SEO Expert Analyst.

[SCRIPT TO ANALYZE]:
{script}

Rate each metric from 0-100 and follow this EXACT markdown:

## 📊 SEO Score Analysis

### 🎯 Overall Score: **[NN/100]**

---

1. ⏱️ **Watch Time Retention**: [NN/100]
2. 🔄 **Rewatch Rate**: [NN/100]
3. 🔍 **Search Intent Alignment**: [NN/100]
4. 🌐 **GEO Semantic Structure**: [NN/100]
5. 🎣 **Hook Power**: [NN/100]
6. 💬 **User Engagement**: [NN/100]
7. ✅ **AI Slop Filter**: [NN/100]

Rules:
- Replace every `NN` with an integer 0–100.
- Keep emojis, bold, brackets, order exactly the same.
- No extra text or explanations.
"""


def analyze_seo_score(script: str) -> str:
    prompt = get_seo_evaluation_prompt(script)
    res = ollama.chat(
        model="gemma3:latest",
        messages=[{"role": "user", "content": prompt}],
    )
    analysis = res["message"]["content"]

    # [NN/100] 패턴에서 숫자만 추출 (공백 허용)
    nums = re.findall(r'\[\s*(\d{1,3})\s*/\s*100\s*\]', analysis)
    if len(nums) < 7:
        return analysis  # 점수 7개 못 찾으면 그냥 리턴

    last7 = [int(n) for n in nums[-7:]]
    avg = max(0, min(100, round(sum(last7) / 7)))

    # Overall Score 라인에 평균 덮어쓰기 (없으면 그대로 둠)
    analysis = re.sub(
        r'Overall Score: \*\*\[\s*\d{1,3}\s*/\s*100\s*\]\*\*',
        f'Overall Score: **[{avg}/100]**',
        analysis,
    )

    return analysis