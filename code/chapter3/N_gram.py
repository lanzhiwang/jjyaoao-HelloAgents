import collections

# 示例语料库, 与上方案例讲解中的语料库保持一致
corpus = "datawhale agent learns datawhale agent works"
tokens = (
    corpus.split()
)  # ['datawhale', 'agent', 'learns', 'datawhale', 'agent', 'works']
total_tokens = len(tokens)  # 6

# --- 第一步: 计算 P(datawhale) ---
count_datawhale = tokens.count("datawhale")  # 2
p_datawhale = count_datawhale / total_tokens  # 0.3333333333333333
print(f"第一步: P(datawhale) = {count_datawhale}/{total_tokens} = {p_datawhale:.3f}")

# --- 第二步: 计算 P(agent|datawhale) ---
# 先计算 bigrams 用于后续步骤
"""
>>> tokens[1:]
['agent', 'learns', 'datawhale', 'agent', 'works']
>>> bigrams = zip(tokens, tokens[1:])
>>> bigrams
<zip object at 0x7fab146bdcc0>
>>> for bigram in bigrams:
...    print(bigram)
...
('datawhale', 'agent')
('agent', 'learns')
('learns', 'datawhale')
('datawhale', 'agent')
('agent', 'works')
>>>
"""
bigrams = zip(tokens, tokens[1:])
bigram_counts = collections.Counter(bigrams)
count_datawhale_agent = bigram_counts[("datawhale", "agent")]  # 2
# count_datawhale 已在第一步计算
p_agent_given_datawhale = count_datawhale_agent / count_datawhale
print(
    f"第二步: P(agent|datawhale) = {count_datawhale_agent}/{count_datawhale} = {p_agent_given_datawhale:.3f}"
)

# --- 第三步: 计算 P(learns|agent) ---
count_agent_learns = bigram_counts[("agent", "learns")]  # 1
count_agent = tokens.count("agent")  # 2
p_learns_given_agent = count_agent_learns / count_agent
print(
    f"第三步: P(learns|agent) = {count_agent_learns}/{count_agent} = {p_learns_given_agent:.3f}"
)

# --- 最后: 将概率连乘 ---
p_sentence = p_datawhale * p_agent_given_datawhale * p_learns_given_agent
print(
    f"最后: P('datawhale agent learns') ≈ {p_datawhale:.3f} * {p_agent_given_datawhale:.3f} * {p_learns_given_agent:.3f} = {p_sentence:.3f}"
)
