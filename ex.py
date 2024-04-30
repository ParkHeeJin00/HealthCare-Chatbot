class ChatbotDataset(Dataset):
    def __init__(self, DF, tokenizer):
        self.data = DF
        self.questions = DF['question'].values
        self.answers = DF['answer'].values
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        question = self.questions[idx]
        answer = self.answers[idx]
        tokenizer = self.tokenizer

        # 질문과 답변을 토큰화하고 오프셋 계산
        q_tokens = tokenizer.tokenize(question)
        a_tokens = tokenizer.tokenize(answer)

        # 토큰을 인덱스로 변환
        q_input = tokenizer.convert_tokens_to_ids(q_tokens)
        a_input = tokenizer.convert_tokens_to_ids(a_tokens)

        # 오프셋 계산
        q_offsets = [(0, 0)] * len(q_input)
        a_offsets = [(0, 0)] * len(a_input)

        return q_input, q_offsets, a_input, a_offsets


def collate_fn(batch):
    # 배치 처리를 위한 리스트 초기화
    q_inputs, q_offsets, a_inputs, a_offsets = [], [], [], []

    for item in batch:
        # 배치의 각 요소에서 데이터 추출
        q_input, q_offset, a_input, a_offset = item
        # 리스트에 추가
        q_inputs.append(q_input)
        q_offsets.append(q_offset)
        a_inputs.append(a_input)
        a_offsets.append(a_offset)

    # 리스트를 텐서로 변환
    return {
        'q_inputs': torch.tensor(q_inputs),
        'q_offsets': torch.tensor(q_offsets),
        'a_inputs': torch.tensor(a_inputs),
        'a_offsets': torch.tensor(a_offsets)
    }
