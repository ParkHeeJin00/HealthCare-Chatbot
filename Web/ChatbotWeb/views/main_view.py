from flask import Blueprint, render_template, request, jsonify
import torch
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast

bp = Blueprint('main', __name__, url_prefix='/')


def chatbot(q):
    # 스페셜 토큰 정의
    Q_TKN = "<usr>"
    A_TKN = "<sys>"
    BOS = "</s>"
    EOS = "</s>"
    SENT = '<unused1>'
    PAD = "<pad>"
    MASK = "<unused0>"
    # 사전학습된 토크나이저
    TOKENIZER = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2", bos_token=BOS, eos_token=EOS, unk_token="<unk>", pad_token=PAD, mask_token=MASK)

    model = GPT2LMHeadModel.from_pretrained("skt/kogpt2-base-v2")


    with torch.no_grad():
        while 1:
            q = input("user > ").strip()
            if q == "quit":
                break
            a = ""
            while 1:
                input_ids = torch.LongTensor(TOKENIZER.encode(Q_TKN + q + SENT + A_TKN + a)).unsqueeze(dim=0)
                print(input_ids)
                pred = model(input_ids)
                pred = pred.logits
                gen = TOKENIZER.convert_ids_to_tokens(torch.argmax(pred, dim=-1).squeeze().numpy().tolist())[-1]
                if gen == EOS:
                    break
                a += gen.replace("▁", " ")
            print("Chatbot > {}".format(a.strip()))

    return a.strip()


@bp.route('/chat', methods=['POST'])
def chat():
    if request.method == 'POST':
        q = request.form.get('message_input')  # 클라이언트로부터 받은 데이터에서 message_input 키를 가져옴
        if q:
            a = chatbot(q)  # chatbot 함수를 호출하여 답변을 얻음
            return jsonify({'answer': a})  # 클라이언트에게 답변을 JSON 형식으로 반환
        else:
            return jsonify({'answer': '죄송합니다. 요청된 데이터가 올바르지 않습니다.'}), 400  # 요청된 데이터가 없을 경우 400 에러 반환
    else:
        return jsonify({'answer': '죄송합니다. 잘못된 요청입니다.'}), 405  # POST 메소드가 아닌 경우 405 에러 반환