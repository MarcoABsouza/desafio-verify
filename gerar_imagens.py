from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("testes", exist_ok=True)

testes = [
    {
        "nome_ficheiro": "testes/pedido_1_ideal.png",
        "cor_fundo": "white",
        "cor_texto": "black",
        "texto": "CLÍNICA NOVA ESPERANÇA\nPaciente: Maria Oliveira\nCPF: 987.654.321-00\n\nSolicitação de Exames:\n- TSH\n- T4 Livre\n- Vitamina D"
    },
    {
        "nome_ficheiro": "testes/pedido_2_ruido.png",
        "cor_fundo": "#e0e0e0",
        "cor_texto": "#333333",
        "texto": "HOSPITAL SANTA LUZIA\nPaciente: Sr. Marcos\nCRM-SP 99887\n\nExames:\n- Colesterol Total\n- Sódio\n- Potássio"
    }
]

for teste in testes:
    img = Image.new('RGB', (600, 400), color=teste["cor_fundo"])
    draw = ImageDraw.Draw(img)
    
    draw.text((20, 20), teste["texto"], fill=teste["cor_texto"])
    
    img.save(teste["nome_ficheiro"])
    print(f"Imagem guardada: {teste['nome_ficheiro']}")