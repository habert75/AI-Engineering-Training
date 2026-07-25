from datasets import load_dataset


dataset_name = "Open-Orca/SlimOrca"

# https://huggingface.co/datasets/Open-Orca/SlimOrca

# ----------------------------
# Load dataset
# ----------------------------
dataset = load_dataset(dataset_name)
print(dataset)

# OUTPUT:
# DatasetDict({
#     train: Dataset({
#         features: ['conversations'],
#         num_rows: 517982
#     })
# })

# ----------------------------
# PRINT 100 ROWS IN DATASET
# ----------------------------
dataset = load_dataset(dataset_name)
print(dataset["train"][:2])

# OUTPUT:
# {
#     "conversations": [
#         [
#             {
#                 "from": "system",
#                 "value": "You are an AI assistant. You will be given a task. You must generate a detailed and long answer.",
#                 "weight": 0,
#             },
#             {
#                 "from": "human",
#                 "value": "Write an article based on this  man has been charged with murder and attempted murder after a woman and the man she was on a date with were stabbed at a restaurant in Sydney, Australia.",
#                 "weight": 0.0,
#             },
#             {
#                 "from": "gpt",
#                 "value": "Title: Tragedy Strikes in Sydney: Victims Stabbed during Dinner Date, Suspect Charged with Murder and Attempted Murder\n\nIntroduction\n\nA seemingly ordinary evening took a tragic turn in Sydney, Australia when a romantic dinner date at a local restaurant ended in bloodshed, as a man allegedly attacked a couple, stabbing both victims. Local authorities have charged the suspect with murder and attempted murder in connection with the horrific crime. In this article, we delve into the chilling incident, the suspect, and the impact it has had on the community.\n\nThe Incident\n\nThe alarming event took place at a popular restaurant in Sydney, Australia. A woman and her date were enjoying their meal – blissfully unaware of the tragic circumstances that would soon unfold. As they shared conversation and indulged in their dinner, a man approached the couple and, without warning, began to stab them with a sharp object.\n\nPatrons at the restaurant scrambled for safety, as the assailant continued his violent rampage. Bystanders quickly called emergency services, who promptly arrived at the scene. Although both victims were rushed to a nearby hospital, the woman succumbed to her injuries. The man she was on a date with remained in critical condition, fighting for his life.\n\nThe Suspect\n\nInitial investigations revealed that the alleged attacker had no known connections to the victims – adding to the mystifying nature of this sudden and brutal assault. Witnesses reported that the assailant seemed to have no specific motive and appeared to carry out the act senselessly.\n\nFollowing a thorough investigation, local police identified and arrested the suspect. During the process, it was discovered that the alleged attacker had a history of criminal behavior and a troubled past, though it is unclear if this played a role in the tragic incident.\n\nAuthorities have formally charged the man with murder and attempted murder in connection with the heinous crime. He awaits a hearing to determine a trial date and, if convicted, could face a life sentence in prison.\n\nThe Community's Response\n\nThe shocking nature of the crime has left the residents of Sydney reeling, as they struggle to come to terms with the harrowing event. The restaurant where the attack occurred has since been closed, with a makeshift memorial being created outside to commemorate the victims.\n\nMany have questioned how such a vicious crime could happen in what is considered to be one of the safest cities in the world. This tragic event has spurred local officials to reassess current security measures and devise strategies to reinforce public safety. Additionally, discussions surrounding mental health and criminal rehabilitation have surfaced as residents seek to comprehend the actions of the alleged perpetrator and prevent similar incidents from occurring in the future.\n\nIn the wake of the stabbing, the community has banded together with an outpouring of grief and support for the victims and their families. Candlelight vigils have been held, and an online fundraising campaign is underway to assist the surviving victim with his medical expenses and recovery.\n\nConclusion\n\nThe tragic attack in Sydney serves as a chilling reminder that senseless acts of violence can happen anywhere and at any time. The community's response to this horrific and seemingly random act of brutality has been one of solidarity and determination to prevent such incidents in the future. As the case unfolds, the victims and their families remain in the hearts of the community, who are grieving the devastating loss of a life cut tragically short and supporting the recovering victim as he continues to endure this unimaginable ordeal.",
#                 "weight": 1.0,
#             },
#         ],
#         [
#             {
#                 "from": "system",
#                 "value": "You are an AI assistant that follows instruction extremely well. Help as much as you can.",
#                 "weight": 0,
#             },
#             {
#                 "from": "human",
#                 "value": "Answer the following question: - number is 54    - debutteam is pittsburgh steelers    - draftpick is 166      - birth date is 24 may 1982    - weight is 243    - nfl is wal475737    - debutyear is 2005    - finalteam is new york sentinels    - statlabel is tackles sacks interceptions    - heightin is 3    - statvalue is 9 0.0 1    - heightft is 6    - college is temple    - birth place is pottstown , pennsylvania    - draftyear is 2005    - position is linebacker    - draftround is 5    - finalyear is 2009    Given the details above, guess who could this information be about.\nAnswer:",
#                 "weight": 0.0,
#             },
#             {
#                 "from": "gpt",
#                 "value": "The information provided seems to OUTPUTrefer to Rian Wallace, a former NFL player.",
#                 "weight": 1.0,
#             },
#         ],
#     ]
# }
