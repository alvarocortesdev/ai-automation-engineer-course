# Model Card — <TODO: name of your RAG assistant>

<!--
Plantilla de model card para el asistente RAG del capstone. Escríbela EN INGLÉS (convención).
Lo importante NO es llenar campos: es que "Out-of-scope uses" y "Limitations" sean honestos
y específicos. Borra los <TODO> y los comentarios al terminar.
Referencia: https://huggingface.co/docs/hub/en/model-cards
-->

## Intended use
<!-- What is this system FOR? Who uses it and for what task? -->
<TODO: e.g. "Answer employee questions about internal product documentation, always citing the source document.">

## Out-of-scope uses
<!-- What it must NOT be used for. This section is what protects you. Be explicit. -->
- <TODO: e.g. "Not for legal, medical or financial advice.">
- <TODO: e.g. "Does not make decisions about people (hiring, credit). It informs, it does not decide.">
- <TODO: e.g. "Not a source of truth without a citation: if it can't find the source, it must say 'I don't know'.">

## Data
<!-- What corpus does it index? Source, date/version, language, licensing, PII status. -->
- Corpus: <TODO: e.g. "1,200 internal KB documents, version 2026-06">
- Languages: <TODO>
- Embeddings model: <TODO>
- PII: <TODO: e.g. "No customer PII (verified during ingest)">

## Evaluation
<!-- Numbers from your eval harness (6.9). Report per-group / per-language if relevant. -->
- Recall@5 = <TODO> on <TODO: e.g. "120 golden questions">
- Faithfulness (LLM-as-judge) = <TODO>
- <TODO: per-language or per-group breakdown if it applies>

## Limitations and risks
<!-- Where does it fail? Hallucination, knowledge cutoff, bias, untested domains. -->
- <TODO: e.g. "May hallucinate if retrieval fails">
- <TODO: e.g. "Knowledge cutoff = corpus date">
- <TODO: e.g. "Possible bias inherited from the KB">

## Governance
<!-- EU AI Act tier, transparency obligation, accountable human, audit logging. -->
- EU AI Act tier: <TODO: e.g. "Limited risk (chatbot) -> Article 50 transparency applies">
- Extraterritorial scope: <TODO: e.g. "Yes — EU users receive the output">
- Transparency: <TODO: e.g. "UI shows 'You are talking to an AI assistant'">
- Accountable owner: <TODO: team/role>
- Audit logging: <TODO: e.g. "Yes — structured, PII-redacted, hash-chained (see audit_log.py)">
