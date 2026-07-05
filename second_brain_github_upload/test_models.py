import google.generativeai as genai

def test_models():
    api_key = input("Inserisci la tua API Key di Google AI Studio per il test: ")
    genai.configure(api_key=api_key.strip())

    print("\n--- INIZIO SCANSIONE MODELLI DISPONIBILI ---")
    try:
        models = list(genai.list_models())
        generate_models = [m for m in models if 'generateContent' in m.supported_generation_methods]
        
        print(f"\nTrovati {len(generate_models)} modelli che supportano la generazione di testo (generateContent):")
        for m in generate_models:
            print(f"- Nome: {m.name}")
            print(f"  Versione/Famiglia: {m.version if hasattr(m, 'version') else 'Sconosciuta'}")
            print(f"  Metodi supportati: {m.supported_generation_methods}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Errore durante la scansione: {e}")

if __name__ == "__main__":
    test_models()
