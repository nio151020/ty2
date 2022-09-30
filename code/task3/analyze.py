import os 
import json
import pandas as pd

pred_paph = "./evaluate/preds_roberta-xlarge-q_e.json"  # ？？？？？
gold_path = "./evaluate/test_labels.json"  # ？？？？？
sys_path = "./dataset/cmdd/symptom_norm.csv"

with open(pred_paph, 'r', encoding='utf-8') as fr:
    pred_data = json.load(fr)

with open(gold_path, 'r', encoding='utf-8') as fr:
    gold_data = json.load(fr)

sys_n = pd.read_csv(sys_path)
sys_n = sys_n['norm'].tolist()
# print(sys_n[:5])

eids = list(gold_data.keys())
cnt = 0
cnt_all = 0

# for eid in eids:
#     gold_type = gold_data[eid]

#     for k, v in gold_type.items():
#         cnt_all += 1
#         if k not in sys_n:
#             print(k)
#             cnt += 1
          

# print(cnt_all, cnt)

for eid in eids:
    pred_type = pred_data[eid]
    gold_type = gold_data[eid]

    for k, v in pred_type.items():
        cnt_all += 1
        if k not in gold_type:
            print(eid, k)
            cnt += 1
            if cnt > 8:
                sys
          

print(cnt_all, cnt)



