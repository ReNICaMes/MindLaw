from flask import Flask, request, render_template, jsonify
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import os
import json

app = Flask(__name__)

# Model ve tokenizer'ı yükleyin
tokenizer = AutoTokenizer.from_pretrained("renicames/t5-base-turkish-MindLaw")
model = AutoModelForSeq2SeqLM.from_pretrained("renicames/t5-base-turkish-MindLaw")

# Kullanıcı verilerini saklayacağımız JSON dosyasının yolu
current_directory = os.path.dirname(os.path.abspath(__file__))
users_data_file = os.path.join(current_directory, "users_data.json")

# JSON dosyasını yükleme veya oluşturma
def load_users_data():
    if os.path.exists(users_data_file):
        with open(users_data_file, 'r') as f:
            return json.load(f)
    else:
        return {"users": {}}

# JSON dosyasına kullanıcı verilerini kaydetme
def save_users_data(data):
    with open(users_data_file, 'w') as f:
        json.dump(data, f)

# Kullanıcı verilerini güncelleme
def update_user_data(user_id, new_question):
    users_data = load_users_data()
    if user_id not in users_data["users"]:
        users_data["users"][user_id] = {"questions": [], "context": ""}
    
    if not is_related(users_data["users"][user_id]["context"], new_question, users_data["users"][user_id]["questions"]):
        reset_user_data(user_id)
        users_data["users"][user_id]["context"] = new_question
    else:
        users_data["users"][user_id]["context"] = update_context(users_data["users"][user_id]["context"], new_question)
    
    users_data["users"][user_id]["questions"].append(new_question)
    save_users_data(users_data)

# Kullanıcı bağlamını güncelleme
def update_context(context, new_question):
    updated_context = context + " " + new_question
    return updated_context

# Model kullanarak metin benzerliğini hesaplama
def compute_similarity(text1, text2):
    inputs1 = tokenizer(text1, return_tensors='pt', truncation=True, padding=True, max_length=512)
    inputs2 = tokenizer(text2, return_tensors='pt', truncation=True, padding=True, max_length=512)
    
    with torch.no_grad():
        outputs1 = model.encoder(**inputs1)
        outputs2 = model.encoder(**inputs2)
    
    embeddings1 = outputs1.last_hidden_state.mean(dim=1)
    embeddings2 = outputs2.last_hidden_state.mean(dim=1)
    
    cosine_similarity = torch.nn.functional.cosine_similarity(embeddings1, embeddings2)
    return cosine_similarity.item()

# Soruların ilişkili olup olmadığını belirleme
def is_related(context, new_question, questions):
    if not context:
        return False
    
    similarities = [compute_similarity(q, new_question) for q in questions]
    average_similarity = sum(similarities) / len(similarities) if similarities else 0
    print(f"Ortalama Benzerlik: {average_similarity}")
    
    return average_similarity > 0.30

# Soru sorma ve yanıt alma fonksiyonu
def ask_chatbot(user_id, question):
    users_data = load_users_data()
    if not is_related(users_data["users"].get(user_id, {}).get("context", ""), question, users_data["users"].get(user_id, {}).get("questions", [])):
        reset_user_data(user_id)
    update_user_data(user_id, question)
    users_data = load_users_data()
    user_context = users_data["users"][user_id]["context"]
    inputs = tokenizer.encode(user_context, return_tensors='pt')
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = answer.replace("Cevap:", "").strip()  # Remove "cevap:" from the answer
    return answer


# Kullanıcı verilerini sıfırlama
def reset_user_data(user_id):
    users_data = load_users_data()
    if user_id in users_data["users"]:
        users_data["users"][user_id] = {"questions": [], "context": ""}
        save_users_data(users_data)

# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html')

# Hakkımızda sayfası
@app.route('/about')
def about():
    return render_template('about.html')

# Projemiz sayfası
@app.route('/project')
def project():
    return render_template('project.html')

# Sohbet sayfası
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    user_id = request.form.get('user_id', 'default_user')
    question = request.form.get('question', '')

    if request.method == 'POST' and question:
        answer = ask_chatbot(user_id, question)
    else:
        answer = "Lütfen bir soru girin."

    return render_template('chat.html', user_id=user_id, question=question, answer=answer)

# Belleği sıfırlama işlemi
@app.route('/reset', methods=['POST'])
def reset():
    if os.path.exists(users_data_file):
        os.remove(users_data_file)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)